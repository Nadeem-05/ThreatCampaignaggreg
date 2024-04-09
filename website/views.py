from flask import Blueprint, render_template,redirect,url_for,request,current_app,jsonify
from . import db
from .rss_manager import RssManager
from .modals import Rssfeed
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
import re
import time
from dotenv import load_dotenv
import json
import ast

load_dotenv() 
  
TUNE_API_KEY = os.environ.get("TUNE_API_KEY")

views = Blueprint("views", __name__)

@views.route('/reportgen', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id = int(request.form['id'])
        existing_feed = Rssfeed.query.filter_by(id=id).first()
        try:
            existing_feed.link
        except:
            return "not a valid id"
        
        cleaned_text=get_data(existing_feed.link)
        if not cleaned_text.startswith("Failed"):
            url = "https://chat.tune.app/api/chat/completions"
            headers = {
                "Authorization": f"{TUNE_API_KEY}",
                "Content-Type": "application/json"
            }
            stream = False
            data = {
                "temperature": 0.5,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are RssBot"
                    },
                    {
                        "role": "user",
                        "content": f"""
                    {cleaned_text}
                    Read through the below advisory. Your task is to produce the followings: 
                    1. Provide a suitable title that outlines the advisory details 
                    2. Provide a 2 liner summary that covers the crux of the advisory in short 
                    3. Check whether any threat actor/threat group mentioned in the writing. If so, list the name of the threat actor /threat group 
                    4. Check whether any Malware mentioned in the writing. If so, list the name of the malware 
                    5. Check whether specific targeted countries mentioned in the writing. If so, list the country names as comma separated. 
                    6. Check whether specific targeted industries mentioned in the writing. If so, list the industry names as comma separated. 
                    7. Check whether any specific applications or CVE is targeted as part the advisory. If so, list the same.
                    8. Understand the impact associated with the advisory. Provide the impact information in short (example: Data Breach, Device compromise, Ransomware attacks, etc) 
                    9. Check whether any IOCs listed in the advisory. If so, list the IOCs as defanged format under their respective IOC_Categories (example: IP, Domains, URLs, Sha). Ensure only to mention IOC values. Do not mention their descriptions. 
                    10. Check whether MITRE TTP IDs are explicitly mentioned in the advisory. If yes, extract the TTP IDs and provide as comma separated. If MITRE TTP IDs not explicitly listed, then understand the attack methods mentioned in the advisory and provide equivalent TTP IDs as comma separated. Ensure only to mention TTP IDs. Do not mention TTP names or descriptions.                  """
                    }
                ],
                "model": "mixtral-8x7b-inst-v0-1-32k",
                "stream": stream,
                "max_tokens": 1000
            }
            response = requests.post(url, headers=headers, json=data)
            response = response.json()
            h = response['choices'][0]['message']['content']
            return render_template('result.html', h=h)
        else:
            error_msg = "Failed to retrieve webpage. Status code: " + \
                str(cleaned_text)
            return render_template('error.html', error=error_msg)
    return render_template('index.html')

@views.route("/", methods=["GET"])
def home_page():
    articles = Rssfeed.query.all()
    return render_template("rss_table.html", articles=articles)

@views.route("/json", methods=["GET"])
def json_page():
    query = request.args.get('query')
    times = request.args.get('time')  # Get list of times
    times = list(times)
    print(list(times))
    articles_query = Rssfeed.query
    if query:
        articles_query = articles_query.filter(Rssfeed.title.ilike(f"%{query}%"))
    
    if times:
        filtered_articles = []
        for time_str in times:
            articles_filtered_by_time = articles_query.filter(Rssfeed.date_added.ilike(f"%{time_str}%")).all()
            filtered_articles.extend(articles_filtered_by_time)
    else:
        filtered_articles = articles_query.all()

    article_dicts = [{'id': article.id, 'title': article.title, 'date': article.date,
                      'date_added': article.date_added, 'link': article.link,
                      'source': article.source, 'status': article.status} for article in filtered_articles]
    return jsonify(article_dicts)

@views.route("/update_status/<int:article_id>", methods=["POST"])
def update_status(article_id):
    new_status = request.form.get("status")
    article = Rssfeed.query.get_or_404(article_id)
    article.status = new_status
    db.session.commit()
    return redirect(url_for('views.home_page'))


@views.route("/updatedb", methods=["GET"])
def updatedb():
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
        "https://orca.security/feed/"
    ]

    rss_manager = RssManager(current_app, rss_feed_list)
    print("Fetching data from Alienvault")
    alienvault_data = rss_manager.fetch_alien_vault_data()
    rss_manager.add_alien_vault_data_to_db(alienvault_data)
    print("Fetching RSS Feeds data")
    rss_data = rss_manager.fetch_rss_data()
    rss_manager.add_rss_data_to_db(rss_data)
    return "DB updated!"


def get_data(urla):
    try:
        browser_options = ChromeOptions()
        browser_options.add_argument("--headless")  
        driver = webdriver.Chrome(options=browser_options)
        url = f"{urla}"
        driver.get(url)
        time.sleep(5)  
        page_source = driver.page_source
        driver.quit()
        soup = BeautifulSoup(page_source, "html.parser")
        text_content = soup.get_text()
        cleaned_text = re.sub(r'\s+', ' ', text_content)
        return cleaned_text.strip()
    except Exception as e:
        return "Failed to retrieve webpage due to "+str(e)