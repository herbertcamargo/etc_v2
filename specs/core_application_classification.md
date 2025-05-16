# Core Application Specification Classification

## Purpose of this Document

This document serves as an implementation companion to [specs/spec_core_application.md](specs/spec_core_application.md). While the main specification provides comprehensive requirements, this document:

1. **Categorizes components** into Frontend and Backend domains for clearer team assignment
2. **Organizes implementation details** according to architectural layers
3. **Highlights integration points** between frontend and backend systems
4. **Maps specifications** to the established project standards and existing design documents

All information is derived directly from the Core Transcription Application specification with no additional requirements added. Development teams should use this document alongside the main specification for efficient implementation planning.

## Frontend Components

### 1. Page Structure and Routing
- **Routes**: `/transcribe` and `/transcribe/:videoId`
- **Component Architecture**:
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
- **Reference**: Section 2.2 of spec_core_application.md

### 2. UI/UX Design
- **Design Principles**: Minimalist UI with whitespace, clear hierarchy, subtle animations
- **Color Palette**: Follows the refined palette from frontend-update.md
- **Accessibility**: Semantic HTML, ARIA attributes, keyboard navigation, contrast ratios
- **Reference**: Section 3.1 of spec_core_application.md

### 3. Key UI Components

#### 3.1. YouTube Search Bar
- Large input with floating label
- Gradient "Search" button
- Keyboard accessibility features
- **Reference**: Section 3.2 of spec_core_application.md

#### 3.2. Search Results
- 4x3 responsive grid of video results
- Result cards with thumbnails and metadata
- User authentication check before navigation
- **Reference**: Section 3.2 of spec_core_application.md

#### 3.3. Video Player
- Responsive embedded YouTube iframe
- Error handling for unsupported videos
- Page scroll anchoring
- **Reference**: Section 3.2 of spec_core_application.md

#### 3.4. Transcription Input
- Multi-line textarea with floating label
- Character/word count
- Auto-save functionality
- Previous attempt retention on "Try Again"
- **Reference**: Section 3.2 of spec_core_application.md

#### 3.5. Button Set
- **Pause Delay Dropdown**:
  - Options: 0, 1, 2, 3, 5 seconds
  - Default: 2 seconds
  - Tooltip: "Sets how long the video remains paused after you stop typing"

- **Rewind Time Dropdown**:
  - Options: 0.0, 0.25, 0.5, 0.75, 1, 2, 3, 5 seconds
  - Default: 2 seconds
  - Tooltip: "Controls how far back the video rewinds after pausing"

- **Rewind Button**:
  - Label: "Rewind"
  - Action: Rewind by selected time
  - Tooltip: "Rewinds the video by the selected time amount"

- **Play/Stop Button**:
  - State-based appearance (Play/Stop)
  - Color coding: dark green/dark red
  - Tooltip: "Play or pause the video playback"

- **Submit Transcription Button**:
  - State-based appearance (Submit/Try Again)
  - Color coding: dark yellow/dark amber
  - Tooltip: Changes based on current state
- **Reference**: Section 4 of spec_core_application.md

#### 3.6. Results Output
- Titled "Transcription Results" box
- Animated transitions with fade-in
- Highlighting effect for new results
- Smooth scroll to results section
- Accessibility considerations for animations
- **Reference**: Section 3.2 of spec_core_application.md

### 4. Frontend Logic & State Management
- React Context API for global state
- Local state for transient UI elements
- Loading and error feedback for all actions
- Debounced YouTube search requests
- **Reference**: Section 5 of spec_core_application.md

#### 4.1. Loading and Error Feedback
- Consistent spinner component
- Inline error messages
- Toast notifications for transient errors
- Logging of errors to monitoring system
- **Reference**: Section 5.1 of spec_core_application.md

#### 4.2. Auto-save Draft Implementation
- LocalStorage with unique keys per video
- SessionStorage fallback
- Save triggers after inactivity, navigation, and submission
- Restoration notification and functionality
- **Reference**: Section 5.2 of spec_core_application.md

#### 4.3. Animated Transitions
- 300ms fade-in transition
- Highlight effect for new results
- Smooth scrolling behavior
- Respect for reduced motion preferences
- **Reference**: Section 3.2 of spec_core_application.md

## Backend Components

### 1. YouTube Video Service

#### 1.1. YouTube API Client
```python
class YouTubeClient:
    """
    Client for interacting with YouTube Data API v3.
    Handles authentication, video searching, and metadata retrieval.
    """
    
    # Methods for:
    # - Client authentication
    # - Video search
    # - Video details
    # - Caption listing
```
- **Reference**: Section 6.1.1 of spec_core_application.md

#### 1.2. Transcript Service
```python
class TranscriptService:
    """
    Service for retrieving and processing YouTube video transcripts.
    Supports multiple retrieval methods and caching.
    """
    
    # Methods for:
    # - Transcript retrieval
    # - Transcript processing
    # - Sound indication filtering
    # - Caption availability checking
```
- **Reference**: Section 6.1.1 of spec_core_application.md

