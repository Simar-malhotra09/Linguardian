import fitz
import re
import unicodedata


def is_english_word(word):
        """Check if the word contains only Latin characters."""
        for char in word:
            print (unicodedata.name(char, '') )



