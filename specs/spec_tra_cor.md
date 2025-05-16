
# Advanced Transcription Correction Logic Specification

## Overview

This document specifies the requirements and implementation details for the advanced transcription correction algorithm that will be used in the YouTube Video Transcription Service. This algorithm provides more sophisticated matching and comparison between user-provided transcriptions and the original/reference transcriptions from YouTube videos, offering detailed and accurate feedback on the user's transcription performance.

## Purpose

The transcription correction system serves as the core evaluation mechanism that:

1. Compares a user's transcription attempt against the reference transcription from YouTube
2. Identifies various types of discrepancies: exact matches, near matches (mistakes), missing words, and wrong/extra words
3. Provides word-by-word feedback that helps users improve their listening and transcription skills
4. Aligns mismatched portions to maximize the learning value of the comparison

## Core Components

### 1. Word Model

```python
@dataclass
class Word:
    text: str                # Original text of the word
    timestamp: float         # Timestamp from the video where the word appears
    normalized: str = ""     # Normalized form for comparison (lowercase, punctuation removed, etc.)
```

### 2. Transcription Comparer

```python
class TranscriptionComparerV4Pro:
    def __init__(self, mistake_threshold: float = 0.75, window_size: int = 20, max_search: int = 200):
        self.mistake_threshold = mistake_threshold  # Similarity threshold to consider a word a "mistake" vs "wrong"
        self.window_size = window_size              # Size of window for searching matches (in words)
        self.max_search = max_search                # Maximum number of words to search ahead
```

## Algorithm Operation

The comparison algorithm operates in the following stages:

### 1. Direct Comparison Phase
- Compares words at the same position in both texts
- Identifies exact matches and near matches (mistakes)
- Adds them to the result with appropriate classification

### 2. Realignment Phase
- When direct matches fail, attempts to realign the texts
- Uses "dubles" (pairs of consecutive words) to find potential alignment points
- Searches in windows to efficiently handle larger texts

### 3. Gap Filling Phase
- After realignment, processes any text "gaps" between the previous position and new alignment
- Marks words as correct, mistakes, missing, or wrong based on comparison

### 4. Remaining Words Processing
- Processes any remaining words in either text
- Words remaining in user text are marked as "wrong"
- Words remaining in reference text are marked as "missing"

## Classification Types

Each word in the comparison result is classified as one of the following:

| Type | Description | Conditions |
|------|-------------|------------|
| `correct` | Perfect match | Words are equivalent (after normalization) |
| `mistake` | Minor error | Similarity ratio ≥ threshold (default: 0.75) |
| `missing` | Word from reference not in user text | Word not found in user text |
| `wrong` | Word in user text not in reference | Word not found in reference text |

## Implementation

### Required Dependencies

```python
from typing import List, Dict
from dataclasses import dataclass
from difflib import SequenceMatcher
```

### Word Equivalence Utility

A separate module (`app.services.transcription_equivalents`) provides the `are_equivalent` function:

```python
def are_equivalent(word1: str, word2: str) -> bool:
    """
    Determines if two normalized words are equivalent.
    This function handles exact matches as well as common variations
    of the same word (e.g., contractions, homonyms).
    
    Args:
        word1: First normalized word
        word2: Second normalized word
        
    Returns:
        True if words are considered equivalent, False otherwise
    """
    # Base case: exact match
    if word1 == word2:
        return True
        
    # Common contraction equivalents
    contractions = {
        "its": ["it's"],
        "youre": ["you're"],
        "theyre": ["they're"],
        "im": ["i'm"],
        # Add more common contractions as needed
    }
    
    # Check contractions in both directions
    if word1 in contractions and word2 in contractions[word1]:
        return True
    if word2 in contractions and word1 in contractions[word2]:
        return True
    
    # Additional equivalence rules can be added here
    
    return False
```

### Main Comparison Function

