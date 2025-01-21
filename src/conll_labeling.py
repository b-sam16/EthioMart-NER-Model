import re
import pandas as pd
import random
import os

class MessageLabeler:
    def __init__(self):
        # Example locations and keywords for location detection
        self.locations = ['Addis Ababa', 'ቦሌ', 'ፒያሳ', 'አዲስ አበባ', 'ልደታ']  # Expand as needed
        self.location_keywords = ['አድራሻ', 'ፎቅ', 'ሞል', 'ህንፃ']  # Keywords for detecting locations

    def label_message(self, message):
        """Label a message with entity tags (e.g., B-PRODUCT, I-PRODUCT, B-LOC, I-LOC, B-PRICE, I-PRICE, O)."""
        if not message:
            return ""  # Return empty string if the message is empty
        
        labeled_tokens = []

        # Split the message into lines
        lines = message.split("\n")
        
        # Process the first line as product-related entities
        if lines:
            first_line_tokens = re.findall(r'\S+', lines[0])  # Tokens from the first line
            if first_line_tokens:
                labeled_tokens.append(f"{first_line_tokens[0]} B-PRODUCT")  # First token is B-PRODUCT
                for token in first_line_tokens[1:]:
                    labeled_tokens.append(f"{token} I-PRODUCT")  # Rest are I-PRODUCT
        
        # Process remaining lines for other entities
        for line in lines[1:]:  # Skip the first line
            tokens = re.findall(r'\S+', line)  # Tokenize each line considering non-ASCII characters
            
            for i, token in enumerate(tokens):
                # Handle price detection (e.g., 500 ETB, $100, or ብር)
                if re.match(r'^\d+(\.\d{1,2})?$', token) or 'ብር' in token or 'birr' in token:
                    label = 'B-PRICE' if i == 0 or labeled_tokens[-1].split()[-1] != 'I-PRICE' else 'I-PRICE'
                    labeled_tokens.append(f"{token} {label}")
                # Handle phone number detection (e.g., +251911234567, 0911234567)
                elif re.match(r'^\+251\d{9}$', token) or re.match(r'^\d{10}$', token):  # Common Ethiopian phone number format
                    labeled_tokens.append(f"{token} O")  # Label phone numbers as 'O' (Other)
                # Handle location detection
                elif any(loc in token for loc in self.locations):
                    label = 'B-LOC' if i == 0 or labeled_tokens[-1].split()[-1] != 'I-LOC' else 'I-LOC'
                    labeled_tokens.append(f"{token} {label}")
                elif any(keyword in token for keyword in self.location_keywords):
                    if 'አድራሻ' in token and i + 1 < len(tokens):  # Label next token if 'አድራሻ' (address) is present
                        labeled_tokens.append(f"{tokens[i + 1]} B-LOC")
                    elif token in ['ፎቅ', 'ሞል', 'ህንፃ'] and i > 0:  # Label the previous token if 'ፎቅ', 'ሞል', or 'ህንፃ' are present
                        labeled_tokens.append(f"{tokens[i - 1]} B-LOC")
                else:
                    labeled_tokens.append(f"{token} O")  # Label as 'Other' (O)

        # Return the labeled tokens as a space-separated string with blank lines separating sentences
        return "\n".join(labeled_tokens) + "\n"  # Adding a newline at the end to separate messages

def label_dataset(input_csv, output_txt):
    """Apply the label function to a random subset of 50 messages from the dataset and save in CoNLL format."""
    # Read the preprocessed data
    df = pd.read_csv(input_csv)
    if 'Message' not in df.columns:
        print("Error: 'Message' column not found in input data.")
        return

    # Drop null messages and randomly select 50 messages
    df = df.dropna(subset=['Message'])
    df_subset = df.sample(n=50, random_state=42)  # Always select exactly 50 random messages

    # Initialize the MessageLabeler
    labeler = MessageLabeler()

    # Open output file to write the labeled data
    with open(output_txt, 'w', encoding='utf-8') as f:
        for _, row in df_subset.iterrows():
            message = row['Message']
            labeled_message = labeler.label_message(message)
            f.write(labeled_message)  # Write the labeled message in CoNLL format
            f.write("\n")  # Separate messages with a blank line

    print(f"Labeled data saved to {output_txt}")

def main():
    """Main function to label the dataset."""
    # Define file paths
    processed_data_dir = 'data/processed'
    os.makedirs(processed_data_dir, exist_ok=True)
    input_csv = 'data/processed/preprocessed_telegram_data.csv'  # Use the already preprocessed data
    output_txt = os.path.join(processed_data_dir, 'labeled_telegram_data.txt')

    # Step 1: Label the preprocessed data
    label_dataset(input_csv=input_csv, output_txt=output_txt)

if __name__ == '__main__':
    main()
