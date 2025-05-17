"""
Advanced Transcription Comparison Algorithm

This module implements a sophisticated algorithm for comparing user transcriptions
against reference transcriptions from YouTube videos. It provides word-by-word
feedback on accuracy and identifies various types of discrepancies.

Requirements fulfilled:
- Word-by-word comparison with multiple classification types
- Realignment capability for mismatched transcriptions
- Similarity detection for near-matches (mistakes)
- Performance optimization with windowed searching
"""

import logging
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Tuple, Union

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class Word:
    """
    Model for a single word in a transcription.
    """
    text: str                # Original text of the word
    timestamp: float = 0.0    # Timestamp from the video where the word appears
    normalized: str = ""     # Normalized form for comparison (lowercase, punctuation removed, etc.)
    
    def __post_init__(self):
        """Automatically normalize the word text after initialization."""
        if not self.normalized:
            self.normalized = normalize_word(self.text)


def normalize_word(text: str) -> str:
    """
    Normalize a word for comparison by lowercasing and removing punctuation.
    
    Args:
        text: The word to normalize
        
    Returns:
        Normalized form of the word
    """
    # Convert to lowercase
    normalized = text.lower()
    
    # Remove punctuation
    normalized = re.sub(r'[^\w\s]', '', normalized)
    
    # Remove extra whitespace
    normalized = normalized.strip()
    
    return normalized


def normalize_text(text: str) -> str:
    """
    Normalize a complete text for comparison.
    
    Args:
        text: The text to normalize
        
    Returns:
        Normalized form of the text
    """
    # Convert to lowercase
    normalized = text.lower()
    
    # Replace common contractions
    contractions = {
        "won't": "will not",
        "can't": "cannot",
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "wouldn't": "would not",
        "couldn't": "could not",
        "shouldn't": "should not",
        "mightn't": "might not",
        "mustn't": "must not",
        "i'm": "i am",
        "you're": "you are",
        "he's": "he is",
        "she's": "she is",
        "it's": "it is",
        "we're": "we are",
        "they're": "they are",
        "i've": "i have",
        "you've": "you have",
        "we've": "we have",
        "they've": "they have",
        "i'd": "i would",
        "you'd": "you would",
        "he'd": "he would",
        "she'd": "she would",
        "we'd": "we would",
        "they'd": "they would",
        "i'll": "i will",
        "you'll": "you will",
        "he'll": "he will",
        "she'll": "she will",
        "we'll": "we will",
        "they'll": "they will"
    }
    
    for contraction, expansion in contractions.items():
        normalized = normalized.replace(contraction, expansion)
    
    # Remove punctuation
    normalized = re.sub(r'[^\w\s]', '', normalized)
    
    # Replace multiple spaces with a single space
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Remove leading/trailing whitespace
    normalized = normalized.strip()
    
    return normalized


def are_equivalent(word1: str, word2: str) -> bool:
    """
    Check if two words are equivalent after normalization.
    
    Args:
        word1: First word
        word2: Second word
        
    Returns:
        True if the words are equivalent, False otherwise
    """
    # Handle empty cases
    if not word1 and not word2:
        return True
    if not word1 or not word2:
        return False
    
    return word1 == word2


def calculate_similarity(word1: str, word2: str) -> float:
    """
    Calculate the similarity between two words.
    
    Args:
        word1: First word
        word2: Second word
        
    Returns:
        Similarity ratio between 0.0 and 1.0
    """
    # Handle empty cases
    if not word1 and not word2:
        return 1.0
    if not word1 or not word2:
        return 0.0
    
    # Use SequenceMatcher to calculate similarity
    return SequenceMatcher(None, word1, word2).ratio()


def text_to_word_list(text: str, timestamps: List[float] = None) -> List[Word]:
    """
    Convert a text string into a list of Word objects.
    
    Args:
        text: Input text
        timestamps: Optional list of timestamps for each word (if available)
        
    Returns:
        List of Word objects
    """
    # Split text into words
    words = re.findall(r'\S+', text)
    
    # Create Word objects
    word_list = []
    for i, word_text in enumerate(words):
        timestamp = timestamps[i] if timestamps and i < len(timestamps) else 0.0
        word_list.append(Word(text=word_text, timestamp=timestamp))
    
    return word_list