#### 1.3. Transcript Debugger
```python
class TranscriptDebugger:
    """
    Debug helper for transcript retrieval.
    Logs detailed information about transcript processes.
    """
    
    # Methods for:
    # - Logging debug messages
    # - Retrieving and clearing logs
```
- **Reference**: Section 6.1.1 of spec_core_application.md

### 2. Transcription Caching System

#### 2.1. In-Memory Caching
- LRUCache implementation with 100MB limit
- Memory usage monitoring
- Size estimation for transcriptions
- Key-based retrieval with YouTube IDs

```python
from cachetools import LRUCache
import sys

def estimate_size(transcription):
    return sys.getsizeof(transcription)

cache = LRUCache(maxsize=100 * 1024 * 1024, getsizeof=estimate_size)

def save_transcription(video_id: str, transcription: str):
    cache[video_id] = transcription

def get_transcription(video_id: str):
    return cache.get(video_id)
```
- **Reference**: Section 6.2 of spec_core_application.md

#### 2.2. Persistent Caching
- Disk caching for video details and transcripts
- Directory structure: `cache/video_details` and `cache/transcripts`
- Async methods for get/save operations
- Cache invalidation and monitoring
- **Reference**: Section 6.2.6 of spec_core_application.md

### 3. Transcription Correction Logic

#### 3.1. Word Model
```python
@dataclass
class Word:
    text: str                # Original text
    timestamp: float         # Video timestamp
    normalized: str = ""     # Normalized form
```
- **Reference**: Section 6.3.2 of spec_core_application.md

#### 3.2. Transcription Comparer
```python
class TranscriptionComparerV4Pro:
    """
    Advanced comparer for transcription texts with
    sophisticated word matching and alignment algorithms.
    """
    
    # Methods for:
    # - Direct word comparison
    # - Realignment with "dubles"
    # - Gap filling
    # - Result classification
```
- **Reference**: Section 6.3.2 of spec_core_application.md

#### 3.3. Comparison Classification Types
- `correct`: Perfect match
- `mistake`: Minor error (similarity ratio ≥ threshold)
- `missing`: Word from reference not in user text
- `wrong`: Word in user text not in reference
- **Reference**: Section 6.3.4 of spec_core_application.md

#### 3.4. Learning Analytics
- Mistake pattern tracking
- Personalized recommendations
- Progress visualization
- Historical data analysis
- **Reference**: Section 6.3.6 of spec_core_application.md

### 4. API Endpoints

#### 4.1. Video Search and Retrieval
```python
# GET /api/v1/videos/search?q=...
@router.get("/search", response_model=List[schemas.VideoSearchResult])
async def search_videos(query: str, max_results: int = 10)

# GET /api/v1/videos/:id
@router.get("/{video_id}", response_model=schemas.VideoDetails)
async def get_video_details(video_id: str)
```
- **Reference**: Section 7.1 of spec_core_application.md

#### 4.2. Transcript Retrieval
```python
# GET /api/v1/videos/{video_id}/transcript
@router.get("/{video_id}/transcript", response_model=schemas.VideoTranscript)
async def get_video_transcript(
    video_id: str,
    languages: Optional[List[str]] = Query(None),
    debug_mode: bool = Query(False)
)
```
- **Reference**: Section 7.2 of spec_core_application.md

#### 4.3. Transcription Analysis
```python
# POST /api/v1/transcriptions/analyze
@router.post("/analyze", response_model=schemas.TranscriptionAnalysis)
async def analyze_transcription(request: schemas.TranscriptionAnalysisRequest)
```
- **Reference**: Section 7.3 of spec_core_application.md

### 5. Data Schemas

#### 5.1. Video Schemas
```python
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
- **Reference**: Section 6.3 of spec_core_application.md

## Integration Considerations

1. **Tech Stack Alignment**
   - Frontend: Follows HTML/JS requirements from tech-stack.mdc
   - Backend: Implements Python with FastAPI as specified
   - Database: Uses SQL (PostgreSQL) as required, not JSON file storage
   - Search: Leverages Elasticsearch via elastic.co for both dev and prod environments
   - **Reference**: application-requirements.md, tech-stack.mdc

2. **Coding Preferences**
   - Simple solutions preferred over complex ones
   - Code duplication avoided by reusing components
   - Support for dev/test/prod environments
   - Clean, organized codebase structure
   - File size limits respected (<300 lines)
   - **Reference**: coding-preferences.mdc

3. **Workflow Preferences**
   - Focus on relevant code areas
   - Thorough tests implemented for all functionality
   - Changes respect existing patterns and architecture
   - Side effects of changes considered
   - **Reference**: workflow-preferences.mdc

## Implementation Path

This classification supports the implementation plan outlined in implementation-plan.md:

1. **Phase 2, Step 3**: Video Search and Playback (Frontend components: YouTube Search, Search Results, Video Player)
2. **Phase 2, Step 4**: Transcription System (Backend components: Transcript Service, Transcription Correction Logic)
3. **Phase 3, Step 5**: Testing & Refinement (All components, with emphasis on integration points)

The classification is aligned with the project directory structure defined in project-directory-and-file-structure.md, particularly:

- Frontend: `frontend/src/components/video/` and `frontend/src/components/transcription/`
- Backend: `backend/app/services/youtube.py` and `backend/app/services/transcription.py` 