from website import create_app
from website.rss_manager import RssManager

app = create_app()

if __name__ == "__main__":
    app.run(port=5000)