class TranscriptionComparerV4Pro:
    """
    Advanced transcription comparison algorithm.
    
    Compares a user transcription against a reference transcription,
    identifying matches, mistakes, missing words, and wrong words.
    """
    
    def __init__(
        self, 
        mistake_threshold: float = 0.75, 
        window_size: int = 20, 
        max_search: int = 200
    ):
        """
        Initialize the transcription comparer.
        
        Args:
            mistake_threshold: Similarity threshold for considering a word a mistake (default: 0.75)
            window_size: Size of window for searching matches (default: 20 words)
            max_search: Maximum number of words to search ahead (default: 200)
        """
        self.mistake_threshold = mistake_threshold
        self.window_size = window_size
        self.max_search = max_search
    
    def compare(
        self, 
        user_text: str, 
        reference_text: str, 
        user_timestamps: List[float] = None, 
        reference_timestamps: List[float] = None
    ) -> List[Dict[str, str]]:
        """
        Compare user transcription against the reference transcription.
        
        Args:
            user_text: User's transcription text
            reference_text: Reference transcription text
            user_timestamps: Optional timestamps for user text
            reference_timestamps: Optional timestamps for reference text
            
        Returns:
            List of dictionaries with 'text' and 'type' keys, where 'type' is one of:
            'correct', 'mistake', 'missing', or 'wrong'
        """
        # Convert texts to lists of Word objects
        user_words = text_to_word_list(user_text, user_timestamps)
        reference_words = text_to_word_list(reference_text, reference_timestamps)
        
        # Comparison results
        result = []
        
        # Tracking indices
        user_idx = 0
        reference_idx = 0
        matched_once = False  # Flag to track if we've matched at least one word
        
        # Direct comparison phase
        while user_idx < len(user_words) and reference_idx < len(reference_words):
            # Case 1: Words are equivalent (perfect match)
            if are_equivalent(user_words[user_idx].normalized, reference_words[reference_idx].normalized):
                # If this is our first match and we've skipped reference words,
                # add all skipped words as "missing"
                if not matched_once and reference_idx > 0:
                    for idx in range(reference_idx):
                        result.append({'text': reference_words[idx].text, 'type': 'missing'})
                matched_once = True
                result.append({'text': user_words[user_idx].text, 'type': 'correct'})
                user_idx += 1
                reference_idx += 1
                continue

            # Case 2: Words are similar but not equivalent (mistake)
            if self.is_mistake(user_words[user_idx].normalized, reference_words[reference_idx].normalized):
                # Same logic for missing words at the beginning
                if not matched_once and reference_idx > 0:
                    for idx in range(reference_idx):
                        result.append({'text': reference_words[idx].text, 'type': 'missing'})
                matched_once = True
                result.append({'text': user_words[user_idx].text, 'type': 'mistake'})
                user_idx += 1
                reference_idx += 1
                continue

            # Case 3: Need to realign the texts
            last_result_len = len(result)
            user_idx, reference_idx = self.realign_with_dubles(
                user_words, user_idx, 
                reference_words, reference_idx, 
                result, matched_once
            )

            # If realignment didn't add any results, mark current words as wrong/missing and advance
            if len(result) == last_result_len:
                result.append({'text': user_words[user_idx].text, 'type': 'wrong'})
                user_idx += 1
                # Only advance the reference index if we've already matched at least one word
                # This handles cases where the user starts with completely different text
                if matched_once:
                    result.append({'text': reference_words[reference_idx].text, 'type': 'missing'})
                    reference_idx += 1

        # Process any remaining user words as wrong
        while user_idx < len(user_words):
            result.append({'text': user_words[user_idx].text, 'type': 'wrong'})
            user_idx += 1

        # Process any remaining reference words as missing
        while reference_idx < len(reference_words):
            result.append({'text': reference_words[reference_idx].text, 'type': 'missing'})
            reference_idx += 1

        return result
    
    def realign_with_dubles(
        self, 
        user_words: List[Word], 
        user_start_idx: int, 
        reference_words: List[Word], 
        reference_start_idx: int, 
        result: List[Dict[str, str]], 
        matched_once: bool
    ) -> Tuple[int, int]:
        """
        Attempts to realign the transcription when direct matching fails.
        Uses "dubles" (pairs of consecutive words) to find potential alignment points.
        
        Args:
            user_words: List of Word objects from user transcription
            user_start_idx: Current position in user transcription
            reference_words: List of Word objects from reference transcription
            reference_start_idx: Current position in reference transcription
            result: Current comparison results (modified in-place)
            matched_once: Whether we've matched at least one word
            
        Returns:
            Tuple of (new user index, new reference index)
        """
        user_new_words = user_words[user_start_idx:]
        reference_target = reference_words[reference_start_idx:]
        
        # Generate dubles (pairs of consecutive words) from user text
        user_dubles = self.generate_dubles(user_new_words)
        
        # Search for dubles in reference text
        for user_offset, duble_user in enumerate(user_dubles):
            # Search in windows to limit computation
            for window_start in range(0, min(len(reference_target), self.max_search), self.window_size):
                window_end = min(window_start + self.window_size, len(reference_target))
                window = reference_target[window_start:window_end]
                reference_dubles = self.generate_dubles(window)
                
                # Check each duble in the current window
                for reference_offset, duble_reference in enumerate(reference_dubles):
                    # If dubles match, we found an alignment point
                    if self.are_dubles_equivalent(duble_user, duble_reference):
                        # Calculate absolute reference index
                        full_reference_start_idx = reference_start_idx + window_start + reference_offset
                        
                        # If this is our first match and we've skipped reference words,
                        # add all skipped words as "missing"
                        if not matched_once and full_reference_start_idx > 0:
                            for idx in range(reference_start_idx, full_reference_start_idx):
                                result.append({'text': reference_words[idx].text, 'type': 'missing'})
                        
                        # Process words in the gap between old positions and new alignment
                        self.fill_field_gaps(
                            user_words[user_start_idx:user_start_idx + user_offset],
                            reference_words[reference_start_idx:full_reference_start_idx],
                            result
                        )
                        
                        # Add the matching dubles as correct
                        for w in duble_user:
                            result.append({'text': w.text, 'type': 'correct'})
                        
                        # Return new positions after the matching dubles
                        return user_start_idx + user_offset + 2, full_reference_start_idx + 2
        
        # If no dubles matched, try matching individual words within a window
        # (This is a fallback for the case where we don't have enough words for dubles)
        user_idx, reference_idx = user_start_idx, reference_start_idx
        max_reference_idx = min(len(reference_words), reference_start_idx + self.max_search)
        
        while user_idx < len(user_words) and reference_idx < max_reference_idx:
            # Check for exact match
            if are_equivalent(user_words[user_idx].normalized, reference_words[reference_idx].normalized):
                if not matched_once and reference_idx > 0:
                    for idx in range(reference_start_idx, reference_idx):
                        result.append({'text': reference_words[idx].text, 'type': 'missing'})
                result.append({'text': user_words[user_idx].text, 'type': 'correct'})
                return user_idx + 1, reference_idx + 1
            
            # Check for mistake (similar but not exact)
            if self.is_mistake(user_words[user_idx].normalized, reference_words[reference_idx].normalized):
                if not matched_once and reference_idx > 0:
                    for idx in range(reference_start_idx, reference_idx):
                        result.append({'text': reference_words[idx].text, 'type': 'missing'})
                result.append({'text': user_words[user_idx].text, 'type': 'mistake'})
                return user_idx + 1, reference_idx + 1
            
            # Move to next reference word
            reference_idx += 1
        
        # If no alignment found, stay at current positions
        return user_start_idx, reference_start_idx
    
    def generate_dubles(self, words: List[Word]) -> List[List[Word]]:
        """
        Generate dubles (pairs of consecutive words) from a list of words.
        
        Args:
            words: List of Word objects
            
        Returns:
            List of dubles (each duble is a list of two Word objects)
        """
        dubles = []
        for i in range(len(words) - 1):
            dubles.append([words[i], words[i+1]])
        return dubles
    
    def are_dubles_equivalent(self, duble1: List[Word], duble2: List[Word]) -> bool:
        """
        Check if two dubles are equivalent.
        
        Args:
            duble1: First duble (list of two Word objects)
            duble2: Second duble (list of two Word objects)
            
        Returns:
            True if the dubles are equivalent, False otherwise
        """
        # Both words in both dubles must be equivalent
        return (are_equivalent(duble1[0].normalized, duble2[0].normalized) and 
                are_equivalent(duble1[1].normalized, duble2[1].normalized))
    
    def fill_field_gaps(self, user_gap: List[Word], reference_gap: List[Word], result: List[Dict[str, str]]):
        """
        Process the gaps between previous position and new alignment.
        
        Args:
            user_gap: List of user words in the gap
            reference_gap: List of reference words in the gap
            result: Current comparison results (modified in-place)
        """
        # Track which user words have been matched
        user_used = [False] * len(user_gap)
        
        # First pass: look for exact matches and mistakes
        for rw in reference_gap:
            matched = False
            
            # Look for exact matches
            for i, uw in enumerate(user_gap):
                if not user_used[i] and are_equivalent(uw.normalized, rw.normalized):
                    result.append({'text': uw.text, 'type': 'correct'})
                    user_used[i] = True
                    matched = True
                    break
            
            # If no exact match, look for mistakes
            if not matched:
                for i, uw in enumerate(user_gap):
                    if not user_used[i] and self.is_mistake(uw.normalized, rw.normalized):
                        result.append({'text': uw.text, 'type': 'mistake'})
                        user_used[i] = True
                        matched = True
                        break
            
            # If no match found, mark as missing
            if not matched:
                result.append({'text': rw.text, 'type': 'missing'})
        
        # Add any remaining user words as wrong
        for i, used in enumerate(user_used):
            if not used:
                result.append({'text': user_gap[i].text, 'type': 'wrong'})
    
    def is_mistake(self, user_norm: str, reference_norm: str) -> bool:
        """
        Check if a user word is similar enough to a reference word to be considered a mistake.
        
        Args:
            user_norm: Normalized user word
            reference_norm: Normalized reference word
            
        Returns:
            True if it's a mistake, False otherwise
        """
        similarity = calculate_similarity(user_norm, reference_norm)
        return similarity >= self.mistake_threshold


