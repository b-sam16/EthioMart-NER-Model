import pandas as pd
import os

class CoNLLFormatter:
    def __init__(self, input_csv, output_txt, sample_size=50):
        self.input_csv = input_csv
        self.output_txt = output_txt
        self.sample_size = sample_size

    def prepare_dataset(self):
        """Load the dataset and sample a subset for labeling."""
        if not os.path.exists(self.input_csv):
            print(f"Error: Input file {self.input_csv} not found.")
            return None

        data = pd.read_csv(self.input_csv)
        if 'Message' not in data.columns:
            print("Error: 'Message' column not found in the dataset.")
            return None

        # Sample messages
        sampled_data = data['Message'].dropna().sample(n=self.sample_size, random_state=42)
        return sampled_data.tolist()

    def save_conll_format(self, messages):
        """Save the dataset in CoNLL format for manual labeling."""
        with open(self.output_txt, 'w', encoding='utf-8') as file:
            for message in messages:
                tokens = message.split()  # Tokenize message into words
                for token in tokens:
                    file.write(f"{token} O\n")  # Default label as "O" for manual correction
                file.write("\n")  # Blank line between sentences
        print(f"Labeled dataset saved to {self.output_txt}. Please label it manually.")

    def run(self):
        """Main execution function."""
        messages = self.prepare_dataset()
        if messages:
            self.save_conll_format(messages)

if __name__ == "__main__":
    # File paths
    input_csv = "data/processed/preprocessed_telegram_data.csv"
    output_txt = "data/processed/labeled_dataset.conll"

    # Initialize and run the formatter
    formatter = CoNLLFormatter(input_csv=input_csv, output_txt=output_txt, sample_size=50)
    formatter.run()
