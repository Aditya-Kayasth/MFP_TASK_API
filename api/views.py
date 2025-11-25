from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

from .scrapers import scrape_postjobfree, scrape_google_xray,parse_experience

logger = logging.getLogger(__name__)

@api_view(['POST'])
def search_candidates(request):
    skill = request.data.get("skill")
    experience = request.data.get("experience")

    # Validation
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
    
    logger.info("Starting Naukri scrape...")
    results += scrape_google_xray("naukri.com", skill)
    
    logger.info("Starting Apna scrape...")
    results += scrape_google_xray("apna.co", skill)


    filtered = []

    for c in results:
        exp_num = parse_experience(c["experience_years"])
        if exp_num is None: 
            filtered.append(c)
        elif exp_num >= experience:
            filtered.append(c)

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