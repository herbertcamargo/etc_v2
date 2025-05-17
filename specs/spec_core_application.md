# Specification: Core Transcription Application
<!-- 
1. Overview
2. Page Routing & Structure
3. UI/UX Design and Accessibility
4. Video Player Buttons & Behavior
5. Frontend Logic & State Management
6. Backend Architecture
7. API Endpoints
8. Comprehensive Data Models
9. Testing Strategy
10. Deployment Considerations
11. Theme System Implementation
12. Compliance Requirements
13. UI Layout System and Grid Specifications
14. Project Structure Alignment
15. Additional Implementation Guidelines
16. Conclusion 
-->
## 1. Overview

This document defines the comprehensive requirements and implementation details for the transcription workflow application. It integrates the transcription page creation, buttons and behaviors, caching mechanism, YouTube video capture service, and transcription correction logic into a cohesive specification. It fully aligns with the codebase's architecture, design system, API conventions, accessibility, performance targets, and testing strategy.

---

### 1.1. Specification Source Traceability

This specification integrates requirements from the following source documents:
- `application-design.md`: Core architecture and data models
- `application-requirements.md`: Functional and non-functional requirements
- `frontend-update.md`: UI/UX design principles and component specifications
- `implementation-plan.md`: Phased development approach and deployment strategy
- `project-directory-and-file-structure.md`: Code organization and file structure

---

### 1.2. Integration of Detailed Requirements from Source Specifications

This section contains the full integration of all implementation details, code snippets, and requirements from multiple source specifications, ensuring no detail is omitted.

#### 1.2.1. Implementation Phases Mapping

The implementation of the transcription application follows a phased approach as outlined in `implementation-plan.md`:

- **Phase 1: Foundation**
  - Backend setup with FastAPI
  - Database models implementation
  - Authentication system with JWT
  - Basic frontend structure with React
- **Phase 2: Core Features**
  - YouTube video search and playback integration
  - Transcription input system and comparison algorithm
  - User dashboard and progress tracking
- **Phase 3: Subscription & Polish**
  - Stripe integration for payment processing
  - Subscription management
  - UI/UX refinements
- **Phase 4: Deployment & Launch**
  - Production environment configuration
  - Monitoring and alerting setup
  - Final QA and performance optimization

---

## 2. Page Routing & Structure

### 2.1. Routes

| Route Pattern               | Description                           |
|---------------------------- |---------------------------------------|
| `/transcribe`               | Entry point for video search          |
| `/transcribe/:videoId`      | Transcription page for selected video |

### 2.2. Component Architecture

- All shared UI elements must be abstracted into reusable components.
- Follow the project's React directory conventions:

```
src/
├── pages/
│   ├── transcribe/
│   │   ├── index.tsx        // Video search page
│   │   └── [videoId].tsx    // Transcription page
├── components/
│   ├── YouTubeSearch/
│   ├── SearchResults/
│   ├── VideoPlayer/
│   ├── TranscriptionInput/
│   ├── ButtonSet/
│   └── ResultsOutput/
```

---

## 3. UI/UX Design and Accessibility

### 3.1. General Principles

- Use the color palettes, font system, and layout tokens from `specs/frontend-update.md`.
- All pages must be fully responsive and provide an excellent experience on desktop and mobile.
- Adhere to accessibility (a11y) best practices: semantic HTML, ARIA attributes, keyboard navigation, sufficient contrast, and focus management.

### 3.2. Key Components

#### 3.2.1. YouTube Search Bar
- Large input box with floating label.
- Primary gradient "Search" button.
- Keyboard accessible (focus, enter key triggers search).
- Styled as per design tokens.

#### 3.2.2. Search Results
- Display top 12 YouTube video results in a 4x3 responsive grid.
- Each result card includes:
  - Thumbnail (with alt text)
  - Video title (truncated, tooltip on overflow)
  - Channel, duration, and other metadata
  - Clickable/selectable for navigation
- Hover/focus effects for accessibility and feedback.
- **User Authentication Check:**
  - Before navigating to the transcription page, validate if the user is authenticated
  - If not authenticated, display a warning message: "Login before starting transcribing"
  - This validation must occur before triggering any API calls or resource loading

#### 3.2.3. Video Player
- Responsive embedded YouTube iframe.
- Error messaging for unsupported videos.
- Anchor page scroll to this section on load/reload.

#### 3.2.4. Transcription Input
- Multi-line textarea with floating label.
- Live character/word count.
- Auto-save draft support (local/session storage).
- Clear error and disabled states.
- **After clicking "Try Again", the input field must be prefilled with the user's previous attempt rather than being cleared.**

#### 3.2.5. Button Set
- Horizontal arrangement of action buttons.
- Each button must follow the exact behavior and state transitions as specified in the Button Behavior section.
- Consistent spacing and color feedback for all states.

##### 3.2.5.1. Tooltips for Button Clarification
- **Pause Delay Dropdown:** Tooltip: "Sets how long the video remains paused after you stop typing"
- **Rewind Time Dropdown:** Tooltip: "Controls how far back the video rewinds after pausing"
- **Rewind Button:** Tooltip: "Rewinds the video by the selected time amount"
- **Play/Stop Button:** Tooltip: "Play or pause the video playback"
- **Submit Transcription Button:** Tooltip: "Compare your transcription with the original"

#### 3.2.6. Results Output
- Results box with the title "Transcription Results"

##### 3.2.6.1. Animated Transitions for New Results
- Fade-in transition (300ms) when new results are displayed
- Subtle highlight effect on newly displayed results
- Smooth scroll to results section when new comparison is generated
- Animation must be subtle and not distracting from the content
- Disable animations if user has set "reduce motion" in their accessibility preferences

---

## 4. Video Player Buttons & Behavior

### 4.1. Pause Delay Dropdown
- **Label**: `"Pause Delay"`
- **Options**: `0`, `1`, `2`, `3`, `5` (seconds)
- **Default**: `2` seconds or the last user selection

