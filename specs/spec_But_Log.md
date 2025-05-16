
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

---

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

---

## 3. `Rewind_Button`

- **Label**: `"Rewind"` (centered)
- **Action**: On click, rewinds the video by the currently selected `Rewind_time_Dropdown` value

---

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
- On click: active the backend steps to generate the transcription comparison results
  - If transcription comparison results are not yet shown → show transcription comparison results
  - If transcription comparison results are being shown → stop showing the transcription comparison results