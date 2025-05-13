"""
Transcription service module.

This module provides functionality for comparing and analyzing text transcriptions,
calculating accuracy scores, and generating detailed feedback.
"""

import re
from difflib import SequenceMatcher
from typing import Dict, List, Tuple

def preprocess_text(text: str) -> str:
    """
    Preprocesses text for comparison by:
    - Converting to lowercase
    - Removing punctuation except apostrophes
    - Removing extra whitespace
    
    Args:
        text: The text to preprocess
        
    Returns:
        Preprocessed text ready for comparison
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation except apostrophes
    text = re.sub(r'[^\w\s\']', '', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def compare_transcriptions(user_text: str, reference_text: str) -> float:
    """
    Compares user transcription with the reference transcription and
    calculates an accuracy score between 0.0 and 1.0.
    
    Args:
        user_text: Text transcribed by the user
        reference_text: The reference/correct transcription
        
    Returns:
        Accuracy score between 0.0 and 1.0
    """
    if not user_text or not reference_text:
        return 0.0
    
    # Preprocess both texts
    clean_user_text = preprocess_text(user_text)
    clean_reference_text = preprocess_text(reference_text)
    
    # Calculate similarity using SequenceMatcher
    matcher = SequenceMatcher(None, clean_user_text, clean_reference_text)
    similarity = matcher.ratio()
    
    return similarity

def get_detailed_comparison(user_text: str, reference_text: str) -> Dict:
    """
    Performs a detailed word-by-word comparison between user and reference text.
    
    Args:
        user_text: Text transcribed by the user
        reference_text: The reference/correct transcription
        
    Returns:
        Dictionary containing:
        - overall_accuracy: Overall accuracy score
        - word_matches: List of tuples (user_word, reference_word, is_match)
        - stats: Dictionary with statistics (correct_words, total_words, etc.)
    """
    if not user_text or not reference_text:
        return {
            "overall_accuracy": 0.0,
            "word_matches": [],
            "stats": {
                "correct_words": 0,
                "total_words": 0,
                "missed_words": 0,
                "extra_words": 0
            }
        }
    
    # Preprocess both texts
    clean_user_text = preprocess_text(user_text)
    clean_reference_text = preprocess_text(reference_text)
    
    # Split into words
    user_words = clean_user_text.split()
    reference_words = clean_reference_text.split()
    
    # Calculate overall accuracy
    overall_accuracy = compare_transcriptions(user_text, reference_text)
    
    # Calculate word-by-word matching using difflib's SequenceMatcher
    matcher = SequenceMatcher(None, user_words, reference_words)
    
    # Process the match information
    word_matches = []
    correct_words = 0
    total_ref_words = len(reference_words)
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            # Words match
            for k in range(i2 - i1):
                word_matches.append((user_words[i1 + k], reference_words[j1 + k], True))
                correct_words += 1
        elif tag == 'replace':
            # Words are different
            for k in range(max(i2 - i1, j2 - j1)):
                user_word = user_words[i1 + k] if i1 + k < i2 else None
                ref_word = reference_words[j1 + k] if j1 + k < j2 else None
                word_matches.append((user_word, ref_word, False))
        elif tag == 'delete':
            # Words in user text but not in reference
            for k in range(i2 - i1):
                word_matches.append((user_words[i1 + k], None, False))
        elif tag == 'insert':
            # Words in reference but not in user text
            for k in range(j2 - j1):
                word_matches.append((None, reference_words[j1 + k], False))
    
    # Calculate stats
    extra_words = len(user_words) - correct_words
    missed_words = total_ref_words - correct_words
    
    stats = {
        "correct_words": correct_words,
        "total_words": total_ref_words,
        "missed_words": missed_words,
        "extra_words": max(0, extra_words)
    }
    
    return {
        "overall_accuracy": overall_accuracy,
        "word_matches": word_matches,
        "stats": stats
    } 