#### 4.1.1. Behavior
- If the selected value is **not `0`**:
  - When the user **types or deletes** inside the transcription input (`#user-try`):
    - Start or **restart** a countdown for the selected seconds
    - While the countdown is running: **pause** the video
    - When the countdown ends: **resume** playback
- Countdown is only triggered if:
  - The video was **already playing**, or
  - The countdown was already **active**

### 4.2. Rewind Time Dropdown
- **Label**: `"Rewind time"`
- **Options**: `0.0`, `0.25`, `0.5`, `0.75`, `1`, `2`, `3`, `5` (seconds)
- **Default**: `2` seconds or the last user selection

#### 4.2.1. Behavior
- This dropdown serves **two purposes**:
  1. Referenced by the `Rewind_Button`
  2. Works **with `Pause_Delay_Dropdown`**:
     - If both dropdowns are set to a value different from `0`:
       - When the `Pause_Delay_Dropdown` countdown ends:
         - **Rewind** the video by the selected `Rewind_time_Dropdown` value
         - Then **continue playing**

### 4.3. Rewind Button
- **Label**: `"Rewind"` (centered)
- **Action**: On click, rewinds the video by the currently selected `Rewind_time_Dropdown` value

### 4.4. Play/Stop Button
- **State 1** (video is playing):
  - Text: `"Stop"`
  - Color: **dark red**
  - Text color: **white**
- **State 2** (video is paused):
  - Text: `"Play"`
  - Color: **dark green**
  - Text color: **white**

#### 4.4.1. Behavior
- On click: toggle video state
  - If playing → pause
  - If paused → play

### 4.5. Submit Transcription Button
- **State 1** (transcription comparison results are not shown):
  - Text: `"Submit Transcription"`
  - Color: **dark yellow**
  - Text color: **white**
- **State 2** (transcription comparison results are shown):
  - Text: `"Try Again"`
  - Color: **dark amber**
  - Text color: **white**

#### 4.5.1. Behavior
- On click: activate the backend steps to generate the transcription comparison results
  - If transcription comparison results are not yet shown → show transcription comparison results
  - If transcription comparison results are being shown → stop showing the transcription comparison results

---

## 5. Frontend Logic & State Management

### 5.1. Loading and Error Feedback

All user actions must provide clear loading and error feedback:

- **Loading Indicators:**
  - Use a consistent spinner component for all asynchronous operations
  - For video search: Overlay spinner on the search results area
  - For transcription submission: Transform the submit button into a loading state
  - For video loading: Show a skeleton UI in the player area
  - All loading states must include appropriate ARIA attributes for accessibility
  
- **Error Feedback:**
  - Display inline error messages directly beneath the relevant component
  - Use toast notifications for transient errors that don't block the workflow
  - All error messages must be clear, actionable, and use consistent styling
  - Provide retry options where appropriate
  - Log errors to monitoring system while showing user-friendly messages

### 5.2. Auto-save Draft Implementation

The transcription input component must implement reliable auto-save functionality to prevent user work loss:

1. **Storage Strategy**
   - Use browser's localStorage to store draft transcriptions
   - Create a unique key for each video using format `transcription_draft_{videoId}`
   - Implement an optional fallback to sessionStorage if localStorage is unavailable
   
2. **Save Triggers**
   - Automatically save draft transcription after every 5 seconds of inactivity
   - Save on explicit page navigation events or tab closing
   - Save before form submission
   
3. **Restoration Logic**
   - Check for existing draft when loading the transcription page
   - If a draft exists, display a notification allowing the user to restore or discard
   - If restored, populate the transcription input with the saved content
   
4. **Implementation Details**
   ```javascript
   // Draft auto-save implementation
   const autosaveDraft = (videoId, content) => {
     const key = `transcription_draft_${videoId}`;
     try {
       localStorage.setItem(key, content);
       return true;
     } catch (error) {
       console.error("Failed to save draft:", error);
       try {
         // Fallback to session storage
         sessionStorage.setItem(key, content);
         return true;
       } catch (innerError) {
         console.error("Failed to save to session storage:", innerError);
         return false;
       }
     }
   };
   
   const loadDraft = (videoId) => {
     const key = `transcription_draft_${videoId}`;
     return localStorage.getItem(key) || sessionStorage.getItem(key) || null;
   };
   
   const clearDraft = (videoId) => {
     const key = `transcription_draft_${videoId}`;
     localStorage.removeItem(key);
     sessionStorage.removeItem(key);
   };
   ```

---

## 6. Backend Architecture

### 6.1. YouTube Video Capture and Transcription Service

#### 6.1.1. Core Components

##### 6.1.1.1. YouTube API Client

A service class that interacts with the YouTube Data API v3 for searching videos and retrieving video metadata.

```python
class YouTubeClient:
    """
    Client for interacting with YouTube Data API v3.
    Handles authentication, video searching, and metadata retrieval.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    async def build_client(self):
        """Create an authenticated YouTube API client."""
        # Implementation with googleapiclient.discovery in an async-compatible way
        
    async def search_videos(self, query: str, max_results: int = 10) -> list[dict]:
        """
        Search YouTube videos by query term.
        """
        
    async def get_video_details(self, video_id: str) -> dict:
        """
        Get detailed information about a specific YouTube video.
        """
        
    async def list_captions(self, video_id: str) -> list:
        """
        List available captions for a video.
        """
```

##### 6.1.1.2. Transcript Service

A service responsible for extracting and processing transcripts from YouTube videos.

```python
class TranscriptService:
    """
    Service for retrieving and processing YouTube video transcripts.
    Supports multiple retrieval methods and caching.
    """
    
    def __init__(self, youtube_client: YouTubeClient, cache_enabled: bool = True):
        self.youtube_client = youtube_client
        self.cache_enabled = cache_enabled
        
    async def get_transcript(self, video_id: str, languages: list[str] = None, debug_mode: bool = True) -> tuple[str, list[float]]:
        """
        Get transcript for a YouTube video.
        """
        
    async def process_transcript_data(self, transcript_data: list) -> tuple[str, list[float]]:
        """
        Process raw transcript data into text and timestamps.
        """
        
    async def filter_sound_indications(self, line: str) -> bool:
        """
        Filter out lines that only contain sound indications.
        """
        
    async def check_captions_availability(self, video_id: str) -> bool:
        """
        Directly check if a video has captions available via the YouTube API.
        """
```

