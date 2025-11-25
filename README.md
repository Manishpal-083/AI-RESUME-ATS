# 🔥 AI Resume Analyzer & ATS Score Predictor

An end-to-end **AI-powered ATS (Applicant Tracking System) Resume Analyzer** that:
- Extracts text from **PDF / Image resumes** using OCR  
- Uses **NLP + ML** to extract skills and match them with a **Job Description (JD)**  
- Predicts an **ATS score (0–100)** using a trained ML model  
- Highlights **missing / recommended skills**  
- Generates **smart suggestions** to improve the resume  
- Provides a **downloadable ATS report (PDF)**  
- Includes a basic **Resume Rewriter AI** to adapt the resume to a given JD  

> _AI model engineered & trained by **Manish**_

---

## 🚀 Features

- 📄 **Resume Upload** – Supports PDF, PNG, JPG, JPEG  
- 🔍 **OCR + Parsing** – Extracts text from regular and scanned resumes  
- 🧠 **Skill Extraction (NLP)**  
  - Extracts skills from both Resume & Job Description  
  - Shows overlap + missing skills  
- 🎯 **ATS Score Prediction (ML)**  
  - Trained on synthetic ATS dataset  
  - Outputs score from **0 – 100**  
- 📊 **Resume–JD Similarity Score**  
  - Shows semantic similarity between resume and JD  
- 💡 **Smart Suggestions**  
  - Suggests improvements like:
    - Add more impact
    - Use numbers / metrics
    - Add projects / GitHub links
- 📥 **ATS Report Download (PDF)**  
  - Complete summary of:
    - Similarity
    - ATS score
    - Missing skills
    - Suggestions
- ✨ **Resume Rewriter AI (Basic)**  
  - Generates an improved resume-style text aligned with the JD  
- 🎨 **Modern UI (Glassmorphism + Animations)**  
  - Clean, modern look using custom CSS  
  - Skill chips, glass cards, and animated progress bar  

---

## 🏗 Tech Stack

- **Frontend / UI**: [Streamlit](https://streamlit.io/)  
- **Language**: Python 3.11+  
- **ML / NLP**:  
  - scikit-learn (ATS model)  
  - spaCy / custom NLP for skill extraction  
  - Sentence similarity (embeddings / TF-IDF based)  
- **OCR**:  
  - `pdfplumber`, `PyMuPDF (fitz)`, `pytesseract` + `Pillow`  
- **Other**:  
  - `reportlab` for PDF report generation  
  - `pandas`, `numpy` for data handling  

---

## 📂 Project Structure

```bash
AI-RESUME-ATS/
│
├── app.py                   # Main Streamlit app
├── requirements.txt         # Python dependencies
├── training_data.csv        # Synthetic ATS training dataset
├── models/
│   ├── ats_model.pkl        # Trained ATS model
│   └── vectorizer.pkl       # Vectorizer for ATS model
│
├── utils/
│   ├── __init__.py
│   ├── ats_model.py         # Train & predict ATS score
│   ├── ocr.py               # Resume OCR & text extraction
│   ├── parser.py            # (Optional) extra parsing utilities
│   ├── skill_extractor.py   # Advanced skill extraction logic
│   ├── similarity.py        # Resume–JD similarity scoring
│   ├── suggestions.py       # Rule-based resume suggestions
│   ├── report_gen.py        # PDF report generation
│   ├── rewriter.py          # Basic Resume Rewriter AI
│   └── train_ats.py         # ATS model training script
│
├── .streamlit/
│   └── config.toml          # Streamlit theme / settings
├── .gitignore
├── Dockerfile               # (Optional) For container deployment
├── Procfile                 # (Optional) For platform deployment
└── README.md


🧠 How ATS Scoring Works

Resume + JD text are cleaned and combined.

TF-IDF / embeddings are used to convert text to numerical vectors.

A regression model (scikit-learn) predicts a score between 0–100.

Score is interpreted as:

ATS Score	Interpretation
0–40	Weak match
40–60	Average / improvable
60–80	Good match
80–100	Excellent / strong fit
🧪 Example Workflow

Upload your resume (PDF / JPG / PNG).

Paste a Job Description from LinkedIn / Naukri / Indeed.

Click “Analyze Resume”.

View:

Extracted resume text

Skills vs JD skills

Missing skills

Similarity score

ATS score

Download the ATS report (PDF).

Use Resume Rewriter AI to generate an improved version aligned with the JD.

🚀 Deployment (Streamlit Community Cloud)

You can deploy this project easily using Streamlit Community Cloud
:

Push this repository to GitHub.

Go to share.streamlit.io (Streamlit Cloud).

Click “New app”.

Select your GitHub repo and branch.

Set:

Main file: app.py

(Optional) Python version via runtime.txt if needed.

Deploy.

Make sure:

requirements.txt contains all the needed libraries.

models/ats_model.pkl and models/vectorizer.pkl are committed so the app can load the ATS model.

🧾 Future Improvements

Replace basic rewriter with a full LLM-powered API (OpenAI / etc.).

Add charts (radar, bar, donut) for skill & score visualization.

Support multiple resumes vs one JD.

User accounts and history (save previous analyses).

👤 Author

Manish
B.Tech Artificial Intelligence & Data Science

“AI-powered tools that actually help candidates understand and improve their resumes for real-world ATS systems.