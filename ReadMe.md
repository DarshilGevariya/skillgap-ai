# SkillGap AI -- Intelligent Skill Assessment & Learning Planner

SkillGap AI is an AI-powered system that goes beyond resumes to **assess real proficiency**, identify **skill gaps**, and generate **personalized learning roadmaps**.

> A resume tells what you *claim* to know. SkillGap AI evaluates what you *actually* know.

---

##  Features

* **Resume Parsing** (PDF/DOCX upload)
* **Job Description Skill Extraction**
* **AI-Based Skill Assessment**
* **Dynamic Interview Questions**
* **Regenerate Questions (Interactive UX)**
* **Skill Scoring & Feedback**
* **Gap Identification**
* **Personalized Learning Plan**

  * Time estimates 
  * Curated resources 

---

## Architecture

```
Frontend (Streamlit)
        ↓
Backend API (FastAPI)
        ↓
LLM (OpenAI GPT-5.5)
```

### Flow:

1. User inputs **Job Description**
2. Uploads **Resume**
3. Backend extracts **skills**
4. AI generates **questions**
5. User answers → system evaluates
6. Final output:

   * Score
   * Gaps
   * Learning roadmap

---

##  Core Logic

### Skill Extraction

* Uses LLM to extract structured skills from JD & Resume
* Input is truncated to ensure fast and stable responses

### Assessment

* Questions generated at 3 levels:

  * Basic
  * Intermediate
  * Advanced

### Scoring

* Each answer evaluated using LLM
* Score normalized to **0–10 scale**

### Gap Detection

```python
gaps = jd_skills - resume_skills
```

### Learning Plan

* 3-week structured roadmap
* Includes:

  * Topics
  * Time estimates
  * Curated resources

---

##  Tech Stack

| Layer            | Technology              |
| ---------------- | ----------------------- |
| Frontend         | Streamlit               |
| Backend          | FastAPI                 |
| AI Model         | OpenAI GPT-5.5          |
| File Parsing     | PyPDF2, python-docx     |
| State Management | Streamlit Session State |

---

##  Project Structure

```
skillgap-ai/
│
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── utils.py
│
├── frontend/
│   ├── app.py
│
├── .env
├── requirements.txt
└── README.md
```

---

##  Setup Instructions (Local)

### 1. Clone Repository

```bash
git clone https://github.com/your-username/skillgap-ai.git
cd skillgap-ai
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Setup Environment Variables

Create `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

### 4. Run Backend

```bash
uvicorn backend.main:app --reload
```

 API Docs: http://127.0.0.1:8000/docs

---

### 5. Run Frontend

```bash
cd frontend
streamlit run app.py
```

 App: http://localhost:8501

---

##  Sample Input

### Job Description

```
Looking for a Python developer with experience in APIs and Docker.
```

### Resume

```
Experienced in Python and basic programming concepts.
```

---

##  Sample Output

*  Extracted Skills
*  Interview Questions
*  Score: 6.5 / 10
*  Gap: APIs
*  Learning Plan with time estimates

---

##  Security

* API key stored using `.env`
* Never exposed in frontend
* `.env` added to `.gitignore`

---

##  Future Improvements

* Adaptive questioning (based on previous answers)
* Skill visualization dashboard
* User authentication
* Resume scoring history
* Deployment (Render / Vercel)

---
---

##  Live Demo

> Add deployed URL here

---

##  Author

**Darshil Gevariya**
GitHub: https://github.com/DarshilGevariya

---

##  License

This project is for educational and hackathon purposes.

---

##  Final Note

SkillGap AI transforms hiring from **resume-based filtering**
to **real capability evaluation** — making it more fair, accurate, and actionable.

---