##### 6.1.1.3. Transcript Debugger

```python
class TranscriptDebugger:
    """
    Debug helper for transcript retrieval.
    Logs and tracks detailed information about transcript retrieval processes.
    """
    
    def __init__(self, debug_enabled: bool = True):
        self.debug_enabled = debug_enabled
        self.debug_info = []
        
    def log(self, message: str) -> None:
        """
        Log a debug message if debug is enabled.
        
        Args:
            message: Debug message to log
        """
        if self.debug_enabled:
            self.debug_info.append(message)
        
    def get_log(self) -> list[str]:
        """
        Get all logged debug messages.
        
        Returns:
            List of debug messages
        """
        return self.debug_info
        
    def clear(self) -> None:
        """Clear all logged debug messages."""
        self.debug_info = []
```

#### 6.1.2. Transcript Retrieval Strategy

The transcript retrieval implementation follows a multi-layered approach:

1. **Cache Check**: First check if transcript exists in cache
2. **Direct YouTube API Check**: Check if captions exist using YouTube API
3. **Multi-language Attempt**: Try retrieving transcript in multiple languages (`['', 'en', 'en-US', 'pt', 'pt-BR', 'es']`)
4. **Fallback Messages**: If all attempts fail, return "No closed captions found. Please contact support or try a different video."

##### 6.1.2.1. Sound Filtering

Transcripts are processed to filter out sound indications like `[music]`, `[applause]`, etc., replacing them with line breaks for better readability.

### 6.2. Transcription Caching Mechanism

#### 6.2.1. Overview

This caching system is responsible for **storing original YouTube video transcriptions** (after formatting via our intelligent processing mechanism) into an in-memory cache using Python's `cachetools` library.

#### 6.2.2. Workflow

1. When a transcription is captured from YouTube, it is **processed and formatted** by our custom logic.
2. Once formatted, it is **saved into the cache**, using the **YouTube video ID** as the unique key.
3. Transcriptions are retrieved **based on video ID**, which is extracted from the video URL (e.g., `/watch?v=hGg3nWp7afg&t=639s` → `hGg3nWp7afg`).

#### 6.2.3. Implementation Details

- We use `cachetools.LRUCache` with a **maximum memory budget of 100 MB**.
- Each transcription is stored as a string (UTF-8), and average size is estimated to be ~10 KB.
- The cache **does not limit by number of entries**, but instead tracks total memory usage.
- When the 100 MB threshold is reached, the cache automatically **evicts the oldest entries first** (Least Recently Used - LRU policy).
- We **do not preload transcriptions**, even if they are popular. All entries are created **on-demand**.

#### 6.2.4. Key Characteristics

| Feature                     | Value                              |
|-----------------------------|-------------------------------------|
| Key                         | YouTube video ID (string)          |
| Value                       | Processed transcription (string)   |
| Cache type                  | `cachetools.LRUCache`              |
| Size limit                  | 100 MB total                       |
| Eviction policy             | Oldest (Least Recently Used)       |
| Preloading popular videos   | ❌ Disabled                        |

#### 6.2.5. Implementation Example

```python
from cachetools import LRUCache
import sys

# Roughly estimate size of each transcription in bytes
def estimate_size(transcription):
    return sys.getsizeof(transcription)

# Initialize cache with size in bytes
cache = LRUCache(maxsize=100 * 1024 * 1024, getsizeof=estimate_size)

def save_transcription(video_id: str, transcription: str):
    cache[video_id] = transcription

def get_transcription(video_id: str):
    return cache.get(video_id)
```

### 6.2.6. Persistent and In-Memory Caching (Expanded)

- In addition to in-memory caching with `cachetools.LRUCache`, implement persistent/disk caching for video details and transcripts:
  - Use a cache directory structure: `cache/video_details` and `cache/transcripts`.
  - Provide async methods for get/save for both in-memory and disk cache.
  - Document cache invalidation and manual clearing procedures.
  - Monitor cache usage and evictions; provide statistics for cache health.

### 6.2.7. Cache Invalidation and Monitoring

- Implement manual cache clearing endpoints or admin tools.
- Log cache evictions and errors.
- Provide metrics for cache hit/miss rates and memory usage.

### 6.3. Advanced Transcription Correction Logic

#### 6.3.1. Purpose

The transcription correction system serves as the core evaluation mechanism that:

1. Compares a user's transcription attempt against the reference transcription from YouTube
2. Identifies various types of discrepancies: exact matches, near matches (mistakes), missing words, and wrong/extra words
3. Provides word-by-word feedback that helps users improve their listening and transcription skills
4. Aligns mismatched portions to maximize the learning value of the comparison

#### 6.3.2. Core Components

##### Word Model

```python
@dataclass
class Word:
    text: str                # Original text of the word
    timestamp: float         # Timestamp from the video where the word appears
    normalized: str = ""     # Normalized form for comparison (lowercase, punctuation removed, etc.)
```

##### Transcription Comparer

```python
class TranscriptionComparerV4Pro:
    def __init__(self, mistake_threshold: float = 0.75, window_size: int = 20, max_search: int = 200):
        self.mistake_threshold = mistake_threshold  # Similarity threshold to consider a word a "mistake" vs "wrong"
        self.window_size = window_size              # Size of window for searching matches (in words)
        self.max_search = max_search                # Maximum number of words to search ahead
```

#### 6.3.3. Algorithm Operation

The comparison algorithm operates in the following stages:

1. **Direct Comparison Phase**
   - Compares words at the same position in both texts
   - Identifies exact matches and near matches (mistakes)
   - Adds them to the result with appropriate classification

2. **Realignment Phase**
   - When direct matches fail, attempts to realign the texts
   - Uses "dubles" (pairs of consecutive words) to find potential alignment points
   - Searches in windows to efficiently handle larger texts

3. **Gap Filling Phase**
   - After realignment, processes any text "gaps" between the previous position and new alignment
   - Marks words as correct, mistakes, missing, or wrong based on comparison

