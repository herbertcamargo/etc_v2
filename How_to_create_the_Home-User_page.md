# Full Specification: /home-user Page Development

## Task Overview

Your task is divided into **three main parts**:

---

## Part 1: Create the `/home-user` Page

The `/home-user` page must include the following components:

1. **YouTube Search Bar**  
   - A text input field  
   - A `Search` button next to it (horizontally aligned)  
   - The text input must be larger than the button

2. **YouTube iFrame**  
   - An embedded YouTube player (iFrame) to play the selected video

3. **Transcription Input Box**  
   - A text input area located **below** the video

4. **Button Set**  
   - Buttons described in the file `para-incluir_Transcription_Botoes_Logic.md`  
   - Placed **below** the transcription input  
   - Arranged horizontally (side by side)

5. **Results Output Box**  
   - A text output area called `Results`  
   - Placed **below** the buttons

---

## Part 2: Frontend Integration

Integrate the frontend components as follows:

a. When the user types in the search box and clicks `Search`, it triggers a **YouTube video search**

b. The **Search Results** appear below the search input section

c. Clicking on a result selects that video

d. The selected video is displayed and played in the **iFrame**

e. All additional frontend logic must comply with `para-incluir_Transcription_Botoes_Logic.md`

---

## Part 3: Backend Development

The backend must support the following functionalities:

i. **YouTube Video Search**  
ii. **Display of Search Results**  
iii. **Reproduction of the Selected Video in the iFrame**  
iv. **All Button Functionalities**  
v. **Original Transcript Capturing** using logic from `para-incluir_Captura_Transcr_Originais.md`  
vi. **Transcription Correction and Results Display**, based on `para_incluir_Transcription_Correction_Logic_Python.md`  
vii. **Transcript Caching Integration**, using logic from `para-incluir_Cache_Logic-Incluir-Captura.md`

---

End of Specification