```python
def compare(self, user_words: List[Word], actual_words: List[Word]) -> List[Dict[str, str]]:
    """
    Compare user transcription against the reference transcription.
    
    Args:
        user_words: List of Word objects from user transcription
        actual_words: List of Word objects from reference transcription
        
    Returns:
        List of dictionaries with 'text' and 'type' keys, where 'type' is one of:
        'correct', 'mistake', 'missing', or 'wrong'
    """
    result = []
    user_idx = 0
    actual_idx = 0
    matched_once = False  # Controls whether to include missing words at the beginning
    
    # Direct comparison phase
    while user_idx < len(user_words) and actual_idx < len(actual_words):
        # Case 1: Words are equivalent (perfect match)
        if are_equivalent(user_words[user_idx].normalized, actual_words[actual_idx].normalized):
            # If this is our first match and we've skipped reference words,
            # add all skipped words as "missing"
            if not matched_once and actual_idx > 0:
                for idx in range(actual_idx):
                    result.append({'text': actual_words[idx].text, 'type': 'missing'})
            matched_once = True
            result.append({'text': user_words[user_idx].text, 'type': 'correct'})
            user_idx += 1
            actual_idx += 1
            continue

        # Case 2: Words are similar but not equivalent (mistake)
        if self.is_mistake(user_words[user_idx].normalized, actual_words[actual_idx].normalized):
            # Same logic for missing words at the beginning
            if not matched_once and actual_idx > 0:
                for idx in range(actual_idx):
                    result.append({'text': actual_words[idx].text, 'type': 'missing'})
            matched_once = True
            result.append({'text': user_words[user_idx].text, 'type': 'mistake'})
            user_idx += 1
            actual_idx += 1
            continue

        # Case 3: Need to realign the texts
        last_result_len = len(result)
        user_idx, actual_idx = self.realign_with_dubles(
            user_words, user_idx, 
            actual_words, actual_idx, 
            result, matched_once
        )

        # If realignment didn't add any results, mark as wrong/missing and advance
        if len(result) == last_result_len:
            result.append({'text': user_words[user_idx].text, 'type': 'wrong'})
            result.append({'text': actual_words[actual_idx].text, 'type': 'missing'})
            user_idx += 1
            actual_idx += 1

    # Process any remaining words
    while user_idx < len(user_words):
        result.append({'text': user_words[user_idx].text, 'type': 'wrong'})
        user_idx += 1

    while actual_idx < len(actual_words):
        result.append({'text': actual_words[actual_idx].text, 'type': 'missing'})
        actual_idx += 1

    return result
```

### Realignment Function

```python
def realign_with_dubles(self, user_words, user_start_idx, actual_words, actual_start_idx, result, matched_once):
    """
    Attempts to realign the transcription when direct matching fails.
    Uses "dubles" (pairs of consecutive words) to find potential alignment points.
    
    Args:
        user_words: Full list of user Word objects
        user_start_idx: Current index in user words
        actual_words: Full list of reference Word objects
        actual_start_idx: Current index in reference words
        result: Current result list being built
        matched_once: Whether we've matched at least one word already
        
    Returns:
        Tuple of (new_user_idx, new_actual_idx) after realignment
    """
    # Get the slice of arrays we're working with
    user_new_world = user_words[user_start_idx:]
    actual_target = actual_words[actual_start_idx:]

    # Generate "dubles" (pairs of consecutive words) for user text
    user_dubles = self.generate_dubles(user_new_world)

    # Search for matching dubles in windows of reference text
    for user_offset, duble_user in enumerate(user_dubles):
        # Iterate through windows of the reference text
        for window_start in range(0, min(len(actual_target), self.max_search), self.window_size):
            window_end = min(window_start + self.window_size, len(actual_target))
            window = actual_target[window_start:window_end]
            target_dubles = self.generate_dubles(window)

            # Check each pair in this window for a match
            for target_offset, duble_target in enumerate(target_dubles):
                if self.are_dubles_equivalent(duble_user, duble_target):
                    # We found a match! Calculate the actual position
                    full_target_start_idx = actual_start_idx + window_start + target_offset

                    # Handle missing words if this is our first match
                    if not matched_once and full_target_start_idx > 0:
                        for idx in range(actual_start_idx, full_target_start_idx):
                            result.append({'text': actual_words[idx].text, 'type': 'missing'})

                    # Process any words in the "gap" between current position and new alignment
                    self.fill_field_gaps(
                        user_words[user_start_idx:user_start_idx + user_offset],
                        actual_words[actual_start_idx:full_target_start_idx],
                        result
                    )

                    # Add the matched duble as correct words
                    for w in duble_user:
                        result.append({'text': w.text, 'type': 'correct'})
                    
                    # Return the new positions (after the dubles)
                    return user_start_idx + user_offset + 2, full_target_start_idx + 2

    # If no dubles matched, try word-by-word matching as fallback
    user_idx, actual_idx = user_start_idx, actual_start_idx
    while user_idx < len(user_words) and actual_idx < len(actual_words):
        if are_equivalent(user_words[user_idx].normalized, actual_words[actual_idx].normalized):
            if not matched_once and actual_idx > 0:
                for idx in range(actual_start_idx, actual_idx):
                    result.append({'text': actual_words[idx].text, 'type': 'missing'})
            result.append({'text': user_words[user_idx].text, 'type': 'correct'})
            return user_idx + 1, actual_idx + 1
            
        if self.is_mistake(user_words[user_idx].normalized, actual_words[actual_idx].normalized):
            if not matched_once and actual_idx > 0:
                for idx in range(actual_start_idx, actual_idx):
                    result.append({'text': actual_words[idx].text, 'type': 'missing'})
            result.append({'text': user_words[user_idx].text, 'type': 'mistake'})
            return user_idx + 1, actual_idx + 1
            
        actual_idx += 1

    # If no matches found, return original indices
    return user_start_idx, actual_start_idx
```