4. **Remaining Words Processing**
   - Processes any remaining words in either text
   - Words remaining in user text are marked as "wrong"
   - Words remaining in reference text are marked as "missing"

#### 6.3.4. Classification Types

Each word in the comparison result is classified as one of the following:

| Type | Description | Conditions |
|------|-------------|------------|
| `correct` | Perfect match | Words are equivalent (after normalization) |
| `mistake` | Minor error | Similarity ratio ≥ threshold (default: 0.75) |
| `missing` | Word from reference not in user text | Word not found in user text |
| `wrong` | Word in user text not in reference | Word not found in reference text |

#### 6.3.5. Frontend Integration

The frontend will render the comparison results with appropriate styling:
- `correct`: Green text
- `mistake`: Yellow text
- `missing`: Gray text (or strikethrough)
- `wrong`: Red text

#### 6.3.6. Learning Analytics and User Progress Tracking

The transcription correction system will include functionality to track and analyze user progress over time:

1. **Mistake Pattern Tracking**
   - Record common mistakes made by individual users
   - Categorize errors by type (e.g., homonyms, contractions, similar-sounding words)
   - Store historical transcription attempts to measure improvement
   
2. **Personalized Recommendations**
   - Generate tailored practice recommendations based on error patterns
   - Suggest videos with content that addresses specific user weaknesses
   - Provide customized tips for improvement on the most frequent error types
   
3. **Progress Visualization**
   - Display charts showing improvement over time
   - Track metrics such as overall accuracy, mistake reduction, and transcription speed
   - Compare current performance against historical averages

4. **Implementation**
   - Store user transcription results in a database with user ID, video ID, timestamp
   - Implement analysis services that process historical data to identify patterns
   - Create recommendation algorithms based on identified weaknesses

### 6.3.7. Realignment and Helper Functions

```python
def realign_with_dubles(self, user_words, user_start_idx, actual_words, actual_start_idx, result, matched_once):
    """
    Attempts to realign the transcription when direct matching fails.
    Uses "dubles" (pairs of consecutive words) to find potential alignment points.
    """
    user_new_world = user_words[user_start_idx:]
    actual_target = actual_words[actual_start_idx:]
    user_dubles = self.generate_dubles(user_new_world)
    for user_offset, duble_user in enumerate(user_dubles):
        for window_start in range(0, min(len(actual_target), self.max_search), self.window_size):
            window_end = min(window_start + self.window_size, len(actual_target))
            window = actual_target[window_start:window_end]
            target_dubles = self.generate_dubles(window)
            for target_offset, duble_target in enumerate(target_dubles):
                if self.are_dubles_equivalent(duble_user, duble_target):
                    full_target_start_idx = actual_start_idx + window_start + target_offset
                    if not matched_once and full_target_start_idx > 0:
                        for idx in range(actual_start_idx, full_target_start_idx):
                            result.append({'text': actual_words[idx].text, 'type': 'missing'})
                    self.fill_field_gaps(
                        user_words[user_start_idx:user_start_idx + user_offset],
                        actual_words[actual_start_idx:full_target_start_idx],
                        result
                    )
                    for w in duble_user:
                        result.append({'text': w.text, 'type': 'correct'})
                    return user_start_idx + user_offset + 2, full_target_start_idx + 2
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
    return user_start_idx, actual_start_idx

def generate_dubles(self, words: List[Word]) -> List[List[Word]]:
    dubles = []
    for i in range(len(words) - 1):
        dubles.append([words[i], words[i+1]])
    return dubles

def are_dubles_equivalent(self, duble1: List[Word], duble2: List[Word]) -> bool:
    return all(are_equivalent(w1.normalized, w2.normalized) for w1, w2 in zip(duble1, duble2))

def fill_field_gaps(self, user_gap: List[Word], actual_gap: List[Word], result: List[Dict[str, str]]):
    user_used = [False] * len(user_gap)
    for aw in actual_gap:
        matched = False
        for i, uw in enumerate(user_gap):
            if not user_used[i] and are_equivalent(uw.normalized, aw.normalized):
                result.append({'text': uw.text, 'type': 'correct'})
                user_used[i] = True
                matched = True
                break
        if not matched:
            for i, uw in enumerate(user_gap):
                if not user_used[i] and self.is_mistake(uw.normalized, aw.normalized):
                    result.append({'text': uw.text, 'type': 'mistake'})
                    user_used[i] = True
                    matched = True
                    break
        if not matched:
            result.append({'text': aw.text, 'type': 'missing'})
    for i, used in enumerate(user_used):
        if not used:
            result.append({'text': user_gap[i].text, 'type': 'wrong'})

def is_mistake(self, user_norm: str, actual_norm: str) -> bool:
    from difflib import SequenceMatcher
    ratio = SequenceMatcher(None, user_norm, actual_norm).ratio()
    return ratio >= self.mistake_threshold
```

### 6.3.8. Main Comparison Function

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

### 6.3.9. Required Dependencies

```python
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from difflib import SequenceMatcher
```

### 6.3.10. Performance Considerations for Transcription Correction

1. **Time Complexity**: The algorithm has O(n*m) worst-case time complexity where n is user word count and m is reference word count. The windowing approach keeps performance reasonable for most transcriptions.

2. **Memory Usage**: Memory usage scales linearly with the size of the input texts.

3. **Optimization Techniques**:
   - Window-based searching to limit comparison scope
   - Early termination of searches when matches are found
   - Caching of normalized forms and comparison results


## 7. API Endpoints

### 7.1. Video Search and Retrieval

All API endpoints should follow the consistent `/api/v1/` prefix convention for better versioning control:

```python
# GET /api/v1/videos/search?q=...
@router.get("/search", response_model=List[schemas.VideoSearchResult])
async def search_videos(
    query: str, 
    max_results: int = 10,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Search for YouTube videos by query term.
    """
    
# GET /api/v1/videos/:id
@router.get("/{video_id}", response_model=schemas.VideoDetails)
async def get_video_details(
    video_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get detailed information about a specific YouTube video.
    """
```

