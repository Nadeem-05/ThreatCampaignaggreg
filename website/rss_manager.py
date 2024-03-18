import requests
from . import db
from .modals import Rssfeed
import feedparser
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

ALIENVAULT_API_KEY = os.environ.get("ALIENVAULT_API_KEY")

class RssManager:
    def __init__(self, app, rss_feed_urls):
        self.app = app
        self.rss_feed_urls = rss_feed_urls

    def fetch_rss_data(self):
        rss_data = []
        for feed_url in self.rss_feed_urls:
            feed = feedparser.parse(feed_url)
            try:
                if feed.status == 200:
                    rss_data.extend(self._process_feed_data(feed))
                    print(f"Got RSS data for {feed_url}")
                else:
                    print(f"Failed to fetch RSS data from {feed_url}: {feed.status}")
            except:
                print(f"Failed to fetch RSS data from {feed_url}")
        return rss_data
    def fetch_alien_vault_data(self):
        url = "https://otx.alienvault.com/api/v1/pulses/activity?page=1"
        headers = {
            "X-OTX-API-KEY": f"{ALIENVAULT_API_KEY}"
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        print("Got data From AlienVault")
        return data.get("results", [])


    def add_alien_vault_data_to_db(self, alien_vault_data):
        with self.app.app_context():
            for item in alien_vault_data:
                title = item["name"]
                date = item["created"]
                link = f"https://otx.alienvault.com/pulse/{item['id']}"
                source = "AlienVault"
                existing_feed = Rssfeed.query.filter_by(link=link).first()
                if existing_feed:
                    print(f"Link '{link}' already exists in the database.")
                else:
                    new_feed = Rssfeed(title=title, date=date, link=link,source=source,date_added=datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z IST"))
                    db.session.add(new_feed)
                    print(f"Added new feed: {title}")
            db.session.commit()


    def _process_feed_data(self, feed):
        processed_articles = []
        entries = feed.entries[:5]
        for entry in entries:
            try:
                title = entry.title
                date = entry.published
                link = entry.link
                source = feed.feed.title
                processed_articles.append({"title": title, "date": date, "link": link, "source": source})
            except AttributeError:
                print(f"Skipping entry due to unexpected format: {entry}")
                continue
        return processed_articles



    def add_rss_data_to_db(self, rss_data):
        with self.app.app_context():
            for item in rss_data:
                title = item["title"]
                date = item["date"]
                link = item["link"]
                source = item["source"]
                existing_feed = Rssfeed.query.filter_by(link=link).first()
                if existing_feed:
                    print(f"Link '{link}' already exists in the database.")
                else:
                    new_feed = Rssfeed(title=title, date=date, link=link,source=source,date_added=datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z IST"))
                    db.session.add(new_feed)
                    print(f"Added new feed: {title}")
            db.session.commit()