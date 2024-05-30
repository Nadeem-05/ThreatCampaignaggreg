from website import create_app
from website.rss_manager import RssManager
from website.modals import Rssfeed

def update_database():
    app = create_app()
    with app.app_context():
        print("Database updation started.")
        rss_feed_list = [
            "https://blog.group-ib.com/rss.xml",
            "https://www.netskope.com/blog/feed",
            "https://www.cloudsek.com/blog/rss.xml",
            "https://osinter.dk/feed/day",
            "https://filestore.fortinet.com/fortiguard/rss/threatsignal.xml",
            "https://filestore.fortinet.com/fortiguard/rss/outbreakalert.xml",
            "https://feeds.fortinet.com/fortinet/blog/psirt",
            "https://www.varonis.com/blog/rss.xml",
            "https://feeds.feedburner.com/akamai/blog",
            "https://newsroom.trendmicro.com/cyberthreat?pagetemplate=rss",
            "https://www.huntress.com/blog/rss.xml",
            "https://www.cyberark.com/feed/",
            "https://cyware.com/allnews/feed",
            "https://www.cybersecurity-help.cz/blog/rss/",
            "https://research.checkpoint.com/feed/",
            "https://securelist.com/feed/",
            "https://www.resecurity.com/feed",
            "https://www.welivesecurity.com/en/rss/feed/",
            "https://www.securonix.com/feed/",
            "https://www.sentinelone.com/feed/",
            "https://news.sophos.com/en-us/feed/",
            "https://socradar.io/feed/",
            "https://www.recordedfuture.com/feed",
            "https://www.microsoft.com/en-us/security/blog/feed/",
            "https://www.malwarebytes.com/blog/feed/index.xml",
            "https://www.proofpoint.com/us/threat-insight-blog.xml",
            "https://unit42.paloaltonetworks.com/feed/",
            "https://www.bitdefender.com/blog/api/rss/labs/",
            "https://www.jamf.com/blog/rss/",
            "https://arcticwolf.com/feed/",
            "https://blog.talosintelligence.com/rss/",
            "https://securityintelligence.com/feed/",
            "https://blog.lumen.com/feed/",
            "https://www.deepinstinct.com/blog/feed",
            "https://www.mcafee.com/blogs/other-blogs/mcafee-labs/feed",
            "https://www.imperva.com/blog/feed/",
            "https://trust.zscaler.com/blog-feed",
            "https://feeds.fortinet.com/fortinet/blog/threat-research",
            "https://isc.sans.edu/rssfeed.xml",
            "https://www.elastic.co/security-labs/rss/feed.xml",
            "https://www.cybereason.com/blog/rss.xml",
            "https://asec.ahnlab.com/en/feed/",
            "https://www.seqrite.com/blog/feed/",
            "https://blog.sekoia.io/feed/",
            "https://www.safebreach.com/blog/feed",
            "https://cyble.com/blog/feed/",
            "https://thecyberexpress.com/feed/",
            "https://www.trustwave.com/en-us/rss/trustwave-blogs/",
            "https://www.armosec.io/blog/feed/",
            "https://thedfirreport.com/feed/",
            "https://www.exploit-db.com/rss.xml",
            "https://www.zerodayinitiative.com/rss/published/",
            "https://bishopfox.com/feeds/advisories.rss",
            "https://blog.morphisec.com/rss.xml",
            "https://securityonline.info/feed/",
            "https://orca.security/feed/",
            "https://www.forcepoint.com/rss.xml",
            "https://www.netskope.com/feed",
        ]
        rss_manager = RssManager(app, rss_feed_list)
        print("Fetchind data from Alienvault")
        alienvault_data = rss_manager.fetch_alien_vault_data()
        rss_manager.add_alien_vault_data_to_db(alienvault_data)
        print("Fetching RSS Feeds data")
        rss_data = rss_manager.fetch_rss_data()
        rss_manager.add_rss_data_to_db(rss_data)
        

        print("Database update complete.")


if __name__ == "__main__":
    update_database()