### 7.2. Transcript Retrieval

```python
# GET /api/v1/videos/{video_id}/transcript
@router.get("/{video_id}/transcript", response_model=schemas.VideoTranscript)
async def get_video_transcript(
    video_id: str,
    languages: Optional[List[str]] = Query(None),
    debug_mode: bool = Query(False),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get transcript for a YouTube video.
    """
```

### 7.3. Trending Videos

```python
# GET /api/v1/videos/trending
@router.get("/trending", response_model=List[schemas.VideoSearchResult])
async def get_trending_videos(
    category: Optional[str] = None,
    limit: int = Query(10, ge=1, le=50),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get trending YouTube videos, optionally filtered by category.
    
    Args:
        category: Optional category to filter trending videos
        limit: Maximum number of results to return (default: 10)
        current_user: Current authenticated user
        
    Returns:
        List of trending video results
    """
    try:
        youtube_client = get_youtube_client()
        
        # Get regionCode from user settings or default to US
        region_code = getattr(current_user, "region_code", "US")
        
        # Construct parameters for trending videos request
        trending_params = {
            "chart": "mostPopular",
            "regionCode": region_code,
            "maxResults": limit,
            "part": "snippet,contentDetails,statistics"
        }
        
        # Add category filter if provided
        if category:
            trending_params["videoCategoryId"] = category
            
        # Execute request
        trending_results = await youtube_client.list_videos(**trending_params)
        
        # Transform API response to our schema
        results = []
        for item in trending_results.get("items", []):
            snippet = item.get("snippet", {})
            results.append({
                "id": item.get("id"),
                "title": snippet.get("title"),
                "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url"),
                "channel": snippet.get("channelTitle"),
                "published_at": snippet.get("publishedAt")
            })
            
        return results
    except Exception as e:
        logger.error(f"Error fetching trending videos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch trending videos"
        )
```

### 7.4. Authentication System

All authentication endpoints should follow the `/api/v1/auth/` prefix convention for better organization and versioning control. These endpoints handle user registration, login, token management, and password resets.

```python
# POST /api/v1/auth/register
@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    Args:
        user: User registration data
        db: Database session
        
    Returns:
        The newly created user
        
    Raises:
        HTTPException: If email already exists
    """
    db_user = users_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return users_crud.create_user(db=db, user=user)

# POST /api/v1/auth/login
@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and provide access token.
    
    Args:
        form_data: OAuth2 password request form
        db: Database session
        
    Returns:
        Access token
        
    Raises:
        HTTPException: If authentication fails
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# POST /api/v1/auth/logout
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Log out the current user by invalidating their token.
    
    Note: For a complete implementation, this would add the token to a blocklist
    or implement a token invalidation strategy.
    
    Args:
        current_user: Current authenticated user
    """
    # In a real implementation, you would add the token to a blacklist
    # or implement a token invalidation strategy
    return {}

# POST /api/v1/auth/refresh
@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Refresh an existing access token.
    
    Args:
        token: Current access token
        db: Database session
        
    Returns:
        New access token
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
        
        if token_data.sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = users_crud.get_user_by_id(db, uuid.UUID(token_data.sub))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# POST /api/v1/auth/reset-password
@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(
    reset_data: schemas.PasswordReset,
    db: Session = Depends(get_db)
):
    """
    Reset user's password.
    
    Args:
        reset_data: Password reset data containing email
        db: Database session
        
    Raises:
        HTTPException: If email not found
    """
    user = users_crud.get_user_by_email(db, email=reset_data.email)
    if not user:
        # Don't leak information about registered emails
        # Still return 204 for security reasons
        return {}
    
    # In a real implementation, this would:
    # 1. Generate a password reset token
    # 2. Send an email with a reset link
    # 3. Store the token in the database with expiration
    
    # For the purpose of this specification, we'll just acknowledge the request
    return {}
```

#### 7.4.1. Authentication Data Models

```python
# schemas/users.py

class UserBase(BaseModel):
    """Base schema for user data."""
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class UserResponse(UserBase):
    """Schema for user response data."""
    id: UUID
    is_premium: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """Schema for token payload."""
    sub: Optional[str] = None
    exp: Optional[int] = None

class PasswordReset(BaseModel):
    """Schema for password reset request."""
    email: EmailStr
```

#### 7.4.2. Authentication Security Implementation

The authentication system uses JWT (JSON Web Tokens) for secure token-based authentication:

```python
# core/security.py

from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext

# Constants
ALGORITHM = "HS256"

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if plain password matches hashed password.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Get password hash.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)

def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token.
    
    Args:
        data: Token payload data
        expires_delta: Optional expiration time delta
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate user with username and password.
    
    Args:
        db: Database session
        username: Username
        password: Plain text password
        
    Returns:
        User if authentication successful, None otherwise
    """
    user = users_crud.get_user_by_username(db, username)
    
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
        
    return user
```

## 8. Comprehensive Data Models

This section defines all database models and schema representations used throughout the application. These models ensure consistent data structures across all components of the system.

### 8.1. Database Models (SQLAlchemy)

#### 8.1.1. User Model

```python
# app/db/models.py

class User(Base):
    """User database model."""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_premium = Column(Boolean, default=False)
    subscription_end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transcriptions = relationship("TranscriptionSession", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
```

#### 8.1.2. TranscriptionSession Model

```python
# app/db/models.py

class TranscriptionSession(Base):
    """TranscriptionSession database model."""
    __tablename__ = "transcription_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    video_id = Column(String, nullable=False)  # YouTube video ID
    user_transcription = Column(Text, nullable=True)
    correct_transcription = Column(Text, nullable=True)
    accuracy_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transcriptions")
```

#### 8.1.3. Subscription Model

```python
# app/db/models.py

class Subscription(Base):
    """Subscription database model."""
    __tablename__ = "subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    stripe_subscription_id = Column(String, nullable=False)
    status = Column(String, nullable=False)  # active, canceled, past_due
    plan_type = Column(String, nullable=False)  # month, year
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
```

#### 8.1.4. Video Model

