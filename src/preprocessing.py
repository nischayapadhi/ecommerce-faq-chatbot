import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download necessary NLTK data (only runs once)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab') # <--- CHECK FOR THIS
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("Downloading NLTK resources...")
    nltk.download('punkt')
    nltk.download('punkt_tab') # <--- ADD THIS LINE
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    print("Download complete.")

# Initialize Lemmatizer and Stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """
    Takes a raw string and performs:
    1. Lowercasing
    2. Removing special characters/numbers
    3. Tokenization
    4. Stopword removal
    5. Lemmatization
    
    Returns: A list of clean tokens (e.g., ['track', 'order'])
    """
    if not isinstance(text, str):
        return []
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove special characters (keep only alphabets)
    text = re.sub(r'[^a-z\s]', '', text)
    
    # 3. Tokenize
    tokens = word_tokenize(text)
    
    # 4. & 5. Remove Stopwords and Lemmatize
    # We keep words that are NOT in stop_words and lemmatize them
    clean_tokens = [
        lemmatizer.lemmatize(word) 
        for word in tokens 
        if word not in stop_words
    ]
    
    return clean_tokens

if __name__ == "__main__":
    # Quick test to see if it works when running this file directly
    sample = "How can I track my orders??? Running fast!"
    print(f"Original: {sample}")
    print(f"Cleaned: {clean_text(sample)}")