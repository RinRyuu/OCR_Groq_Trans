import re
from typing import Set

class ContentFilter:
    def __init__(self):
        # Common Hindi and English profanity words (this is a minimal example)
        # In production, you'd want a more comprehensive list
        self.profanity_list: Set[str] = {
            # Add your list of words to filter here
           'गंदी', 'बकवास', 'फालतू', 'चूत', 'मादर', 'बायच'# Placeholder words
        }
        
        # Load additional word lists
        self.load_word_lists()
    
    def load_word_lists(self):
        """Load profanity word lists from files if they exist"""
        try:
            # You can create these files with comprehensive lists
            files = ['hindi_profanity.txt', 'english_profanity.txt', 'marathi_profanity.txt']
            for file in files:
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        self.profanity_list.update(word.strip().lower() for word in f.readlines())
                except FileNotFoundError:
                    pass
        except Exception as e:
            print(f"Error loading word lists: {e}")

    def clean_text(self, text: str) -> str:
        """Clean text by removing or replacing inappropriate content"""
        if not text:
            return text
            
        cleaned_text = text.lower()
        
        # Replace profanity with asterisks
        for word in self.profanity_list:
            # Create a pattern that matches the word with flexible boundaries
            pattern = r'\b' + re.escape(word) + r'\b'
            cleaned_text = re.sub(pattern, '*' * len(word), cleaned_text, flags=re.IGNORECASE)
        
        # Additional cleaning steps
        cleaned_text = self.remove_excessive_punctuation(cleaned_text)
        cleaned_text = self.normalize_spacing(cleaned_text)
        
        return cleaned_text.strip()
    
    @staticmethod
    def remove_excessive_punctuation(text: str) -> str:
        """Remove excessive punctuation while preserving sentence structure"""
        # Replace multiple punctuation marks with a single one
        text = re.sub(r'([!?.]){2,}', r'\1', text)
        return text
    
    @staticmethod
    def normalize_spacing(text: str) -> str:
        """Normalize spacing in text"""
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        return text.strip()