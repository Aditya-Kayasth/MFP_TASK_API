# Candidate Search API (Django)

A modular REST API designed to source candidate profiles from multiple public platforms.

---

## Setup & Installation

1. **Clone the repository**

   ```bash
   git clone https://gitlab.com/internship-task1/MFP-Task-API-V1.git
   cd candidate_api
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # Windows:
   venv\Scripts\activate

   # macOS / Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   python manage.py runserver
   ```

---

## Websites / APIs Explored & Evaluated

### PostJobFree.com (Selected)

- **Evaluation:** Identified as an open resume database that permits public search indexing.
- **Outcome:** Selected as the primary data source. Unlike some other platforms, it allows direct scraping, which helps the API maintain high availability.

### Naukri.com (Partially Integrated)

- **Evaluation:** A primary source of candidate data but direct scraping is prohibited and technically blocked.
- **Outcome:** Implemented via **Google X-Ray** (`site:naukri.com`) to legally source indexed profiles. This approach can be rate-limited by search engines; more robust tooling (e.g., `curl_cffi` or Selenium) may be needed for long-term stability.

### GitHub User API (Rejected)

- **Evaluation:** Offers a structured, authentication-friendly JSON API for user search.
- **Outcome:** Rejected for this assignment because it is biased toward technical roles and returns few or no results for non-technical professions (e.g., Marketing, Accounting), failing the requirement for a universal candidate search tool.

### Apna.co, Indeed, & Monster / Foundit (Secondary Sources)

- **Evaluation:** Major job portals with significant candidate data but lacking public developer APIs.
- **Outcome:** Integrated via **Google X-Ray** to increase data coverage. These sources are dependent on Google's index and share similar rate-limiting challenges as Naukri.

---

## API Usage

**Endpoint:** `POST /api/candidates/search`

This repository includes a test script to validate the API response without external tools like Postman. Edit the payload in the test script as needed.

### How to test locally

1. Ensure your server is running in one terminal:

   ```bash
   python manage.py runserver
   ```

2. Open another terminal and run:
   ```bash
   python test_api.py
   ```

### Example Request

**Body (JSON):**

```json
{
  "skill": "java",
  "experience": 3
}
```

### Example Response (truncated)

**Body (JSON):**

```json
{
  "status": "success",
  "count": 10,
  "candidates": [
    {
      "source": "PostJobFree",
      "name": "Candidate (Hidden)",
      "current_job_title": "Senior Java Developer with Full Stack Experience",
      "experience_years": "5+ Years",
      "skills": ["java"],
      "location": "Bangalore",
      "resume_url": "https://www.postjobfree.com/resume/ad83"
    },
    {
      "source": "Naukri (via Google)",
      "name": "Rahul V.",
      "current_job_title": "Java Backend Engineer",
      "experience_years": "4 Years",
      "skills": ["java"],
      "location": "Pune",
      "resume_url": "https://www.naukri.com/"
    }
  ]
}
```

---
