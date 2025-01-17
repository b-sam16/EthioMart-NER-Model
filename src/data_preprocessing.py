import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import re
import os

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')  # Ensure punkt_tab is downloaded

class DataPreprocessor:
    def __init__(self, input_csv, output_csv):
        self.input_csv = input_csv
        self.output_csv = output_csv

    def preprocess_text(self, text):
        """Tokenize, normalize, and clean Amharic text."""
        if not text or pd.isna(text):
            return None
        # Remove non-Amharic characters
        text = re.sub(r'[^፩-፻ሀ-፞ ]', ' ', text)
        # Tokenize text
        tokens = word_tokenize(text)
        return ' '.join(tokens)

    def preprocess_data(self):
        """Preprocess raw data."""
        if not os.path.exists(self.input_csv):
            print(f"Error: Input file {self.input_csv} not found.")
            return

        data = pd.read_csv(self.input_csv)
        if 'Message' not in data.columns:
            print("Error: 'Message' column not found in input data.")
            return

        # Preprocess messages
        data['Message'] = data['Message'].apply(self.preprocess_text)
        data.to_csv(self.output_csv, index=False)
        print(f"Preprocessed data saved to {self.output_csv}")
