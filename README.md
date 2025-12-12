# 🔥 AI Resume Analyzer & ATS Score Predictor

An end-to-end **AI-powered ATS (Applicant Tracking System) Resume Analyzer** that:

- Extracts text from **PDF / Image resumes** using OCR  
- Uses **NLP + ML** to extract skills and match them with a **Job Description (JD)**  
- Predicts an **ATS score (0–100)** using a trained ML model  
- Highlights **missing + recommended skills**  
- Generates **smart suggestions** to improve the resume  
- Provides a **downloadable ATS report (PDF)**  
- Includes a basic **Resume Rewriter AI** to rewrite the resume based on the JD  

> _AI model engineered & trained by **Manish**_

---

## 🚀 Features

- 📄 **Resume Upload** → Supports PDF, PNG, JPG, JPEG  
- 🔍 **OCR + Parsing** → Handles both digital & scanned resumes  
- 🧠 **Skill Extraction (NLP):**  
  - Extracts skills from Resume & Job Description  
  - Highlights overlap + missing skills  
- 🎯 **ATS Score Prediction (ML):**  
  - Trained regression model  
  - Outputs **0–100 ATS score**  
- 🔎 **Resume–JD Semantic Similarity Score**  
- 💡 **Smart Suggestions Engine**  
- 📥 **Downloadable ATS Report (PDF)**  
- ✨ **Resume Rewriter AI**  
- 🎨 **Modern UI (Glassmorphism)**  

---

## 🏗 Tech Stack

**Frontend/UI:** Streamlit  
**Language:** Python 3.11+  
**ML/NLP:**  
- scikit-learn  
- spaCy / custom NLP  
- TF-IDF / Embedding similarity  
**OCR:**  
- pdfplumber  
- PyMuPDF (`fitz`)  
- pytesseract  
**Other:**  
- reportlab  
- pandas, numpy  

---

## 📂 Project Structure

```bash
AI-RESUME-ATS/
│
├── app.py                   # Main Streamlit app
├── requirements.txt         # Dependencies
├── training_data.csv        # Synthetic ATS training dataset
│
├── models/
│   ├── ats_model.pkl        # Trained ATS model
│   └── vectorizer.pkl       # TF-IDF/Vectorizer
│
├── utils/
│   ├── __init__.py
│   ├── ats_model.py         # ATS scoring logic
│   ├── ocr.py               # Resume OCR
│   ├── parser.py            # Optional parsing utilities
│   ├── skill_extractor.py   # Advanced skill extractor
│   ├── similarity.py        # Resume–JD semantic similarity
│   ├── suggestions.py       # Smart suggestions engine
│   ├── report_gen.py        # PDF report generator
│   └── rewriter.py          # Resume Rewriter AI
│
├── .streamlit/
│   └── config.toml          # UI theme settings
│
├── Dockerfile               # Optional for container deployment
├── Procfile                 # Optional for cloud hosting
└── README.md

How ATS Scoring Works

Resume + JD text is cleaned

Converted into numerical vectors (TF-IDF or embeddings)

ATS model predicts a score from 0–100

ATS Score	Interpretation
0–40	Weak match
40–60	Average / improvable
60–80	Good match
80–100	Excellent / strong fit
🧪 Example Workflow

Upload resume (PDF / JPG / PNG)

Paste Job Description

Click Analyze Resume

View:

Extracted text

Skills match

Missing skills

Similarity score

ATS score

Download ATS report (PDF)

Improve using Resume Rewriter AI

🚀 Deployment (Streamlit Cloud)

Push repo to GitHub

Go to: https://share.streamlit.io

Create a new app

Set:

Main file: app.py


Ensure:

requirements.txt includes all libraries

models/ats_model.pkl & vectorizer.pkl exist in repo

🧾 Future Improvements

Upgrade Rewriter AI → Full LLM support

Add radar/bar charts for visual scoring

Multi-resume bulk analyzer

User accounts + save history

👤 Author

Manish
B.Tech – Artificial Intelligence & Data Science

“AI-powered tools that help candidates understand and improve their resumes for real-world ATS systems.”

© Copyright

© 2025 Manish Pal
This project is intended for educational and personal use.
Unauthorized commercial reuse or redistribution is prohibited.
