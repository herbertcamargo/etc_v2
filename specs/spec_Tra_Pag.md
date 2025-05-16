# Specification: Transcription Flow Page Creation

## 1. Overview

This document defines the requirements and implementation details for creating the transcription workflow pages within the project. It fully aligns with the codebase’s architecture, design system, API conventions, accessibility, performance targets, and testing strategy.

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
- Buttons implement logic defined in `para-incluir_Transcription_Botoes_Logic.md`.
- Each button must follow the exact behavior and state transitions as specified in this document.
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

## 4. Frontend Logic & State Management

- Use React Context API for global state (selected video, search results, user progress, etc.).
- Local state for form inputs and transient UI.
- Ensure all actions provide loading and error feedback.
- Debounce YouTube search requests to minimize API calls.
- **Store the user's transcription attempt in state when submitting for results, and restore this value into the input field when "Try Again" is pressed.**

### 4.1. Loading and Error Feedback

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

---

## 5. Backend/API Integration

### 5.1. Endpoints

- Search: `GET /api/videos/search?q=...`
- Video details: `GET /api/videos/:id`
- Submit transcription: `POST /api/transcriptions`
- Fetch transcription: `GET /api/transcriptions/:id`

### 5.2. Data Handling

- Validate user authentication and subscription status before allowing transcription submission.
- Only include videos that are embeddable via YouTube iFrame API.
- Handle all backend errors gracefully in the frontend.
- Transcript capture/processing must be implemented according to `para-incluir_Captura_Transcr_Originais.md`.
- Implement transcription caching as specified in `para-incluir_Cache_Logic-Incluir_Captura.md`.
- Apply correction logic for transcription comparison as detailed in `para-incluir_Transcription_Correction_Logic_Python.md`.

---

## 6. Error, Loading & Edge State Handling

- All async actions must display loading indicators as specified in section 4.1.
- Show user-friendly error messages for API/network problems.
- Fallback UI for empty search, invalid video, or backend issues.

---

## 7. Accessibility (a11y) Requirements

- All interactive elements are reachable and usable by keyboard.
- Use ARIA attributes where appropriate.
- Provide focus outlines and skip-to-content links.
- Ensure color/contrast meets WCAG AA standards.

---

## 8. Testing and Validation

- Unit tests for all components using Jest + React Testing Library.
- Integration tests for key flows (search, select, transcribe, submit).
- End-to-end tests (Cypress) for page navigation, accessibility, and error states.
- Validate accessibility using automated tools and manual keyboard navigation checks.

---

## 9. Design Consistency

- Strictly adhere to styling and layout rules from `specs/frontend-update.md`.
- Use design tokens for spacing, colors, typography, and border radii.
- All new components must be reusable and documented.

---

## 10. Implementation Notes & Gotchas

- Avoid code and variable naming inconsistencies (e.g., always use "transcribe" not "transcrive").
- Abstract repeated UI logic into shared components.
- Provide clear prop definitions for all components.
- Ensure scroll anchoring to the video player is smooth and accessible.
- All logic for action buttons must reference `para-incluir_Transcription_Botoes_Logic.md`.
- Original transcript capture must implement logic from `para-incluir_Captura_Transcr_Originais.md`.
- Transcript caching should follow patterns in `para-incluir_Cache_Logic-Incluir_Captura.md`.
- Transcription comparison must implement algorithms from `para-incluir_Transcription_Correction_Logic_Python.md`.
- Thoroughly document any API contract or UI deviation from this spec.

---

## 11. Change Management and Future Enhancements

- Update this spec as new requirements emerge or if the design system evolves.
- All modifications must be peer-reviewed and validated against this document and the global design system.

---

## 12. References

- [Project README](README.md)
- [Application Requirements](specs/application-requirements.md)
- [Application Design](specs/application-design.md)
- [Frontend Update Spec](specs/frontend-update.md)
- [Implementation Plan](specs/implementation-plan.md)
- [Transcription Buttons Logic](para-incluir_Transcription_Botoes_Logic.md)
- [Original Transcription Capture](para-incluir_Captura_Transcr_Originais.md)
- [Transcription Caching Implementation](para-incluir_Cache_Logic-Incluir_Captura.md)
- [Transcription Correction Logic](para-incluir_Transcription_Correction_Logic_Python.md)
- [Changelog](progress-tracking/CHANGELOG.md)

---

_This document supersedes all prior ad-hoc instructions for the transcription workflow pages. All future work must comply fully with this specification._