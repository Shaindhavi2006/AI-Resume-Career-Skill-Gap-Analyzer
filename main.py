from pypdf import PdfReader
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

# ---------- Find Resume PDF ----------
pdf_files = list(Path("resumes").glob("*.pdf"))

if not pdf_files:
    print("No PDF found in resumes folder.")
    exit()

pdf_path = pdf_files[0]

print("Using resume:", pdf_path)

# ---------- Read Resume ----------
reader = PdfReader(pdf_path)

resume_text = ""

for page in reader.pages:
    resume_text += page.extract_text() or ""


# ---------- Read Job Description ----------
with open("job_description.txt", "r", encoding="utf-8") as file:
    job_text = file.read()


# ---------- Skills ----------
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


# ---------- Find Resume Skills ----------
resume_lower = resume_text.lower()
job_lower = job_text.lower()

resume_skills = []

for skill in skills:
    if skill.lower() in resume_lower:
        resume_skills.append(skill)


# ---------- Find Job Skills ----------
job_skills = []

for skill in skills:
    if skill.lower() in job_lower:
        job_skills.append(skill)


# ---------- Matching Skills ----------
matching_skills = []

for skill in job_skills:
    if skill.lower() in [s.lower() for s in resume_skills]:
        matching_skills.append(skill)


# ---------- Missing Skills ----------
missing_skills = []

for skill in job_skills:
    if skill.lower() not in [s.lower() for s in resume_skills]:
        missing_skills.append(skill)


# ---------- Match Percentage ----------
if len(job_skills) > 0:
    match_percentage = (len(matching_skills) / len(job_skills)) * 100
else:
    match_percentage = 0


# ---------- Results ----------
print("\n===== AI RESUME SKILL GAP ANALYZER =====")

print("\nResume Skills:")
print(resume_skills)

print("\nJob Required Skills:")
print(job_skills)

print("\nMatching Skills:")
print(matching_skills)

print("\nMissing Skills:")
print(missing_skills)

print("\nJob Match Percentage:")
print(f"{match_percentage:.2f}%")
if match_percentage>=70:
    recommendation="Good Match"
elif match_percentage>=40:
    recommendation="Moderate Match"
else:
    recommendation="Low Match"
print("\nRecommendation:")
print(recommendation)

# ---------- NLP Similarity ----------

documents = [resume_text, job_text]

vectorizer = TfidfVectorizer(stop_words="english")

tfidf_matrix = vectorizer.fit_transform(documents)

similarity = cosine_similarity(
    tfidf_matrix[0:1],
    tfidf_matrix[1:2]
)

similarity_percentage = similarity[0][0] * 100

print("\nNLP Resume-JD Similarity Score:")
print(f"{similarity_percentage:.2f}%")

# ---------- Overall Match Score ----------

overall_score = (match_percentage * 0.6) + (similarity_percentage * 0.4)

print("\nOverall Resume-JD Match Score:")
print(f"{overall_score:.2f}%")

# ---------- AI Skill Recommendations ----------

print("\nAI Skill Recommendations:")

if missing_skills:
    for skill in missing_skills:
        print(f"- Improve your knowledge in {skill}")
else:
    print("- Your skills match all the required job skills!")

import matplotlib.pyplot as plt

labels = ["Matching Skills", "Missing Skills"]
values = [len(matching_skills), len(missing_skills)]

plt.figure(figsize=(7, 5))
plt.bar(labels, values)

plt.title("Resume Skill Gap Analysis")
plt.xlabel("Skill Category")
plt.ylabel("Number of Skills")
# ---------- Overall Match Score Visualization ----------

plt.figure(figsize=(7, 5))

plt.bar(
    ["Overall Match Score"],
    [overall_score]
)

plt.ylim(0, 100)

plt.title("Overall Resume-JD Match Score")
plt.ylabel("Score (%)")

plt.show()

