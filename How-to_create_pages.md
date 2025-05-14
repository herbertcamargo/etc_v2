# Full Specification: /transcrive Page Development

## Task Overview

Your task is divided into **four main parts**:

---

Before starting, basically what is the `/transcribe` page doing?
   - The `/transcribe` page displays both the **YouTube Search Bar** and the **Search Results**.
   - After clicking the selected search result, the user is redirected to the page `/transcribe/video`.
   - The page `/transcribe/video` shows the **YouTube Search Bar** and the **Search Results** loaded from the page `/transcribe`which the user was in, with all their functionalities still working, and below them, the `/transcribe/video` page shows the **YouTube iFrame**, the **Transcription Input Box**, the **Button Set** and the **Results Output Box**.
   - When the `/transcribe/video` page is loaded or reloaded, the scroll must be anchored to the **YouTube iFrame**. 


## Part 1: Create the `/transcribe` Page

The `/transcribe` page must include the following components:

1. **YouTube Search Bar**  
   - A text input field  
   - A `Search` button next to it (horizontally aligned)  
   - The text input must be larger than the button

2. **Search Results**  
   - The top 12 results of the **YouTube video search** after the `Search` be triggered, listed on 4 lines of 3 results each.


## Part 2: Create the `/transcribe/video` Page

The `/transcribe/video` page must include the following components:

1. **YouTube Search Bar**  
   - A text input field  
   - A `Search` button next to it (horizontally aligned)  
   - The text input must be larger than the button

2. **Search Results**  
   - The top 12 results of the **YouTube video search** after the `Search` be triggered, listed on 4 lines of 3 results each.

3. **YouTube iFrame**  
   - An embedded YouTube player (iFrame) to play the selected video

4. **Transcription Input Box**  
   - A text input area located **below** the video

5. **Button Set**  
   - Buttons described in the file `para-incluir_Transcription_Botoes_Logic.md`  
   - Placed **below** the transcription input  
   - Arranged horizontally (side by side)

6. **Results Output Box**  
   - A text output area called `Results`  
   - Placed **below** the buttons

---

## Part 3: Frontend Integration

Integrate the frontend components as follows:

a. When the user types in the search box and clicks `Search`, it triggers a **YouTube video search**

b. The **Search Results** appear below the search input section

c. Clicking on a result selects that video

d. The selected video is displayed and played in the **iFrame**

e. All additional frontend logic must comply with `para-incluir_Transcription_Botoes_Logic.md`

---

## Part 4: Backend Development

The backend must support the following functionalities:

i. **YouTube Video Search**, filtering only videos which support the youtube iFrame API.
ii. **Display of Search Results**  
iii. **Reproduction of the Selected Video in the iFrame**  
iv. **All Button Functionalities**  
v. **Original Transcript Capturing** using logic from `para-incluir_Captura_Transcr_Originais.md`  
vi. **Transcription Correction and Results Display**, based on `para_incluir_Transcription_Correction_Logic_Python.md`  
vii. **Transcript Caching Integration**, using logic from `para-incluir_Cache_Logic-Incluir-Captura.md`

---

End of Specification