```python
# app/db/models.py

class Video(Base):
    """Video database model for caching YouTube metadata."""
    __tablename__ = "videos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    youtube_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)  # Duration in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 8.2. Schema Models (Pydantic)

The schema models ensure proper data validation and serialization for API requests and responses.

#### 8.2.1. User Schemas

The user schemas defined in section 7.4.1 cover the core user-related data validation needs.

#### 8.2.2. Transcription Schemas

```python
# app/schemas/transcriptions.py

class TranscriptionBase(BaseModel):
    """Base schema for transcription data."""
    video_id: str
    user_transcription: Optional[str] = None
    correct_transcription: Optional[str] = None

class TranscriptionCreate(TranscriptionBase):
    """Schema for creating a transcription."""
    pass

class TranscriptionSession(TranscriptionBase):
    """Schema for transcription session response."""
    id: UUID
    user_id: UUID
    accuracy_score: Optional[float] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

class TranscriptionAnalysisRequest(BaseModel):
    """Schema for transcription analysis request."""
    user_text: str
    reference_text: str

class TranscriptionAnalysisItem(BaseModel):
    """Schema for a single transcription analysis item."""
    text: str
    type: str  # correct, mistake, missing, wrong

class TranscriptionAnalysisStats(BaseModel):
    """Schema for transcription analysis stats."""
    correct_words: int
    mistake_words: int
    missing_words: int
    wrong_words: int
    total_words: int

class TranscriptionAnalysis(BaseModel):
    """Schema for transcription analysis response."""
    comparison: List[TranscriptionAnalysisItem]
    overall_accuracy: float
    stats: TranscriptionAnalysisStats
```

#### 8.2.3. Subscription Schemas

```python
# app/schemas/subscriptions.py

class SubscriptionBase(BaseModel):
    """Base schema for subscription data."""
    user_id: UUID
    stripe_subscription_id: str
    status: str  # active, canceled, past_due
    plan_type: str  # month, year
    start_date: datetime
    end_date: datetime

class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a subscription."""
    pass

class Subscription(SubscriptionBase):
    """Schema for subscription response."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class SubscriptionPlanFeature(BaseModel):
    """Schema for subscription plan feature."""
    name: str
    description: Optional[str] = None

class SubscriptionPlan(BaseModel):
    """Schema for subscription plan."""
    id: str
    name: str
    description: str
    price: float
    currency: str = "USD"
    interval: str  # month, year
    features: List[str]
```

#### 8.2.4. Video Schemas

```python
# app/schemas/videos.py

class VideoBase(BaseModel):
    """Base schema for video data."""
    youtube_id: str
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None

class VideoCreate(VideoBase):
    """Schema for creating a video."""
    pass

class Video(VideoBase):
    """Schema for video response."""
    id: UUID
    created_at: datetime
    
    class Config:
        orm_mode = True

class VideoSearchResult(BaseModel):
    """Schema for YouTube video search results."""
    id: str
    title: str
    thumbnail: str
    channel: str
    published_at: datetime

class VideoDetails(BaseModel):
    """Schema for detailed YouTube video information."""
    video_id: str
    title: str
    channel: str
    description: str
    embed_url: str
    duration: str  # ISO 8601 duration format
    
class VideoTranscript(BaseModel):
    """Schema for YouTube video transcript."""
    video_id: str
    transcript: str
    timestamps: List[float]  # Start time for each word
    debug_info: Optional[List[str]] = None  # Debug information if debug_mode=True
```

### 8.3. Data Model Relationships

The data models are designed with the following relationships:

1. **User to TranscriptionSession**: One-to-Many
   - A user can have multiple transcription sessions
   - Each transcription session belongs to a single user

2. **User to Subscription**: One-to-Many
   - A user can have multiple subscriptions (historical record)
   - Each subscription belongs to a single user

3. **Video**: Independent entity
   - Used for caching YouTube video metadata
   - Referenced by TranscriptionSession via video_id

These relationships ensure proper data organization and efficient querying capabilities throughout the application.

## 9. Testing Strategy

This section outlines the comprehensive testing approach for the application, covering all components from frontend to backend, and defining methodologies for unit, integration, and end-to-end testing.

### 9.1. Frontend Testing

Frontend testing focuses on component functionality, user interaction flows, and visual consistency.

#### 9.1.1. Unit Testing with Jest and React Testing Library

All React components should be tested using Jest and React Testing Library with the following guidelines:

```javascript
// Example component test for TranscriptionInput.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TranscriptionInput from '../components/transcription/TranscriptionInput';

describe('TranscriptionInput Component', () => {
  test('renders textarea with correct placeholder', () => {
    render(<TranscriptionInput />);
    const textArea = screen.getByPlaceholderText('Type what you hear...');
    expect(textArea).toBeInTheDocument();
  });
  
  test('updates character count when typing', async () => {
    render(<TranscriptionInput />);
    const textArea = screen.getByPlaceholderText('Type what you hear...');
    await userEvent.type(textArea, 'Hello, world!');
    expect(screen.getByText('13 characters')).toBeInTheDocument();
  });
  
  test('calls onSubmit when submit button is clicked', () => {
    const handleSubmit = jest.fn();
    render(<TranscriptionInput onSubmit={handleSubmit} />);
    const submitButton = screen.getByRole('button', { name: /submit transcription/i });
    fireEvent.click(submitButton);
    expect(handleSubmit).toHaveBeenCalledTimes(1);
  });
});
```

**Test Coverage Requirements:**
- 80% minimum code coverage for all components
- 90% minimum coverage for core UI components
- 100% coverage for utility functions

#### 9.1.2. Integration Testing

Integration tests should verify the proper interaction between connected components:

```javascript
// Example integration test for transcription workflow
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TranscriptionPage from '../pages/transcribe/[videoId]';
import { TranscriptionProvider } from '../contexts/TranscriptionContext';

// Mock API responses
jest.mock('../services/api', () => ({
  getVideoTranscript: jest.fn(() => Promise.resolve({
    transcript: 'Sample reference transcription'
  })),
  analyzeTranscription: jest.fn(() => Promise.resolve({
    comparison: [/* comparison data */],
    overall_accuracy: 0.85,
    stats: {
      correct_words: 8,
      mistake_words: 1,
      missing_words: 0,
      wrong_words: 1,
      total_words: 10
    }
  }))
}));

