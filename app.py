import streamlit as st
from io import BytesIO
from reportlab.pdfgen import canvas
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- Page Settings ----------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------- Custom Styling ----------

st.markdown("""
<style>
.main-title {
    font-size: 38px;
    font-weight: bold;
    text-align: center;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------

st.markdown(
    '<div class="main-title">📄 AI-Powered Resume & Career Skill Gap Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze your resume using Python, NLP and Data Science</div>',
    unsafe_allow_html=True
)

# ---------- Skills List ----------

skills = [
    "Python",
    "SQL",
    "Java",
    "C",
    "C++",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Django",
    "Flask",
    "Pandas",
    "NumPy",
    "Machine Learning",
    "Data Science",
    "Statistics",
    "Data Visualization",
    "Power BI",
    "Excel",
    "Tableau",
    "NLP"
]

# ---------- Upload Resume ----------

st.subheader("📄 Upload Resume")

uploaded_file = st.file_uploader(
    "Choose your Resume PDF",
    type=["pdf"]
)

# ---------- Job Description ----------

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the Job Description here",
    height=200
)

# ---------- Analyze ----------

if st.button("🔍 Analyze Resume"):

    if uploaded_file is None:

        st.warning("Please upload your resume PDF.")

    elif not job_description.strip():

        st.warning("Please enter a job description.")

    else:

        # ---------- Read Resume ----------

        reader = PdfReader(uploaded_file)

        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text() or ""

        # ---------- Skill Detection ----------

        resume_lower = resume_text.lower()
        job_lower = job_description.lower()

        resume_skills = [
            skill for skill in skills
            if skill.lower() in resume_lower
        ]

        job_skills = [
            skill for skill in skills
            if skill.lower() in job_lower
        ]

        # ---------- Matching Skills ----------

        matching_skills = [
            skill for skill in job_skills
            if skill in resume_skills
        ]

        missing_skills = [
            skill for skill in job_skills
            if skill not in resume_skills
        ]

        # ---------- Job Match Percentage ----------

        if len(job_skills) > 0:
            match_percentage = (
                len(matching_skills) / len(job_skills)
            ) * 100
        else:
            match_percentage = 0

        # ---------- NLP Similarity ----------

        documents = [
            resume_text,
            job_description
        ]

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        tfidf_matrix = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )

        similarity_percentage = (
            similarity[0][0] * 100
        )

        # ---------- Overall Score ----------

        overall_score = (
            match_percentage * 0.6
        ) + (
            similarity_percentage * 0.4
        )

        # ---------- Recommendation ----------

        if overall_score >= 70:
            recommendation = "Good Match"

        elif overall_score >= 40:
            recommendation = "Moderate Match"

        else:
            recommendation = "Low Match"

        # ---------- Results ----------

        st.divider()

        st.header("📊 Resume Analysis Results")

        # ---------- Score Cards ----------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="🎯 Skill Match",
                value=f"{match_percentage:.2f}%"
            )

        with col2:
            st.metric(
                label="🧠 NLP Similarity",
                value=f"{similarity_percentage:.2f}%"
            )

        with col3:
            st.metric(
                label="🏆 Overall Match",
                value=f"{overall_score:.2f}%"
            )

        # ---------- Skill Comparison ----------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Matching Skills")

            if matching_skills:

                for skill in matching_skills:
                    st.success(skill)

            else:

                st.write("No matching skills found.")

        with col2:

            st.subheader("❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:
                    st.warning(skill)

            else:

                st.success("No missing skills found!")

        # ---------- Recommendation ----------

        st.subheader("🎯 Recommendation")

        st.info(recommendation)

        # ---------- AI Skill Recommendations ----------

        st.subheader("🤖 AI Skill Recommendations")

        if missing_skills:

            for skill in missing_skills:

                st.write(
                    f"• Improve your knowledge in **{skill}**"
                )

        else:

            st.success(
                "Your skills match all the required job skills!"
            )

        # ---------- PDF Report ----------

        pdf_buffer = BytesIO()

        pdf = canvas.Canvas(pdf_buffer)

        pdf.setTitle("Resume Analysis Report")

        pdf.drawString(
            50,
            800,
            "AI-Powered Resume & Career Skill Gap Analyzer"
        )

        pdf.drawString(
            50,
            770,
            f"Skill Match: {match_percentage:.2f}%"
        )

        pdf.drawString(
            50,
            750,
            f"NLP Similarity: {similarity_percentage:.2f}%"
        )

        pdf.drawString(
            50,
            730,
            f"Overall Match: {overall_score:.2f}%"
        )

        pdf.drawString(
            50,
            690,
            "Matching Skills:"
        )

        y = 670

        for skill in matching_skills:

            pdf.drawString(
                70,
                y,
                f"- {skill}"
            )

            y -= 20

        pdf.drawString(
            50,
            y - 10,
            "Missing Skills:"
        )

        y -= 30

        for skill in missing_skills:

            pdf.drawString(
                70,
                y,
                f"- {skill}"
            )

            y -= 20

        pdf.drawString(
            50,
            y - 10,
            "Recommendation:"
        )

        pdf.drawString(
            70,
            y - 30,
            recommendation
        )

        pdf.save()

        pdf_buffer.seek(0)

        st.download_button(
            label="📄 Download PDF Analysis Report",
            data=pdf_buffer,
            file_name="resume_analysis_report.pdf",
            mime="application/pdf"
        )

        # ---------- Skill Gap Chart ----------

        st.subheader("📈 Skill Gap Analysis")

        chart_data = {
            "Matching Skills": len(matching_skills),
            "Missing Skills": len(missing_skills)
        }

        st.bar_chart(chart_data)