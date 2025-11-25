from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

def generate_report(resume_skills, jd_skills, missing, similarity, ats_score, suggestions):
    pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    c = canvas.Canvas(pdf_path, pagesize=letter)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "AI ATS Resume Report")

    c.setFont("Helvetica", 12)
    y = 720
    c.drawString(50, y, f"Similarity Score: {similarity:.3f}")
    y -= 20
    c.drawString(50, y, f"ATS Score: {ats_score:.2f}/100")

    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Missing Skills:")
    y -= 20
    c.setFont("Helvetica", 12)
    for s in missing:
        c.drawString(60, y, f"- {s}")
        y -= 18

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Improvement Suggestions:")
    y -= 20
    c.setFont("Helvetica", 12)
    for s in suggestions:
        c.drawString(60, y, f"- {s}")
        y -= 18

    c.save()
    return pdf_path
