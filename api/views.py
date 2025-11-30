from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

from .scrapers import scrape_postjobfree, scrape_google_xray, parse_experience

logger = logging.getLogger(__name__)


def matches_skill(candidate_skills, search_skill):
    search_skill_lower = search_skill.lower()
    return any(search_skill_lower in skill.lower() for skill in candidate_skills)

@api_view(['POST'])
def search_candidates(request):
    skill = request.data.get("skill")
    experience = request.data.get("experience")

    if not skill:
        return Response({"error": "Missing skill"}, status=400)
    
    try:
        experience = int(experience)
    except:
        return Response({"error": "Experience must be a number"}, status=400)

    logger.info(f"Received search request: Skill='{skill}', Exp={experience}")

    # 1. Scraping Phase (Expanded to 5 Sources)
    results = []
    
    logger.info("Starting PostJobFree scrape...")
    results += scrape_postjobfree(skill)
    
    logger.info("Starting Naukri scrape (via Google)...")
    results += scrape_google_xray("naukri.com", skill)
    
    logger.info("Starting Apna scrape (via Google)...")
    results += scrape_google_xray("apna.co", skill)

    # --- NEW SOURCES ---
    logger.info("Starting Indeed scrape (via Google)...")
    results += scrape_google_xray("in.indeed.com", skill) # Targeting Indeed India

    logger.info("Starting Monster/Foundit scrape (via Google)...")
    results += scrape_google_xray("foundit.in", skill) # Monster is now Foundit
    # -------------------

    # 2. Filtering Phase
    filtered = []
    for c in results:
        exp_num = parse_experience(c["experience_years"])
        
        # Lenient Experience Check
        is_exp_good = (exp_num is None) or (exp_num >= experience)

        # Strict Skill Check
        is_skill_good = matches_skill(c["skills"], skill)

        if is_exp_good and is_skill_good:
            filtered.append(c)

    # 3. Fallback Phase
    if not filtered:
        logger.warning("No candidates found via scraping. Returning mock data.")
        filtered = [{
            "source": "Mock Data",
            "name": "Amit Sharma",
            "current_job_title": f"Senior {skill} Developer",
            "experience_years": f"{experience}+ Years",
            "skills": [skill],
            "location": "NA",
            "summary": "Fallback mock profile generated because live scraping returned 0 results.",
            "resume_url": "https://naukri.com/mock-profile"
        }]

    logger.info(f"Returning {len(filtered)} candidates.")
    
    return Response({
        "status": "success",
        "count": len(filtered),
        "candidates": filtered
    })