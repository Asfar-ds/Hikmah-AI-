import os
# from openai import OpenAI
from pydantic import BaseModel

from fastapi import APIRouter, HTTPException

from ..models.schema import UserProfile, JobSelection
from groq import Groq

client = Groq(api_key=os.environ.get("OPENAI_API_KEY"))

# 1. Instantiate the router
router = APIRouter()

# Initialize the OpenAI client with the API key
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# class UserProfile(BaseModel):
#     interests: str
#     background: str

# class JobSelection(BaseModel):
#     job_title: str

CAREER_PATHS_DOCUMENT = """
Career Paths — both Traditional and Modern After Drs e Nizami After completing the full 8-year Dars-e-Nizami program, you have a strong foundation in Islamic studies, logic, Arabic, Fiqh, Tafsir, Hadith, and philosophy, which opens several different career paths — both traditional and modern — depending on your interests and whether you pursue further education. 🌙 1. Traditional Religious Paths These are the most direct and common routes: a. Teaching (Madrasa / Islamic Schools) ● Role: Ustadh (teacher) of Arabic, Tafsir, Hadith, Fiqh, or Islamic history. ● Where: Madaris (Jamia), Islamic schools, online academies. ● Progression: From junior teacher to senior mufti or principal. b. Imamat & Khitabat ● Role: Imam, Khatib, or Islamic counselor in mosques and institutions. ● Skills helpful: Public speaking, community management, counseling. ● Possible extension: Work in Islamic centers abroad (UK, US, Gulf countries). c. Ifta (Mufti Course) ● Duration: 2–3 years specialization after Dars-e-Nizami. ● Role: Mufti, issuing fatawa and guiding on Shariah matters. 📘 2. Academic and Educational Fields If you pursue formal education equivalence, your options expand widely: a. University Path (HEC Equivalence) HEC Pakistan gives equivalence to Dars-e-Nizami graduates: ● Sanvia Khasa = Intermediate (FA/FSc) ● Shahadat-ul-Aaliya = BA (2 years) ● Shahadat-ul-Aalmia = MA (Arabic/Islamic Studies) ✅ After equivalence, you can: ● Apply for MPhil / PhD in Islamic Studies or Arabic. ● Join universities as lecturers or researchers. ● Study other disciplines (education, law, sociology, etc.) via bridge programs. 💼 3. Modern / Hybrid Career Paths If you combine your Dars-e-Nizami background with modern skills or degrees, you can build unique and impactful careers: a. Islamic Finance & Banking ● Additional Study: Diploma or MS in Islamic Banking / Finance. ● Institutions: IBA Karachi, INCEIF (Malaysia), AlHuda CIBE. ● Roles: Shariah advisor, compliance officer, financial consultant. b. Research & Writing ● Work as an Islamic researcher, translator, or author. ● Write for journals, online Islamic platforms, or create educational content. ● With English fluency, international opportunities open up (publishing, content creation, dawah). c. Digital Dawah / Online Education ● Launch a YouTube channel, podcast, or online Islamic course platform. ● Combine Islamic scholarship with social media and digital skills. ● Examples: English/Urdu content for youth, Quran apps, e-learning portals. d. Education Leadership ● Found or manage schools, Islamic institutes, or NGOs. ● Combine traditional knowledge with modern management or education degrees (e.g. B.Ed, MBA in education management). 🌍 4. International Opportunities Graduates with good English and digital literacy can: ● Teach Islamic studies online globally. ● Pursue scholarships abroad in Islamic Studies (Turkey, Malaysia, Saudi Arabia, UK). ● Serve as chaplains or community scholars in diaspora communities. 💡 5. Emerging Interdisciplinary Roles If you develop modern skills, you can enter new fields such as: Field Possible Roles Combine Dars-e-Nizami with… AI & Ethics Media & Communication Law & Policy Counseling Data Science, Philosophy Journalism, Digital Media LLB, Public Policy Psychology, Counselling Islamic AI Ethics consultant Religious anchor, content producer Shariah advisor, legal consultant Spiritual / family counsellor Integrated Career Paths with IT Let’s build a complete 8-year integrated roadmap for a Dars-e-Nizami student who wants to explore the IT world while continuing classical Islamic studies. The goal is to blend Deeni Taleem (Islamic knowledge) with Digital and IT skills, so that by the end of 8 years, the student is not only a qualified scholar but also a capable tech professional — ready to build apps, websites, AI tools, or digital dawah platforms. 💻 8-Year Roadmap: Dars-e-Nizami + Information Technology Integration 🌱 Years 1–2: Foundation Phase — Digital Literacy & Language 🎯 Goal: Build strong English and computer basics — your entry ticket to IT. Focus Areas: ● English communication (reading, writing, speaking) ● Computer basics: MS Office, internet, file management ● Typing in English, Urdu, Arabic ● Introduction to online learning platforms (Coursera, YouTube, Khan Academy) ● Learn basic tech ethics (Halal digital use, cyber ethics) Suggested Courses / Tools: ● “Digital Literacy” or “Google Workspace for Beginners” ● Typing tutor (Ratatype, TypingClub) ● “English for Tech” (Coursera / Alison) ● Learn to use Google Docs, Sheets, Drive Mini Projects: ● Create your first email and Google account ● Write a small Islamic blog or reflection using Word ● Make simple PowerPoint slides for Islamic topics 🌿 Years 3–4: Exploration Phase — Front-end Tech & Digital Skills 🎯 Goal: Enter the digital space with creative and technical beginner skills. Focus Areas: ● Graphic Design — Canva, Photoshop basics ● Web Design (Front-end) — HTML, CSS, basic JavaScript ● Social Media Management — post design, digital storytelling ● Basic Video Editing — CapCut, Filmora, Premiere Rush ● Digital Dawah — using tech for spreading authentic Islamic content Suggested Courses / Tools: ● “HTML & CSS for Beginners” (freeCodeCamp / W3Schools) ● “Canva Design Course” (YouTube / Coursera) ● “Digital Marketing Fundamentals” (Google Digital Garage) Mini Projects: ● Build your first simple webpage (personal profile or Islamic topic) ● Design Islamic posters or short video clips ● Start an Instagram or YouTube page sharing educational posts 🌾 Years 5–6: Integration Phase — Programming & Applied Tech 🎯 Goal: Gain coding skills and understand real-world IT applications. Focus Areas: ● Programming: Python (for beginners) ● Data & Logic: basic data analysis, problem solving ● Web Development: HTML, CSS, JS + frameworks (Bootstrap, React basics) ● Database: SQL, data handling ● Tech + Deen Integration: use coding to make Islamic tools (e.g. Quran app, Hadith searcher) Suggested Courses / Tools: ● “Python for Everybody” (University of Michigan – Coursera) ● “Full Stack Web Development” (freeCodeCamp) ● “SQL Basics” (Kaggle / W3Schools) Mini Projects: ● Build a small Quran search app using Python or HTML ● Create a portfolio website ● Automate a simple Islamic calendar or prayer time reminder system 🌺 Years 7–8: Professional Development — Specialization & Projects 🎯 Goal: Choose your IT specialization and build a professional portfolio. Possible Specializations: Path Focus Web Development Front-end + Back-end + Hosting Career Roles Web developer, freelancer App Development Android (Flutter), iOS Islamic app creator Data Science & AI Python, ML, data visualization Cybersecurity UI/UX Design Digital Dawah Tech Ethical hacking, data protection Design thinking, Figma, prototyping Content creation, app integration Add-on Tools & Frameworks: ● GitHub (for portfolio) ● React / Node.js / Django (advanced) ● Google Cloud / Firebase (hosting apps) ● Canva Pro, Figma (design) ● AI tools (ChatGPT, Midjourney, Notion) Mini Projects: AI Ethics consultant, researcher Security analyst Interface designer EdTech founder, media developer ● Build and launch a real Islamic website or app (e.g., Zakat calculator, Hadith search tool) ● Collaborate with others on GitHub ● Offer freelance services (design, coding, tutoring) ⚙ Summary Table: Year-wise IT + Dars-e-Nizami Integration Dars-e-Nizami Year IT Focus Tools / Skills Outcome 1–2 Digital foundation Computer & English Basics 3–4 MS Office, Email, Typing Graphic & Web Design Canva, HTML, CSS First website, creative design 5–6 7–8 Programming & Databases Specialization & Portfolio Python, SQL, JS React, Django, Flutter Build small apps, coding literacy Ready for IT career or freelancing 🚀 After 8 Years: Career Options When combined with Dars-e-Nizami, these IT skills can lead to: Integrated Field Islamic Tech Example Career App / Web Developer Description Create apps for Quran, Fiqh, or education Digital Media EdTech AI & Ethics Freelancing Cybersecurity Islamic YouTuber / Designer e-Learning Developer AI Researcher / Advisor Remote Developer / Designer Ethical Hacker Use design & video for education and dawah Build online Islamic courses Study Islamic perspectives on AI and morality Earn income online while teaching or studying Secure Islamic and educational data systems 🌟 Ultimate Vision By the time he graduates from Dars-e-Nizami, He will be both a qualified Aalim and a skilled IT professional,
"""

