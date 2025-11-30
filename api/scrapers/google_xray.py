import requests
from bs4 import BeautifulSoup
import re
import time
import random
import logging

logger = logging.getLogger(__name__)


def scrape_google_xray(domain, skill):
    candidates = []
    query = f'site:{domain} "{skill}" resume'
    url = f"https://www.google.com/search?q={query}&num=20"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        time.sleep(random.uniform(2, 4)) # delay 
        response = requests.get(url, headers=headers, timeout=15)

        print("\nResponse (google x ray raw):\n",response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        
        results = soup.select("div.tF2Cxc, div.MjjYud, div.g")
        print("\nResponse (google-xray result cleaned):\n",results)
        for item in results:
            title_tag = item.find("h3")
            link = item.find("a", href=True)
            if not title_tag or not link: continue
            
            href = link["href"]
            if domain not in href: continue
            
            title = title_tag.text.strip()
            snippet_tag = item.find("div", class_="VwiC3b")
            snippet = snippet_tag.text.strip() if snippet_tag else ""
            
            combined = title + " " + snippet
            exp = "Check Profile"
            exp_match = re.search(r'(\d+(\.\d+)?\+?)\s*(years|yrs|year)', combined, re.I)
            if exp_match: exp = exp_match.group(0)

            name = "Candidate (Hidden)"
            name_match = re.match(r'^([A-Z][a-z]+ [A-Z][a-z]+)', title)
            if name_match: name = name_match.group(1)

            candidates.append({
                "source": f"{domain} (via Google)",
                "name": name,
                "current_job_title": title,
                "skills": [skill],
                "experience_years": exp,
                "summary": snippet[:200],
                "location": "India",
                "resume_url": href
            })
            
            if len(candidates) >= 15: break

    except Exception as e:
        logger.error(f"Google X-Ray failed for {domain}: {e}")

    return candidates