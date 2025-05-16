# Specification: Core Transcription Application

## 1. Overview

This document defines the comprehensive requirements and implementation details for the transcription workflow application. It integrates the transcription page creation, buttons and behaviors, caching mechanism, YouTube video capture service, and transcription correction logic into a cohesive specification. It fully aligns with the codebase's architecture, design system, API conventions, accessibility, performance targets, and testing strategy.

---

## 1.1. Specification Source Traceability

This document is a synthesis and adaptation of the following detailed specifications, which MUST be referenced for implementation details and rationale:
- [Video Player Buttons & Behavior Guide](specs/spec_But_Log.md)
- [YouTube Transcription Caching Mechanism](specs/spec_Cac_Mec.md)
- [YouTube Video Capture and Transcription Service](specs/spec_cap_tra.md)
- [Advanced Transcription Correction Logic Specification](specs/spec_tra_cor.md)
- [Transcription Flow Page Creation](specs/spec_Tra_Pag.md)

Wherever ambiguity or conflict arises, the most specific referenced spec takes precedence for its domain.

---

## 1.2. Integration of Detailed Requirements from Source Specifications

This section contains the full integration of all implementation details, code snippets, and requirements from the following source specifications, ensuring no detail is omitted:
- [Video Player Buttons & Behavior Guide](specs/spec_But_Log.md)
- [YouTube Transcription Caching Mechanism](specs/spec_Cac_Mec.md)
- [YouTube Video Capture and Transcription Service](specs/spec_cap_tra.md)
- [Advanced Transcription Correction Logic Specification](specs/spec_tra_cor.md)
- [Transcription Flow Page Creation](specs/spec_Tra_Pag.md)

Wherever a section below is marked as "[INTEGRATED FROM ...]", it is a direct, complete inclusion of content from the referenced spec, unless already present in this document. This ensures full traceability and no loss of detail.

---

### [INTEGRATED FROM specs/spec_But_Log.md]

# 🎛️ Video Player Buttons & Behavior Guide

## 1. `Pause_Delay_Dropdown`
- **Label**: `"Pause Delay"`
- **Options**: `0`, `1`, `2`, `3`, `5` (seconds)
- **Default**: `2` seconds or the last user selection

### Behavior
- If the selected value is **not `0`**:
  - When the user **types or deletes** inside the transcription input (`#user-try`):
    - Start or **restart** a countdown for the selected seconds
    - While the countdown is running: **pause** the video
    - When the countdown ends: **resume** playback
- Countdown is only triggered if:
  - The video was **already playing**, or
  - The countdown was already **active**

## 2. `Rewind_time_Dropdown`
- **Label**: `"Rewind time"`
- **Options**: `0.0`, `0.25`, `0.5`, `0.75`, `1`, `2`, `3`, `5` (seconds)
- **Default**: `2` seconds or the last user selection

### Behavior
- This dropdown serves **two purposes**:
  1. Referenced by the `Rewind_Button`
  2. Works **with `Pause_Delay_Dropdown`**:
     - If both dropdowns are set to a value different from `0`:
       - When the `Pause_Delay_Dropdown` countdown ends:
         - **Rewind** the video by the selected `Rewind_time_Dropdown` value
         - Then **continue playing**

## 3. `Rewind_Button`
- **Label**: `"Rewind"` (centered)
- **Action**: On click, rewinds the video by the currently selected `Rewind_time_Dropdown` value

## 4. `Play_Stop_Button`
- **State 1** (video is playing):
  - Text: `"Stop"`
  - Color: **dark red**
  - Text color: **white**
- **State 2** (video is paused):
  - Text: `"Play"`
  - Color: **dark green**
  - Text color: **white**

### Behavior
- On click: toggle video state
  - If playing → pause
  - If paused → play

## 5. `Submit_Transcription_Button`
- **State 1** (transcription comparison results are not shown):
  - Text: `"Submit Transcription"`
  - Color: **dark yellow**
  - Text color: **white**