describe('Transcription Workflow', () => {
  test('full transcription workflow from input to results', async () => {
    render(
      <TranscriptionProvider>
        <TranscriptionPage videoId="test123" />
      </TranscriptionProvider>
    );
    
    // Wait for video player to load
    await screen.findByTitle('YouTube video player');
    
    // Type transcription
    const textArea = screen.getByPlaceholderText('Type what you hear...');
    await userEvent.type(textArea, 'Sample user transcription');
    
    // Submit transcription
    const submitButton = screen.getByRole('button', { name: /submit transcription/i });
    fireEvent.click(submitButton);
    
    // Wait for results to appear
    const results = await screen.findByText('Transcription Results');
    expect(results).toBeInTheDocument();
    
    // Verify accuracy display
    expect(screen.getByText('85%')).toBeInTheDocument();
  });
});
```

#### 9.1.3. End-to-End Testing with Cypress

End-to-end tests should cover critical user flows from start to finish:

```javascript
// cypress/integration/transcription_spec.js
describe('Transcription Feature', () => {
  beforeEach(() => {
    // Mock authentication
    cy.login('testuser', 'password123');
  });
  
  it('allows a user to search for videos and start transcribing', () => {
    // Visit search page
    cy.visit('/transcribe');
    
    // Search for a video
    cy.get('[data-testid="search-input"]').type('learn english');
    cy.get('[data-testid="search-button"]').click();
    
    // Wait for search results
    cy.get('[data-testid="search-results"]').should('be.visible');
    
    // Select the first video
    cy.get('[data-testid="video-card"]').first().click();
    
    // Check that we navigate to transcription page
    cy.url().should('include', '/transcribe/');
    
    // Verify video player is present
    cy.get('iframe[title="YouTube video player"]').should('be.visible');
    
    // Verify transcription input is present
    cy.get('[data-testid="transcription-input"]').should('be.visible');
  });
  
  it('submits transcription and displays results', () => {
    // Visit a specific video transcription page
    cy.visit('/transcribe/test123');
    
    // Type a transcription
    cy.get('[data-testid="transcription-input"]')
      .type('This is a test transcription for cypress');
    
    // Submit transcription
    cy.get('[data-testid="submit-button"]').click();
    
    // Verify results appear
    cy.get('[data-testid="transcription-results"]').should('be.visible');
    
    // Click try again
    cy.get('[data-testid="try-again-button"]').click();
    
    // Verify input has previous text
    cy.get('[data-testid="transcription-input"]')
      .should('have.value', 'This is a test transcription for cypress');
  });
});
```

**End-to-End Test Scenarios:**
1. User registration and login flow
2. Video search and selection
3. Complete transcription workflow
4. Subscription purchase flow
5. User settings management

### 9.2. Backend Testing

Backend testing focuses on API functionality, business logic, and database operations.

#### 9.2.1. Unit Testing with pytest

All backend functions should have unit tests covering normal operation, edge cases, and error handling:

```python
# tests/test_transcription_service.py
import pytest
from unittest.mock import MagicMock, patch
from app.services.transcription import compare_transcriptions

def test_compare_transcriptions_perfect_match():
    """Test comparison with perfectly matching transcriptions."""
    user_text = "this is a test"
    reference_text = "this is a test"
    
    result = compare_transcriptions(user_text, reference_text)
    
    assert result == 1.0

def test_compare_transcriptions_partial_match():
    """Test comparison with partially matching transcriptions."""
    user_text = "this is a tost"  # Intentional typo
    reference_text = "this is a test"
    
    result = compare_transcriptions(user_text, reference_text)
    
    assert 0.7 <= result < 1.0

def test_compare_transcriptions_no_match():
    """Test comparison with non-matching transcriptions."""
    user_text = "completely different text"
    reference_text = "this is a test"
    
    result = compare_transcriptions(user_text, reference_text)
    
    assert result < 0.5

@patch('app.services.transcription.TranscriptionComparerV4Pro')
def test_compare_transcriptions_detailed(mock_comparer):
    """Test detailed comparison with mocked comparer."""
    # Setup mock comparer
    mock_instance = MagicMock()
    mock_instance.compare.return_value = [
        {'text': 'this', 'type': 'correct'},
        {'text': 'is', 'type': 'correct'},
        {'text': 'a', 'type': 'correct'},
        {'text': 'tost', 'type': 'mistake'}
    ]
    mock_comparer.return_value = mock_instance
    
    # Call function
    from app.services.transcription import get_detailed_comparison
    result = get_detailed_comparison("this is a tost", "this is a test")
    
    # Assert
    assert len(result) == 4
    assert result[0]['text'] == 'this'
    assert result[0]['type'] == 'correct'
    assert result[3]['text'] == 'tost'
    assert result[3]['type'] == 'mistake'
```

#### 9.2.2. API Testing with FastAPI TestClient

API endpoints should be tested to ensure they return correct responses and handle errors appropriately:

```python
# tests/test_transcriptions_api.py
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.db.models import User, TranscriptionSession
from app.core.security import create_access_token

client = TestClient(app)