### Helper Functions

```python
def generate_dubles(self, words: List[Word]) -> List[List[Word]]:
    """
    Generates pairs of consecutive words ("dubles") from the input list.
    
    Args:
        words: List of Word objects
        
    Returns:
        List of word pairs
    """
    dubles = []
    for i in range(len(words) - 1):
        dubles.append([words[i], words[i+1]])
    return dubles

def are_dubles_equivalent(self, duble1: List[Word], duble2: List[Word]) -> bool:
    """
    Checks if two word pairs are equivalent by comparing normalized forms.
    
    Args:
        duble1: First pair of Word objects
        duble2: Second pair of Word objects
        
    Returns:
        True if all corresponding words are equivalent
    """
    return all(are_equivalent(w1.normalized, w2.normalized) for w1, w2 in zip(duble1, duble2))

def fill_field_gaps(self, user_gap: List[Word], actual_gap: List[Word], result: List[Dict[str, str]]):
    """
    Processes the "gap" between the current position and realignment point.
    Tries to match words in the gaps and classify them appropriately.
    
    Args:
        user_gap: List of user Word objects in the gap
        actual_gap: List of reference Word objects in the gap
        result: Result list to append classifications to
    """
    # Track which user words have been used in matching
    user_used = [False] * len(user_gap)

    # Process each word in the reference gap
    for aw in actual_gap:
        matched = False
        
        # First pass: look for exact matches
        for i, uw in enumerate(user_gap):
            if not user_used[i] and are_equivalent(uw.normalized, aw.normalized):
                result.append({'text': uw.text, 'type': 'correct'})
                user_used[i] = True
                matched = True
                break

        # Second pass: look for mistakes (similar but not exact)
        if not matched:
            for i, uw in enumerate(user_gap):
                if not user_used[i] and self.is_mistake(uw.normalized, aw.normalized):
                    result.append({'text': uw.text, 'type': 'mistake'})
                    user_used[i] = True
                    matched = True
                    break

        # If no match found in user text, mark as missing
        if not matched:
            result.append({'text': aw.text, 'type': 'missing'})

    # Mark any unused user words as wrong
    for i, used in enumerate(user_used):
        if not used:
            result.append({'text': user_gap[i].text, 'type': 'wrong'})

def is_mistake(self, user_norm: str, actual_norm: str) -> bool:
    """
    Determines if two words are similar enough to be considered a mistake
    rather than completely wrong.
    
    Args:
        user_norm: Normalized user word
        actual_norm: Normalized reference word
        
    Returns:
        True if similarity ratio is at or above the mistake threshold
    """
    # Calculate similarity ratio using SequenceMatcher
    ratio = SequenceMatcher(None, user_norm, actual_norm).ratio()
    # Return true if similarity meets or exceeds threshold
    return ratio >= self.mistake_threshold
```

## Integration with Existing System

### Frontend Integration