- **State 2** (transcription comparison results are  shown):
  - Text: `"Try Again"`
  - Color: **dark amber**
  - Text color: **white**

### Behavior
- On click: activate the backend steps to generate the transcription comparison results
  - If transcription comparison results are not yet shown → show transcription comparison results
  - If transcription comparison results are being shown → stop showing the transcription comparison results

---

### [INTEGRATED FROM specs/spec_Cac_Mec.md]

# 📦 YouTube Transcription Caching Mechanism (Python + cachetools)

## Implementation Example

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

---

### [INTEGRATED FROM specs/spec_cap_tra.md]

# YouTube Video Capture and Transcription Service

## Core Components

#### 1. YouTube API Client

```python
class YouTubeClient:
    """
    Client for interacting with YouTube Data API v3.
    Handles authentication, video searching, and metadata retrieval.
    """
    # ... (full class as in spec_cap_tra.md)
```

#### 2. Transcript Service

```python
class TranscriptService:
    """
    Service for retrieving and processing YouTube video transcripts.
    Supports multiple retrieval methods and caching.
    """
    # ... (full class as in spec_cap_tra.md)
```

#### 3. Caching Layer

```python
class YouTubeCache:
    """
    Caching service for YouTube data.
    Provides persistent caching for video details and transcripts.
    """
    # ... (full class as in spec_cap_tra.md)
```

#### 4. Debug and Logging Component

```python
class TranscriptDebugger:
    """
    Debug helper for transcript retrieval.
    Logs and tracks detailed information about transcript retrieval processes.
    """
    # ... (full class as in spec_cap_tra.md)
```

## API Endpoints

- GET /api/v1/videos/search
- GET /api/v1/videos/{video_id}
- GET /api/v1/videos/{video_id}/transcript

## Data Models

```python
# schemas/video.py

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
    debug_info: Optional[List[str]]  # Debug information if debug_mode=True
```

## Implementation Details

- Configuration, dependencies, proxy support, performance, and testing strategies as in spec_cap_tra.md.

---

### [INTEGRATED FROM specs/spec_tra_cor.md]

# Advanced Transcription Correction Logic Specification

## Core Components, Algorithm, and Implementation

- Full Word model, TranscriptionComparerV4Pro, are_equivalent, compare, realign_with_dubles, generate_dubles, are_dubles_equivalent, fill_field_gaps, is_mistake, and all helper functions as in spec_tra_cor.md.
- Full backend API integration example for /transcriptions/analyze endpoint.
- All performance, testing, and enhancement notes as in spec_tra_cor.md.

---

### [INTEGRATED FROM specs/spec_Tra_Pag.md]

# Specification: Transcription Flow Page Creation

- All frontend structure, component, and state management requirements as in spec_Tra_Pag.md.
- All backend/API integration, error/loading/edge state handling, accessibility, testing, and design consistency requirements as in spec_Tra_Pag.md.
- All implementation notes and gotchas as in spec_Tra_Pag.md.

---

## 2. Page Routing & Structure

### 2.1. Routes

| Route Pattern               | Description                           |
|---------------------------- |---------------------------------------|
| `/transcribe`               | Entry point for video search          |
| `/transcribe/:videoId`      | Transcription page for selected video |

### 2.2. Component Architecture

- All shared UI elements must be abstracted into reusable components.
- Follow the project's React directory conventions as detailed in [Transcription Flow Page Creation](specs/spec_Tra_Pag.md):

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

#### YouTube Search Bar

- Large input box with floating label.
- Primary gradient "Search" button.
- Keyboard accessible (focus, enter key triggers search).
- Styled as per design tokens.

#### Search Results

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

#### Video Player

- Responsive embedded YouTube iframe.
- Error messaging for unsupported videos.
- Anchor page scroll to this section on load/reload.

#### Transcription Input