def test_create_transcription(db_session: Session, test_user: User):
    """Test creating a new transcription session."""
    # Create access token for test user
    access_token = create_access_token(data={"sub": str(test_user.id)})
    
    # Test data
    transcription_data = {
        "video_id": "test123",
        "user_transcription": "This is a test transcription",
        "correct_transcription": "This is a test transcription"
    }
    
    # Make request
    response = client.post(
        "/api/v1/transcriptions/",
        json=transcription_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["video_id"] == "test123"
    assert data["user_id"] == str(test_user.id)
    assert data["accuracy_score"] > 0.9  # Should be high for matching text
    
    # Verify database entry
    db_transcription = db_session.query(TranscriptionSession).filter_by(id=data["id"]).first()
    assert db_transcription is not None
    assert db_transcription.video_id == "test123"
```

#### 9.2.3. Integration Testing with Databases

Database operations should be tested using test databases or in-memory SQLite:

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.database import get_db
from app.main import app
from app.db.models import User
from app.core.security import get_password_hash

@pytest.fixture(scope="function")
def test_db():
    """Create test database."""
    # Use in-memory SQLite for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Dependency override
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal
    
    # Clean up
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db):
    """Get database session."""
    session = test_db()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_user(db_session):
    """Create test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        is_premium=False
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
```

### 9.3. Performance Testing

Performance testing ensures the application meets response time and throughput requirements.

#### 9.3.1. Load Testing with Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """Log in before tests."""
        response = self.client.post("/api/v1/auth/login", {
            "username": "testuser",
            "password": "password123"
        })
        self.token = response.json()["access_token"]
        self.client.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(1)
    def index_page(self):
        """Test homepage."""
        self.client.get("/")
    
    @task(2)
    def search_videos(self):
        """Test video search."""
        self.client.get("/api/v1/videos/search?q=english%20lesson")
    
    @task(3)
    def get_video_transcript(self):
        """Test transcript retrieval."""
        self.client.get("/api/v1/videos/test123/transcript")
    
    @task(1)
    def analyze_transcription(self):
        """Test transcription analysis."""
        self.client.post("/api/v1/transcriptions/analyze", json={
            "user_text": "This is a test transcription",
            "reference_text": "This is a test transcription"
        })
```

**Performance Targets:**
- API response time: < 500ms for 95% of requests
- Page load time: < 2 seconds
- Support for 1000+ concurrent users

### 9.4. Security Testing

Security testing safeguards user data and protects against common vulnerabilities.

#### 9.4.1. Authentication Testing

```python
# tests/test_auth_security.py
from fastapi.testclient import TestClient
import pytest

from app.main import app

client = TestClient(app)

def test_access_protected_route_without_token():
    """Test accessing protected route without token."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401

def test_access_protected_route_with_invalid_token():
    """Test accessing protected route with invalid token."""
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401

def test_password_reset_does_not_leak_email_existence():
    """Test password reset does not leak if email exists or not."""
    # Test with non-existent email
    response = client.post(
        "/api/v1/auth/reset-password",
        json={"email": "nonexistent@example.com"}
    )
    # Should still return 204 No Content for security
    assert response.status_code == 204
```

#### 9.4.2. Rate Limiting Testing

```python
# tests/test_rate_limiting.py
from fastapi.testclient import TestClient
import time

from app.main import app

client = TestClient(app)

def test_login_rate_limiting():
    """Test rate limiting on login endpoint."""
    # Send multiple login requests in quick succession
    for i in range(10):
        client.post(
            "/api/v1/auth/login",
            data={"username": f"test{i}", "password": "wrong_password"}
        )
    
    # Next request should be rate limited
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test", "password": "password"}
    )
    
    assert response.status_code == 429  # Too Many Requests
```

### 9.5. Testing Automation

All tests should be integrated into CI/CD pipelines to ensure code quality and prevent regressions.

#### 9.5.1. GitHub Actions Configuration

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements/dev.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
        with:
          file: ./backend/coverage.xml
  
  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v2
        with:
          file: ./frontend/coverage/lcov.info
```

_This document supersedes all prior ad-hoc instructions for the transcription workflow. All future work must comply fully with this specification._ 

## 10. Deployment Considerations

This application should follow the Docker deployment practices outlined in `ai_docs/3_expl_Docker.md` with these application-specific configurations:
- Environment separation (dev/test/prod) with appropriate database connections
- Elasticsearch indexes for dev and prod environments
- Custom startup scripts for database migrations

## 11. Theme System Implementation

Implementation should follow theme specifications in `frontend-update.md`.

## 12. Compliance Requirements

- Implement GDPR and CCPA compliance with data minimization and explicit user consent
- Document policies in privacy policy
- Implement data access and deletion rights
- Set up security logging for breach detection

## 13. UI Layout System and Grid Specifications

Implementation should follow the grid system defined in `frontend-update.md`.

## 14. Project Structure Alignment

File organization should follow patterns defined in `project-directory-and-file-structure.md`.

## 15. Additional Implementation Guidelines

### 15.1. Code Documentation and Organization

- **Module Documentation**: For any code module created, include complete documentation of the requirements this module fulfills in comments at the top of the file.
- **File Size Limits**: Strictly maintain files under 200-300 lines of code. Refactor when approaching these limits.
- **Scripting Practices**: Avoid writing scripts in files whenever possible, especially if the script is likely to be run only once.
- **Environment Variables**: NEVER overwrite any .env file without first asking and confirming with the project owner.

### 15.2. Change Management

- **Changelog Updates**: All changes implemented must be documented in `progress-tracking/CHANGELOG.md`.
- **Implementation Scope**: DO NOT touch code that is unrelated to the task at hand.
- **Technology Introduction**: When fixing an issue or bug, DO NOT introduce a new pattern or technology without first exhausting all other options for the existing implementation. If a new pattern must be introduced, REMOVE the old implementation to avoid duplicate logic.

### 15.3. Testing Requirements

- **Test Framework**: Implement Pytest with mocked data for all backend components.
- **Test Coverage**: Ensure tests cover all requirements specified in the application.
- **Mocking Data**: Mocking data is ONLY permitted for tests, NEVER for dev or prod environments.
- **Stubbing Practices**: Never add stubbing or fake data patterns to code that affects the dev or prod environments.

### 15.4. Environment Considerations

- **Environment Awareness**: All code must take into account the different environments: dev, test, and prod.
- **Elasticsearch Indexes**: Ensure Elasticsearch configurations include separate dev and prod indexes.

All implementation work must adhere to these guidelines in addition to the detailed specifications in previous sections. 

## 16. Conclusion

This specification provides a comprehensive, unified guide for the design, implementation, and compliance of the transcription workflow application. All requirements, technical details, and best practices are integrated to ensure a robust, scalable, and maintainable system. Future work and all development must adhere strictly to this document, with any changes tracked in the project changelog. For questions or clarifications, refer to the relevant section or contact the project owner.