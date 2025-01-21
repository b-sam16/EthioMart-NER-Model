from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import os
import sys
import csv
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TelegramScraper:
    def __init__(self, input_csv):
        load_dotenv('.env')
        self.api_id = os.getenv('TG_API_ID')
        self.api_hash = os.getenv('TG_API_HASH')
        self.phone = os.getenv('phone')
        self.client = TelegramClient('scraping_session', self.api_id, self.api_hash)
        self.input_csv = input_csv

    async def scrape_channel(self, client, channel_username, writer, media_dir):
        """Scrapes messages, metadata, and media from a Telegram channel."""
        try:
            async for message in client.iter_messages(channel_username, limit=10000):
                content = message.message or ''
                date = message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else ''
                media_path = None

                # Download media if present
                #if isinstance(message.media, (MessageMediaPhoto, #MessageMediaDocument)):
                #    media_path = os.path.join(media_dir, f"{message.id}.jpg")
                #    await client.download_media(message, media_path)

                writer.writerow([message.chat.title, channel_username, message.id, content, date, media_path])
        except Exception as e:
            print(f"Error scraping {channel_username}: {e}")

    async def scrape_channels(self):
        """Scrapes multiple channels and saves data to CSV."""
        await self.client.start()
        media_dir = 'data/media'
        os.makedirs(media_dir, exist_ok=True)

        # Skip scraping if the output file already exists
        if os.path.exists(self.input_csv):
            print(f"Scraped data already exists at {self.input_csv}. Skipping scraping.")
            return
        
        with open(self.input_csv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])

            channels = ['@helloomarketethiopia', '@Shewabrand', '@modernshoppingcenter', '@sinayelj', '@ZemenExpress']
            for channel in channels:
                print(f"Scraping channel: {channel}")
                await self.scrape_channel(self.client, channel, writer, media_dir)

    def run(self):
        """Runs the scraper."""
        with self.client:
            self.client.loop.run_until_complete(self.scrape_channels())

def main():
    # Define file path and directories
    raw_data_dir = 'data/raw'
    os.makedirs(raw_data_dir, exist_ok=True)  # Ensure raw data directory exists
    input_csv = os.path.join(raw_data_dir, 'telegram_data.csv')

    # Step 1: Scrape data from Telegram channels
    scraper = TelegramScraper(input_csv=input_csv)
    scraper.run()

if __name__ == '__main__':
    main()