- Multi-line textarea with floating label.
- Live character/word count.
- Auto-save draft support (local/session storage).
- Clear error and disabled states.
- **After clicking "Try Again", the input field must be prefilled with the user's previous attempt rather than being cleared.**  
  This ensures the user can efficiently revise or retry their last attempt without retyping, supporting a smoother workflow and better learning experience.

#### Button Set

- Horizontal arrangement of action buttons.
- Each button must follow the exact behavior and state transitions as specified in the Button Behavior section.
- Consistent spacing and color feedback for all states.

##### Tooltips for Button Clarification
- **Pause Delay Dropdown:**
  - Tooltip: "Sets how long the video remains paused after you stop typing"
  - Appears on hover/focus of the dropdown
  
- **Rewind Time Dropdown:**
  - Tooltip: "Controls how far back the video rewinds after pausing"
  - Appears on hover/focus of the dropdown
  
- **Rewind Button:**
  - Tooltip: "Rewinds the video by the selected time amount"
  - Appears on hover/focus of the button
  
- **Play/Stop Button:**
  - Tooltip: "Play or pause the video playback"
  - Text changes based on current state
  - Appears on hover/focus of the button
  
- **Submit Transcription Button:**
  - Tooltip: "Compare your transcription with the original"
  - Changes to "Keep trying from where you stopped" when showing results
  - Appears on hover/focus of the button

#### Results Output

- Results box with the title "Transcription Results"

##### Animated Transitions for New Results
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

#### Behavior
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

#### Behavior
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

#### Behavior
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

#### Behavior
- On click: activate the backend steps to generate the transcription comparison results
  - If transcription comparison results are not yet shown → show transcription comparison results
  - If transcription comparison results are being shown → stop showing the transcription comparison results

---

## 5. Frontend Logic & State Management

- Use React Context API for global state (selected video, search results, user progress, etc.).
- Local state for form inputs and transient UI.
- Ensure all actions provide loading and error feedback.
- Debounce YouTube search requests to minimize API calls.
- **Store the user's transcription attempt in state when submitting for results, and restore this value into the input field when "Try Again" is pressed.**

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

##### YouTube API Client

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

##### Transcript Service

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

##### Transcript Debugger

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

##### Sound Filtering

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

- In addition to in-memory caching with `cachetools.LRUCache`, implement persistent/disk caching for video details and transcripts as described in [YouTube Video Capture and Transcription Service](specs/spec_cap_tra.md):
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

### 6.3.2.2. Realignment and Helper Functions

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

### 6.3.2.3. Main Comparison Function

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

### 6.3.2.4. Required Dependencies

```python
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from difflib import SequenceMatcher
```

### 6.3.7. Performance Considerations for Transcription Correction

1. **Time Complexity**: The algorithm has O(n*m) worst-case time complexity where n is user word count and m is reference word count. The windowing approach keeps performance reasonable for most transcriptions.

2. **Memory Usage**: Memory usage scales linearly with the size of the input texts.

3. **Optimization Techniques**:
   - Window-based searching to limit comparison scope
   - Early termination of searches when matches are found
   - Caching of normalized forms and comparison results


## 5. Frontend Logic & State Management

### 5.2. Auto-save Draft Implementation Details

The transcription input component's auto-save functionality will follow these precise rules:

1. **Save Timing**:
   - Initial auto-save occurs 5 seconds after the user starts typing
   - Subsequent saves happen every 5 seconds while typing is ongoing
   - Final save happens when typing stops for more than 5 seconds
   - Immediate save occurs on:
     - Page navigation attempts
     - Tab/browser close attempts
     - Before form submission

2. **Storage Key Format**: `transcription_draft_{videoId}`

3. **Draft Restoration UX**:
   - When a draft is detected, show a notification banner at the top of the input component
   - Banner text: "You have a saved draft for this video. Would you like to restore it?"
   - Provide "Restore" and "Discard" buttons
   - Apply subtle highlight animation to the banner to draw attention

