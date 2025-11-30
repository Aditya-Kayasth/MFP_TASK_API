import requests
from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)

def scrape_postjobfree(skill):
    candidates = []
    url = f"https://www.postjobfree.com/resumes?q={skill}&l=India"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        #print("\nResponse (postjobfree):\n",response.text)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all("a"):
                href = link.get("href", "")
                if '/resume/' not in href or href.endswith("/resume/"):
                    continue

                title = link.text.strip()
                if not title: continue

                parent = link.find_parent()
                snippet = ""
                if parent:
                    snippet = parent.get_text(" ", strip=True).replace(title, "").strip()

                combined = title + " " + snippet
                exp = "Check Profile"
                match = re.search(r'(\d+(\.\d+)?\+?)\s*(years|yrs|year)', combined, re.I)
                if match:
                    exp = match.group(0)

                location = "India"
                loc_match = re.search(r'(Mumbai|Delhi|Bangalore|Chennai|Kolkata|Pune|Hyderabad|Ahmedabad|Jaipur|Bengaluru)', combined, re.I)
                if loc_match:
                    location = loc_match.group(0).title()

                candidates.append({
                    "source": "PostJobFree",
                    "name": "Candidate (Hidden)",
                    "current_job_title": title,
                    "skills": [skill],
                    "experience_years": exp,
                    "summary": snippet[:200],
                    "location": location,
                    "resume_url": "https://www.postjobfree.com" + href
                })
                
                if len(candidates) >= 15: break
                
    except Exception as e:
        logger.error(f"PostJobFree scraping error: {e}")

    return candidates


def parse_experience(exp_str):
    if not exp_str or exp_str == "Check Profile":
        return None
    match = re.search(r'(\d+)', exp_str)
    if match:
        return int(match.group(1))
    return None