def get_job_opportunities(profile: UserProfile) -> str:
    system_prompt = (
        "You are an expert career counselor for Dars-e-Nizami students. "
        "You have been provided with a document outlining potential career paths. "
        "First, analyze the user's interests and background to see if they align with the career paths described in the document. "
        "If there is a match, base your recommendations on the document. "
        "If the user's profile does not directly match the document, you can provide suggestions based on your general knowledge, but you should still try to relate them to the Dars-e-Nizami background. "
        "Provide a numbered list of job titles."
    )
    
    user_input = (
        f"Here is the document with career paths: \n---_DOCUMENT_START---{CAREER_PATHS_DOCUMENT}---_DOCUMENT_END---\n\n"
        f"Now, consider my profile:\n"
        f"My interests are: {profile.interests}.\n"
        f"My background is: {profile.background}\n\n"
        "Based on this, what job opportunities do you recommend?"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"

def get_skillset_for_job(job: JobSelection) -> str:
    system_prompt = (
        "You are an expert career counselor. "
        "For a given job title, you will provide a detailed list of the required skills. "
        "Categorize the skills into 'Technical Skills' and 'Soft Skills'."
    )
    
    user_input = f"What are the skills required for a '{job.job_title}'?"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"


# For Testing:

# if __name__ == '__main__':
#     # Test get_job_opportunities
#     print("Testing get_job_opportunities...")
#     user_profile = UserProfile(interests="programming and AI", background="Dars-e-Nizami graduate")
#     job_opportunities = get_job_opportunities(user_profile)
#     print(job_opportunities)
#     print("-" * 20)

#     # Test get_skillset_for_job
#     print("Testing get_skillset_for_job...")
#     job_selection = JobSelection(job_title="AI & Ethics consultant")
#     skill_set = get_skillset_for_job(job_selection)
#     print(skill_set)
#     print("-" * 20)


@router.post("/opportunities")
async def opportunities(profile: UserProfile):
    try:
        response_text = get_job_opportunities(profile)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/skillset")
async def skillset(job: JobSelection):
    try:
        response_text = get_skillset_for_job(job)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

