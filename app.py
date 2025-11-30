import streamlit as st
import os
import tempfile
from utils.ocr import extract_text
from utils.skill_extractor import extract_skills_advanced
from utils.ats_model import predict_ats_score
from utils.similarity import similarity_score
from utils.suggestions import generate_suggestions
from utils.report_gen import generate_report
from utils.rewriter import rewrite_resume

# ---------- BASIC CONFIG ----------
st.set_page_config(page_title="AI ATS Analyzer Pro", layout="wide")

# ---------- UI THEME (Glassmorphism CSS) ----------
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #1f1c2c, #928dab);
    font-family: 'Inter', sans-serif;
}

/* Glass card */
.glass-card {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    padding: 20px;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    margin-bottom: 20px;
    animation: fadeIn 0.8s ease-in-out;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Skill Chips */
.skill-chip {
    display: inline-block;
    padding: 6px 12px;
    background: rgba(255,255,255,0.15);
    margin: 4px;
    border-radius: 12px;
    color: white;
    font-size: 14px;
}

.skill-chip-missing {
    display: inline-block;
    padding: 6px 12px;
    background: rgba(255,0,0,0.4);
    margin: 4px;
    border-radius: 12px;
    color: white;
    font-size: 14px;
}

.subtitle {
    color: #f5f5f5;
    font-size: 14px;
    margin-top: -8px;
    margin-bottom: 20px;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("🚀 AI-Powered ATS Resume Analyzer")
st.markdown("<p class='subtitle'>AI model engineered & trained by Manish</p>", unsafe_allow_html=True)# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align: center; font-size: 50px; font-weight: 900; 
            background: linear-gradient(90deg, #8f94fb, #4e54c8, #00d4ff);
            -webkit-background-clip: text; color: transparent;'>
    🚀 AI-Powered ATS Resume Analyzer
</h1>
""", unsafe_allow_html=True)

st.markdown("<p class='subtitle' style='text-align:center;'>AI model engineered & trained by Manish</p>", unsafe_allow_html=True)


uploaded_file = st.file_uploader("📄 Upload Resume (PDF/PNG/JPG):", type=["pdf", "png", "jpg", "jpeg"])
jd_text = st.text_area("📝 Paste Job Description Here:", height=200)

# ---------- MAIN PROCESSING ----------
if st.button("Analyze Resume"):

    if not uploaded_file:
        st.error("Upload a resume first.")
        st.stop()

    if not jd_text.strip():
        st.error("Paste a job description.")
        st.stop()

    # Save temporary file with correct suffix
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    # OCR -> Resume Text
    resume_text = extract_text(temp_path)

    # ---------- SKILL EXTRACTION ----------
    resume_skills = extract_skills_advanced(resume_text)
    jd_skills = extract_skills_advanced(jd_text)
    missing = sorted(list(set(jd_skills) - set(resume_skills)))

    # store stuff in session for rewriter & other actions
    st.session_state["resume_text"] = resume_text
    st.session_state["jd_text"] = jd_text
    st.session_state["resume_skills"] = resume_skills
    st.session_state["jd_skills"] = jd_skills
    st.session_state["missing_skills"] = missing

    # ---------- GLASS CARD: Extracted Text ----------
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📌 Extracted Resume Text")
    st.text_area("Resume Content Preview:", resume_text[:2000], height=200)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- GLASS CARD: Skills ----------
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🧠 Skill Extraction & Matching")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Resume Skills")
        for s in resume_skills:
            st.markdown(f"<span class='skill-chip'>{s}</span>", unsafe_allow_html=True)

    with col2:
        st.markdown("### JD Skills")
        for s in jd_skills:
            st.markdown(f"<span class='skill-chip'>{s}</span>", unsafe_allow_html=True)

    st.subheader("🚨 Missing / Recommended Skills")
    if missing:
        for s in missing:
            st.markdown(f"<span class='skill-chip-missing'>{s}</span>", unsafe_allow_html=True)
    else:
        st.success("Perfect! No missing skills 🎉")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- SIMILARITY ----------
    sim = similarity_score(resume_text[:2000], jd_text[:2000])

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📊 Resume-JD Similarity")
    st.metric("Similarity Score", f"{sim:.3f}")
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- ATS SCORE ----------
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🎯 Predicted ATS Score")

    try:
        ats_score = predict_ats_score(resume_text, jd_text)
        st.progress(int(ats_score))
        st.success(f"ATS Score: {ats_score:.2f}/100")
    except Exception:
        ats_score = 0
        st.warning("ATS model not trained!")

    st.session_state["ats_score"] = ats_score
    st.session_state["similarity"] = sim

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- SUGGESTIONS ----------
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("💡 Smart Resume Suggestions")

    suggestions = generate_suggestions(resume_text, jd_text, resume_skills, jd_skills)
    st.session_state["suggestions"] = suggestions

    for s in suggestions:
        st.write(f"✔ {s}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- PDF REPORT ----------
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📥 Download Full ATS Report")

    pdf_path = generate_report(resume_skills, jd_skills, missing, sim, ats_score, suggestions)
    with open(pdf_path, "rb") as f:
        st.download_button("Download ATS Report (PDF)", f, file_name="ATS_Report.pdf")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- RESUME REWRITER ----------
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("✨ Resume Rewriter AI")

if "resume_text" not in st.session_state or "jd_text" not in st.session_state:
    st.info("Pehle upar se 'Analyze Resume' chalao, phir yaha Resume Rewriter use karo 🙂")
else:
    if st.button("Rewrite My Resume for This JD"):
        rewritten = rewrite_resume(
            st.session_state["resume_text"],
            st.session_state["jd_text"],
        )
        st.text_area("📄 Improved Resume Version", rewritten, height=300)

st.markdown("</div>", unsafe_allow_html=True)
import streamlit as st
import os
import tempfile
from utils.ocr import extract_text
from utils.skill_extractor import extract_skills_advanced
from utils.ats_model import predict_ats_score
from utils.similarity import similarity_score
from utils.suggestions import generate_suggestions
from utils.report_gen import generate_report
from utils.rewriter import rewrite_resume

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI ATS Analyzer Pro",
    layout="wide",
    page_icon="🚀"
)

# ---------------------------------------------------------
# PARTICLE BACKGROUND + MODERN CSS
# ---------------------------------------------------------
st.markdown("""
<style>
/* ---- Particle Background ---- */
#particles-js {
  position: fixed;
  width: 100%;
  height: 100%;
  background: #0f051d;
  top: 0;
  left: 0;
  z-index: -1;
}

/* ---- Glassmorphic Cards ---- */
.glass-card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 22px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.20);
    margin-bottom: 25px;
    animation: fadeIn 0.8s ease-in-out;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.45);
}

