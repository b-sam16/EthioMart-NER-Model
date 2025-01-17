import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.telegram_scraper import TelegramScraper
from src.data_preprocessing import DataPreprocessor

def main():
    print("Running the EthioMart NER Pipeline")

    # Define file paths
    raw_data_dir = "data/raw"
    processed_data_dir = "data/processed"
    os.makedirs(raw_data_dir, exist_ok=True)
    os.makedirs(processed_data_dir, exist_ok=True)

    input_csv = os.path.join(raw_data_dir, "telegram_data.csv")
    output_csv = os.path.join(processed_data_dir, "preprocessed_telegram_data.csv")

    # Check if the CSV file already exists and has data
    if os.path.exists(input_csv) and os.path.getsize(input_csv) > 0:
        print(f"Data already scraped and saved in {input_csv}. Skipping scraping.")
    else:
        # Scrape data from Telegram channels
        scraper = TelegramScraper(input_csv=input_csv)
        scraper.run()  # Ensures the coroutine is called properly

    # Step 2: Preprocess the scraped data
    preprocessor = DataPreprocessor(input_csv=input_csv, output_csv=output_csv)
    preprocessor.preprocess_data()

if __name__ == '__main__':
    main()
