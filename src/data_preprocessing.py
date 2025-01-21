import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

nltk.download('punkt')
nltk.download('punkt_tab')  # Ensure punkt_tab is downloaded

class DataPreprocessor:
    def __init__(self, input_csv, output_csv):
        self.input_csv = input_csv
        self.output_csv = output_csv

        # Define a basic Amharic stop words list (expand as needed)
        self.amharic_stopwords = set([
            "እንደ", "እና", "ወይም", "ለ", "ከ", "ስለ", "ወደ", "በተለይ", "እስከ", "እንጂ",
            "በኩል", "በዚህ", "የሚሆን"
        ])
        # English stop words from NLTK
        self.english_stopwords = set(stopwords.words('english'))

    def preprocess_text(self, text):
        """Tokenize, normalize, and clean Amharic text."""
        if not text or pd.isna(text):
            return None
        
        # Keep newlines intact by replacing them with a unique token
        text = text.replace('\n', '\\n')

        # Remove Duplicate words
        text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)

        # Remove URLs and email addresses
        text = re.sub(r'(https?://\S+|www\.\S+)', '', text)  # Remove URLs
        text = re.sub(r'\S+@\S+\.\S+', '', text)  # Remove email addresses

        # Normalize by removing special characters, except alphanumerics and Amharic characters
        text = re.sub(r'[^፩-፻ሀ-፞A-Za-z0-9.,\\n]', ' ', text)
        
        # Tokenize text into words
        tokens = word_tokenize(text)

        # Convert to lowercase (if Latin characters are included)
        tokens = [token.lower() if token.isalpha() else token for token in tokens]

        # Remove Amharic stop words
        tokens = [token for token in tokens if token not in self.amharic_stopwords]

        # Remove English stop words
        tokens = [token for token in tokens if token not in self.english_stopwords]
        
        # Join tokens back, restoring newlines
        processed_text = ' '.join(tokens)
        processed_text = processed_text.replace('\\n', '\n')

        return processed_text

    def preprocess_data(self):
        """Preprocess raw data."""
        if not os.path.exists(self.input_csv):
            print(f"Error: Input file {self.input_csv} not found.")
            return
        
        data = pd.read_csv(self.input_csv)
        if 'Message' not in data.columns:
            print("Error: 'Message' column not found in input data.")
            return

        # drop null values in messages column
        data = data.dropna(subset=['Message'])
        
        # Preprocess messages
        data['Message'] = data['Message'].apply(self.preprocess_text)
        data.to_csv(self.output_csv, index=False)
        print(f"Preprocessed data saved to {self.output_csv}")

def main():
    # Define file paths and directories
    processed_data_dir = 'data/processed'
    os.makedirs(processed_data_dir, exist_ok=True)  # Ensure processed data directory exists

    input_csv = 'data/raw/telegram_data.csv'
    output_csv = os.path.join(processed_data_dir, 'preprocessed_telegram_data.csv')

    # Step 2: Preprocess the scraped data
    preprocessor = DataPreprocessor(input_csv=input_csv, output_csv=output_csv)
    preprocessor.preprocess_data()

if __name__ == '__main__':
    main()