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

 
    results = []
    
    logger.info("Starting PostJobFree scrape...")
    results += scrape_postjobfree(skill)
    
    logger.info("Starting Naukri scrape (via Google)...")
    results += scrape_google_xray("naukri.com", skill)
    
    logger.info("Starting Apna scrape (via Google)...")
    results += scrape_google_xray("apna.co", skill)

   
    logger.info("Starting Indeed scrape (via Google)...")
    results += scrape_google_xray("in.indeed.com", skill) 

    logger.info("Starting Monster/Foundit scrape (via Google)...")
    results += scrape_google_xray("foundit.in", skill) 
    # -------------------

    filtered = []
    for c in results:
        exp_num = parse_experience(c["experience_years"])
    
        is_exp_good = (exp_num is None) or (exp_num >= experience)

    
        is_skill_good = matches_skill(c["skills"], skill)

        if is_exp_good and is_skill_good:
            filtered.append(c)

   
    if not filtered:
        logger.warning("No candidates found via scraping. Returning mock data.")
        filtered = [{
        "status": "success",
        "count": 0,
        "candidates": [],
        "message": "No candidates found. PostJobFree returned no matches. Google X-Ray sources are blocked by bot detection."
    }]

    logger.info(f"Returning {len(filtered)} candidates.")
    
    return Response({
        "status": "success",
        "count": len(filtered),
        "candidates": filtered
    })