1. The frontend will send the user's transcription attempt to the backend for comparison
2. The backend will process the text using the TranscriptionComparerV4Pro
3. Results will be returned to the frontend in a consistent format
4. The frontend will render the comparison results with appropriate styling:
   - `correct`: Green text
   - `mistake`: Yellow text
   - `missing`: Gray text (or strikethrough)
   - `wrong`: Red text

### Backend API Integration

Extend the existing `/transcriptions/analyze` endpoint:

```python
@router.post("/analyze", response_model=schemas.TranscriptionAnalysis)
async def analyze_transcription(
    request: schemas.TranscriptionAnalysisRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Analyze and compare user transcription against reference.
    
    Args:
        request: Contains user_text (user's transcription) and reference_text
        
    Returns:
        Detailed analysis including word-by-word comparison
    """
    # Create Word objects with normalized text
    user_words = []
    for idx, word in enumerate(request.user_text.split()):
        user_words.append(Word(
            text=word,
            timestamp=idx,  # Placeholder timestamp (could be refined with actual timestamps)
            normalized=preprocess_text(word)
        ))
    
    reference_words = []
    for idx, word in enumerate(request.reference_text.split()):
        reference_words.append(Word(
            text=word,
            timestamp=idx,
            normalized=preprocess_text(word)
        ))
    
    # Instantiate comparer and get results
    comparer = TranscriptionComparerV4Pro()
    comparison_result = comparer.compare(user_words, reference_words)
    
    # Calculate overall statistics
    total_words = len(reference_words)
    correct_words = sum(1 for item in comparison_result if item['type'] == 'correct')
    mistake_words = sum(1 for item in comparison_result if item['type'] == 'mistake')
    missing_words = sum(1 for item in comparison_result if item['type'] == 'missing')
    wrong_words = sum(1 for item in comparison_result if item['type'] == 'wrong')
    
    # Calculate accuracy score
    accuracy_score = (correct_words + (mistake_words * 0.5)) / total_words if total_words > 0 else 0.0
    
    return {
        "comparison": comparison_result,
        "overall_accuracy": accuracy_score,
        "stats": {
            "correct_words": correct_words,
            "mistake_words": mistake_words,
            "missing_words": missing_words,
            "wrong_words": wrong_words,
            "total_words": total_words
        }
    }
```

## Enhancements and Extensions

### Timestamp-Based Alignment
- Use word timestamps from YouTube transcription to better align with user input
- Allow for rewinding to specific words that were incorrect

### Learning Analytics
- Track common mistake patterns for individual users
- Provide personalized recommendations based on error types

### Language-Specific Rules
- Add language-specific equivalence rules
- Support for multiple languages with specialized comparison logic

## Performance Considerations

1. **Time Complexity**: The algorithm has O(n*m) worst-case time complexity where n is user word count and m is reference word count. The windowing approach keeps performance reasonable for most transcriptions.

2. **Memory Usage**: Memory usage scales linearly with the size of the input texts.

3. **Optimization Techniques**:
   - Window-based searching to limit comparison scope
   - Early termination of searches when matches are found
   - Caching of normalized forms and comparison results

## Testing Strategy

1. **Unit Tests**:
   - Test Word class and normalization
   - Test different comparison scenarios (exact matches, near matches, realignments)
   - Test edge cases (empty inputs, single-word inputs, very dissimilar inputs)

2. **Integration Tests**:
   - Test API endpoint with various input combinations
   - Verify correct calculation of statistics
   - Ensure proper error handling

3. **Performance Tests**:
   - Benchmark algorithm with large inputs
   - Ensure response times remain acceptable

## Implementation Timeline

1. **Phase 1** (Week 1):
   - Implement core Word class and equivalence function
   - Basic comparison algorithm without realignment

2. **Phase 2** (Week 2):
   - Implement realignment and gap filling logic
   - Add comprehensive test suite

3. **Phase 3** (Week 3):
   - Integrate with existing API endpoints
   - Frontend integration
   - Performance optimizations

## Conclusion

The TranscriptionComparerV4Pro provides a sophisticated algorithm for comparing user transcriptions against reference transcriptions, offering detailed and accurate feedback. This helps users improve their transcription skills by identifying exactly where and how they made errors, with intelligent alignment capabilities to handle scenarios where users may skip or add words. 