/* ---- Header Title ---- */
.big-title {
    font-size: 52px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #8f94fb, #4e54c8, #00d4ff);
    -webkit-background-clip: text;
    color: transparent;
    animation: glow 3s ease-in-out infinite;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #ddd;
    margin-top: -10px;
    margin-bottom: 30px;
    opacity: 0.85;
}

/* ---- Animations ---- */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes glow {
  0% { text-shadow: 0 0 6px #4e54c8; }
  50% { text-shadow: 0 0 20px #00d4ff; }
  100% { text-shadow: 0 0 6px #4e54c8; }
}

/* ---- Skill Chips ---- */
.skill-chip {
    display: inline-block;
    padding: 7px 14px;
    background: rgba(0, 194, 255, 0.25);
    margin: 4px;
    border-radius: 12px;
    color: #e8f8ff;
    border: 1px solid #00d4ff;
    font-size: 14px;
}

.skill-chip-missing {
    display: inline-block;
    padding: 7px 14px;
    background: rgba(255,0,0,0.35);
    margin: 4px;
    border-radius: 12px;
    color: white;
    border: 1px solid red;
    font-size: 14px;
}

/* Buttons Neon */
.stButton button {
    background: linear-gradient(90deg, #4e54c8, #8f94fb);
    border-radius: 10px;
    padding: 10px 18px;
    color: white;
    border: none;
    font-size: 16px;
    transition: 0.3s;
}
.stButton button:hover {
    transform: scale(1.07);
    box-shadow: 0px 0px 15px #8f94fb;
}

/* Footer */
.footer {
    text-align: center;
    color: #aaa;
    margin-top: 40px;
    padding: 10px;
    font-size: 14px;
}
</style>

<!-- Particle.js container -->
<div id="particles-js"></div>

<!-- Load Particle.js -->
<script src="https://cdn.jsdelivr.net/npm/particles.js"></script>

<script>
particlesJS.load('particles-js',
  'https://raw.githubusercontent.com/VincentGarreau/particles.js/master/demo/particles.json',
  function(){ console.log('particles loaded.'); });
</script>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown("<h1 class='big-title'>🚀 AI ATS Analyzer Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Engineered & Designed by <b>Manish Pal</b> • Powered by AI Intelligence</p>", unsafe_allow_html=True)


# ---------------------------------------------------------
# INPUTS
# ---------------------------------------------------------
uploaded_file = st.file_uploader("📄 Upload Resume (PDF / PNG / JPG):", type=["pdf", "png", "jpg", "jpeg"])
jd_text = st.text_area("📝 Paste Job Description", height=180)

st.write("")


# ---------------------------------------------------------
# MAIN ANALYSIS BUTTON
# ---------------------------------------------------------
if st.button("🔍 Analyze Resume"):

    if not uploaded_file:
        st.error("⚠️ Please upload a resume file.")
        st.stop()

    if not jd_text.strip():
        st.error("⚠️ Job description missing!")
        st.stop()

    # Temporary file store
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    resume_text = extract_text(temp_path)

    # SKILL EXTRACTION
    resume_skills = extract_skills_advanced(resume_text)
    jd_skills = extract_skills_advanced(jd_text)
    missing = sorted(list(set(jd_skills) - set(resume_skills)))

    st.session_state.update({
        "resume_text": resume_text,
        "jd_text": jd_text,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "missing_skills": missing
    })


    # ---------------------------------------------------------
    # EXTRACTED RESUME TEXT
    # ---------------------------------------------------------
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📌 Extracted Resume Text")
    st.text_area("Resume Preview:", resume_text[:2000], height=200)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SKILLS
    # ---------------------------------------------------------
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🧠 Skill Matching")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Resume Skills")
        for s in resume_skills:
            st.markdown(f"<span class='skill-chip'>{s}</span>", unsafe_allow_html=True)

    with col2:
        st.markdown("### JD Skills")
        for s in jd_skills:
            st.markdown(f"<span class='skill-chip'>{s}</span>", unsafe_allow_html=True)

    st.markdown("### 🚨 Missing / Recommended Skills")
    if missing:
        for s in missing:
            st.markdown(f"<span class='skill-chip-missing'>{s}</span>", unsafe_allow_html=True)
    else:
        st.success("Perfect match! No missing skills 🎉")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SIMILARITY SCORE
    # ---------------------------------------------------------
    sim = similarity_score(resume_text[:2000], jd_text[:2000])

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📊 Resume ↔ JD Similarity Score")
    st.metric("Similarity", f"{sim:.3f}")
    st.markdown("</div>", unsafe_allow_html=True)


    # ---------------------------------------------------------
    # ATS SCORE
    # ---------------------------------------------------------
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🎯 ATS Score Prediction")

    try:
        ats_score = predict_ats_score(resume_text, jd_text)
        st.progress(int(ats_score))
        st.success(f"ATS Score: {ats_score:.1f} / 100")
    except:
        st.warning("ATS ML Model Not Available")
        ats_score = 0

    st.session_state["ats_score"] = ats_score
    st.session_state["similarity"] = sim

    st.markdown("</div>", unsafe_allow_html=True)



    # ---------------------------------------------------------
    # SUGGESTIONS
    # ---------------------------------------------------------
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("💡 AI Suggestions to Improve Your Resume")

    suggestions = generate_suggestions(resume_text, jd_text, resume_skills, jd_skills)
    st.session_state["suggestions"] = suggestions

    for s in suggestions:
        st.write(f"✔ {s}")

    st.markdown("</div>", unsafe_allow_html=True)


    # ---------------------------------------------------------
    # PDF REPORT DOWNLOAD
    # ---------------------------------------------------------
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📥 Download Full ATS Report")

    pdf_path = generate_report(resume_skills, jd_skills, missing, sim, ats_score, suggestions)
    with open(pdf_path, "rb") as f:
        st.download_button("⬇️ Download ATS Report (PDF)", f, file_name="ATS_Report.pdf")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# RESUME REWRITER
# ---------------------------------------------------------
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("✨ AI Resume Rewriter")

if "resume_text" not in st.session_state:
    st.info("⚠️ First Analyze your resume above, then rewrite here.")
else:
    if st.button("⚡ Rewrite My Resume for this JD"):
        rewritten = rewrite_resume(
            st.session_state["resume_text"],
            st.session_state["jd_text"],
        )
        st.text_area("📄 Improved Resume Version", rewritten, height=300)

st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# FOOTER WITH CREDIT
# ---------------------------------------------------------
st.markdown("""
<div class="footer">
    <br>
    © 2025 <b>Manish Pal</b> • AI ATS Analyzer Pro • All Rights Reserved <br>
    Designed with ❤️ & Intelligence
</div>
""", unsafe_allow_html=True)