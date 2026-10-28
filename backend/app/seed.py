from sqlalchemy import select
from .models import Course, Opportunity

COURSES = [
    ("CSC 226", "Software Design & Implementation", "Computer Science", 3, 24, "Dr. Scott Heggen", "MWF · 10:00 AM", "Design, implement, test, and maintain software systems."),
    ("MAT 216", "Discrete Mathematics", "Mathematics", 3, 30, "Faculty TBA", "TR · 1:00 PM", "Logic, proofs, graphs, sets and combinatorics."),
    ("CSC 236", "Data Structures", "Computer Science", 3, 22, "Faculty TBA", "TR · 9:30 AM", "Arrays, trees, hashing, algorithms and complexity."),
    ("MAT 135", "Calculus I", "Mathematics", 4, 28, "Faculty TBA", "MWF · 9:00 AM", "Limits, derivatives and applications."),
    ("ENG 103", "English & American Culture", "Humanities", 3, 30, "Faculty TBA", "MWF · 11:00 AM", "Academic writing and cultural studies."),
    ("CSC 330", "Database Systems", "Computer Science", 3, 20, "Faculty TBA", "TR · 2:00 PM", "Relational databases, SQL and schema design."),
]
OPPORTUNITIES = [
    ("Undergraduate Research Assistant", "Campus Research Lab", "Research", "On campus", "Support faculty research with Python data analysis and reproducible reports.", ""),
    ("Software Engineering Internship", "Demo Tech Company", "Internship", "Remote", "Build and test backend APIs alongside a software engineering team.", ""),
    ("Open Source Contributors Meetup", "Campus Computing Club", "Event", "On campus", "Collaborate on beginner-friendly open-source issues and Git workflows.", ""),
    ("Community Coding Tutor", "Local Learning Center", "Volunteer", "Berea, KY", "Help students learn Python and foundational web development.", ""),
    ("Data Visualization Hackathon", "Student Innovation Hub", "Hackathon", "Hybrid", "Prototype a data-driven solution in a weekend team challenge.", ""),
]

def seed(db):
    if not db.scalar(select(Course.id).limit(1)):
        db.add_all([Course(code=c, title=t, department=d, credits=cr, capacity=cap, instructor=i, schedule=s, description=desc) for c,t,d,cr,cap,i,s,desc in COURSES])
    if not db.scalar(select(Opportunity.id).limit(1)):
        db.add_all([Opportunity(title=t, organization=o, kind=k, location=l, description=d, url=u) for t,o,k,l,d,u in OPPORTUNITIES])
    db.commit()