def compare_transcriptions(user_text: str, reference_text: str) -> float:
    """
    Compare two transcriptions and return an overall accuracy score.
    
    Args:
        user_text: User's transcription text
        reference_text: Reference transcription text
        
    Returns:
        Accuracy score between 0.0 and 1.0
    """
    # Normalize texts
    user_normalized = normalize_text(user_text)
    reference_normalized = normalize_text(reference_text)
    
    # Simple case: texts are identical
    if user_normalized == reference_normalized:
        return 1.0
    
    # Simple case: one or both texts are empty
    if not user_normalized or not reference_normalized:
        return 0.0
    
    # Use SequenceMatcher for an overall similarity score
    similarity = SequenceMatcher(None, user_normalized, reference_normalized).ratio()
    
    return similarity


def get_detailed_comparison(
    user_text: str, 
    reference_text: str, 
    user_timestamps: List[float] = None, 
    reference_timestamps: List[float] = None
) -> Tuple[List[Dict[str, str]], float, Dict[str, int]]:
    """
    Get a detailed comparison between user transcription and reference transcription.
    
    Args:
        user_text: User's transcription text
        reference_text: Reference transcription text
        user_timestamps: Optional timestamps for user text words
        reference_timestamps: Optional timestamps for reference text words
        
    Returns:
        Tuple of (comparison results, overall accuracy, statistics)
    """
    # Create comparer
    comparer = TranscriptionComparerV4Pro()
    
    # Get comparison results
    comparison = comparer.compare(
        user_text, 
        reference_text, 
        user_timestamps, 
        reference_timestamps
    )
    
    # Calculate statistics
    correct_count = sum(1 for item in comparison if item['type'] == 'correct')
    mistake_count = sum(1 for item in comparison if item['type'] == 'mistake')
    missing_count = sum(1 for item in comparison if item['type'] == 'missing')
    wrong_count = sum(1 for item in comparison if item['type'] == 'wrong')
    total_count = correct_count + mistake_count + missing_count + wrong_count
    
    # Calculate overall accuracy
    if total_count > 0:
        # Consider mistakes as half-correct
        accuracy = (correct_count + (mistake_count * 0.5)) / total_count
    else:
        accuracy = 0.0
    
    # Statistics
    stats = {
        "correct_words": correct_count,
        "mistake_words": mistake_count,
        "missing_words": missing_count,
        "wrong_words": wrong_count,
        "total_words": total_count
    }
    
    return comparison, accuracy, stats 