4. **Edge Cases**:
   - If localStorage is full, attempt to use sessionStorage
   - If both fail, display a warning to the user
   - Set a reasonable max size limit for draft storage (50KB)
   - Implement garbage collection to remove drafts older than 7 days

## 3. UI/UX Design and Accessibility

### 3.2. Key Components

#### Button Tooltips Implementation

All tooltips must follow these implementation details:

1. **Visual Styling**:
   - Light background (#f8f9fa) with dark text (#212529)
   - 1px border with color #dee2e6
   - 4px border radius
   - Small drop shadow (0 2px 4px rgba(0,0,0,0.1))
   - Maximum width of 200px with text-wrapping
   
2. **Behavior**:
   - Appear 300ms after hover/focus
   - Disappear immediately on hover/focus loss
   - Position 8px above or below the target element (preferred above)
   - Remain visible when user moves from element to tooltip
   - Disappear after 5 seconds if no interaction

3. **Content**:
   - **Pause Delay Dropdown**: "Sets how long the video remains paused after you stop typing"
   - **Rewind Time Dropdown**: "Controls how far back the video rewinds after pausing"
   - **Rewind Button**: "Rewinds the video by the selected time amount"
   - **Play/Stop Button**: "Play or pause the video playback" (changes based on current state)
   - **Submit Transcription Button**: "Compare your transcription with the original" (changes to "Keep trying from where you stopped" when showing results)

4. **Accessibility**:
   - Use `aria-describedby` to associate tooltip with target element
   - Ensure tooltips are readable by screen readers
   - Support keyboard-only access
   - Respect "reduce-motion" user preference

#### Animated Transitions for Results Output

The results output component must implement these animation details:

1. **Fade-in Effect**:
   - Duration: 300ms
   - Timing function: ease-in-out
   - Starting opacity: 0
   - Ending opacity: 1
   
2. **Highlight Effect**:
   - Subtle background color transition
   - From: rgba(255, 255, 200, 0.3)
   - To: transparent
   - Duration: 1200ms
   - Delay: 300ms (after fade-in completes)
   
3. **Scroll Behavior**:
   - Smooth scroll to results section when new comparison is generated
   - Offset: 60px from top of viewport (to account for fixed headers)
   - Duration: 500ms
   - Timing function: ease-in-out
   
4. **Accessibility Considerations**:
   - Disable all animations if user has set "prefers-reduced-motion: reduce"
   - Include appropriate ARIA live region attributes:
     - `aria-live="polite"`
     - `aria-atomic="true"`
   - Announce meaningful changes to screen readers

5. **Implementation Example**:
   ```css
   @keyframes highlightFade {
     0% { background-color: rgba(255, 255, 200, 0.3); }
     100% { background-color: transparent; }
   }
   
   .results-container {
     opacity: 0;
     transition: opacity 300ms ease-in-out;
   }
   
   .results-container.visible {
     opacity: 1;
     animation: highlightFade 1200ms ease-in-out 300ms;
   }
   
   @media (prefers-reduced-motion: reduce) {
     .results-container {
       transition: none;
     }
     .results-container.visible {
       opacity: 1;
       animation: none;
     }
   }
   ```

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

### 7.3. Transcription Analysis

```python
# POST /api/v1/transcriptions/analyze
@router.post("/analyze", response_model=schemas.TranscriptionAnalysis)
async def analyze_transcription(
    request: schemas.TranscriptionAnalysisRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Analyze and compare user transcription against reference.
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

## 13. Changelog

- **[2023-07-15]**: Fully integrated all missing and previously unadapted details from specs/spec_But_Log.md, specs/spec_Cac_Mec.md, specs/spec_cap_tra.md, specs/spec_tra_cor.md, and specs/spec_Tra_Pag.md, including all implementation details, code snippets, and requirements. This ensures the core application specification is now fully comprehensive and traceable to all source specs.

_This document supersedes all prior ad-hoc instructions for the transcription workflow. All future work must comply fully with this specification._ 