from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import os
import csv
from dotenv import load_dotenv

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
            async for message in client.iter_messages(channel_username, limit=100):
                content = message.message or ''
                date = message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else ''
                media_path = None

                # Download media if present
                if isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument)):
                    media_path = os.path.join(media_dir, f"{message.id}.jpg")
                    await client.download_media(message, media_path)

                writer.writerow([message.chat.title, channel_username, message.id, content, date, media_path])
        except Exception as e:
            print(f"Error scraping {channel_username}: {e}")

    async def scrape_channels(self):
        """Scrapes multiple channels and saves data to CSV."""
        await self.client.start()
        media_dir = 'data/media'
        os.makedirs(media_dir, exist_ok=True)

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
