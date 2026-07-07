"""
School Management System — Streamlit UI
Wraps the original student/teacher management logic in a clean web interface.
Run with:  streamlit run school_app.py
"""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------
# Data layer (same JSON database approach as the original script)
# ----------------------------------------------------------------------

DATABASE = "school.json"


def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE, "r") as f:
            content = f.read()
            if content:
                return json.loads(content)
    return {"student": [], "teacher": []}


def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)


if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data


def persist():
    save_data(data)


def validate_email(email: str) -> bool:
    return "@" in email and "." in email


def find_student(roll_no):
    for s in data["student"]:
        if s["roll_no"] == roll_no:
            return s
    return None


def find_teacher(employee_id):
    for t in data["teacher"]:
        if t["employee_id"] == employee_id:
            return t
    return None


# ----------------------------------------------------------------------
# Page config & styling
# ----------------------------------------------------------------------

st.set_page_config(
    page_title="School Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .main > div { padding-top: 1.5rem; }
        .app-title {
            font-size: 2.1rem;
            font-weight: 800;
            margin-bottom: 0;
            color: #1f2937;
        }
        .app-subtitle {
            color: #6b7280;
            margin-top: 0.1rem;
            margin-bottom: 1.5rem;
        }
        .stat-card {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            padding: 1.1rem 1.3rem;
            border-radius: 14px;
            color: white;
            text-align: center;
        }
        .stat-card h2 { margin: 0; font-size: 2rem; }
        .stat-card p { margin: 0; opacity: 0.9; font-size: 0.9rem; }
        div[data-testid="stForm"] {
            background-color: #f9fafb;
            padding: 1.3rem 1.5rem 0.6rem 1.5rem;
            border-radius: 14px;
            border: 1px solid #e5e7eb;
        }
        .result-card {
            background-color: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 1.2rem 1.4rem;
            margin-top: 0.8rem;
        }
        .section-divider { margin: 0.4rem 0 1.2rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="app-title">🎓 School Management System</p>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Register students & teachers, track grades, and look up records.</p>', unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Sidebar navigation + quick stats
# ----------------------------------------------------------------------

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Go to",
        [
            "🏠 Dashboard",
            "🧑‍🎓 Register Student",
            "🧑‍🏫 Register Teacher",
            "📊 Add Grades",
            "🔎 Student Details",
            "🔎 Teacher Details",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption(f"Database file: `{DATABASE}`")

# ----------------------------------------------------------------------
# Dashboard
# ----------------------------------------------------------------------

if page == "🏠 Dashboard":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-card"><h2>{len(data["student"])}</h2><p>Students</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><h2>{len(data["teacher"])}</h2><p>Teachers</p></div>', unsafe_allow_html=True)
    with col3:
        graded = sum(1 for s in data["student"] if s.get("grades"))
        st.markdown(f'<div class="stat-card"><h2>{graded}</h2><p>Students with Grades</p></div>', unsafe_allow_html=True)

    st.write("")
    tab1, tab2 = st.tabs(["Students", "Teachers"])

    with tab1:
        if data["student"]:
            rows = []
            for s in data["student"]:
                grades = s.get("grades", {})
                avg = sum(grades.values()) / len(grades) if grades else 0
                rows.append({
                    "Roll No": s["roll_no"],
                    "Name": s["name"],
                    "Age": s["age"],
                    "Email": s["email"],
                    "Subjects Graded": len(grades),
                    "Average": round(avg, 1),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info("No students registered yet.")

    with tab2:
        if data["teacher"]:
            st.dataframe(pd.DataFrame(data["teacher"]), use_container_width=True, hide_index=True)
        else:
            st.info("No teachers registered yet.")

# ----------------------------------------------------------------------
# Register Student
# ----------------------------------------------------------------------

elif page == "🧑‍🎓 Register Student":
    st.subheader("Register a new student")
    with st.form("register_student_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full name")
            age = st.number_input("Age", min_value=3, max_value=100, step=1)
        with c2:
            roll_no = st.number_input("Roll number", min_value=0, step=1, format="%d")
            email = st.text_input("Email")

        submitted = st.form_submit_button("Register student", use_container_width=True)

        if submitted:
            if not name.strip():
                st.error("Please enter the student's name.")
            elif not validate_email(email):
                st.error("Invalid email address.")
            elif find_student(int(roll_no)):
                st.error(f"A student with roll number {int(roll_no)} already exists.")
            else:
                data["student"].append({
                    "name": name.strip(),
                    "age": int(age),
                    "email": email.strip(),
                    "roll_no": int(roll_no),
                    "grades": {},
                })
                persist()
                st.success(f"Student **{name}** registered successfully! 🎉")

# ----------------------------------------------------------------------
# Register Teacher
# ----------------------------------------------------------------------

elif page == "🧑‍🏫 Register Teacher":
    st.subheader("Register a new teacher")
    with st.form("register_teacher_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full name")
            age = st.number_input("Age", min_value=18, max_value=100, step=1)
            employee_id = st.text_input("Employee ID")
        with c2:
            subject = st.text_input("Subject taught")
            email = st.text_input("Email")

        submitted = st.form_submit_button("Register teacher", use_container_width=True)

        if submitted:
            if not name.strip():
                st.error("Please enter the teacher's name.")
            elif not employee_id.strip():
                st.error("Please enter an employee ID.")
            elif not validate_email(email):
                st.error("Invalid email address.")
            elif find_teacher(employee_id.strip()):
                st.error(f"A teacher with employee ID {employee_id} already exists.")
            else:
                data["teacher"].append({
                    "name": name.strip(),
                    "age": int(age),
                    "email": email.strip(),
                    "employee_id": employee_id.strip(),
                    "subject": subject.strip(),
                })
                persist()
                st.success(f"Teacher **{name}** registered successfully! 🎉")

# ----------------------------------------------------------------------
# Add Grades
# ----------------------------------------------------------------------

elif page == "📊 Add Grades":
    st.subheader("Add / update a grade")

    if not data["student"]:
        st.info("No students registered yet. Register a student first.")
    else:
        options = {f'{s["roll_no"]} — {s["name"]}': s["roll_no"] for s in data["student"]}
        with st.form("add_grades_form"):
            choice = st.selectbox("Student", list(options.keys()))
            c1, c2 = st.columns(2)
            with c1:
                subject = st.text_input("Subject")
            with c2:
                marks = st.number_input("Marks", min_value=0.0, max_value=100.0, step=0.5)

            submitted = st.form_submit_button("Save grade", use_container_width=True)

            if submitted:
                if not subject.strip():
                    st.error("Please enter a subject name.")
                else:
                    roll_no = options[choice]
                    student = find_student(roll_no)
                    student["grades"][subject.strip()] = marks
                    persist()
                    st.success(f"Grade saved: **{subject}** → **{marks}** for {student['name']}.")

    if data["student"]:
        st.markdown("##### Current grades")
        roll_pick = st.selectbox(
            "View grades for",
            [f'{s["roll_no"]} — {s["name"]}' for s in data["student"]],
            key="view_grades_select",
        )
        roll_no_view = int(roll_pick.split(" — ")[0])
        student_view = find_student(roll_no_view)
        grades = student_view.get("grades", {})
        if grades:
            df = pd.DataFrame(list(grades.items()), columns=["Subject", "Marks"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            avg = sum(grades.values()) / len(grades)
            st.metric("Average", f"{avg:.1f}")
        else:
            st.caption("No grades recorded yet for this student.")

# ----------------------------------------------------------------------
# Student Details lookup
# ----------------------------------------------------------------------

elif page == "🔎 Student Details":
    st.subheader("Look up a student")
    roll_no_input = st.number_input("Roll number", min_value=0, step=1, format="%d")
    if st.button("Search", use_container_width=True):
        s = find_student(int(roll_no_input))
        if s:
            grades = s.get("grades", {})
            avg = sum(grades.values()) / len(grades) if grades else 0
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(f"### {s['name']}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Roll No", s["roll_no"])
            c2.metric("Age", s["age"])
            c3.metric("Average", f"{avg:.1f}")
            st.write(f"**Email:** {s['email']}")
            if grades:
                st.write("**Grades:**")
                st.dataframe(pd.DataFrame(list(grades.items()), columns=["Subject", "Marks"]),
                             use_container_width=True, hide_index=True)
            else:
                st.caption("No grades recorded yet.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No student found with that roll number.")

# ----------------------------------------------------------------------
# Teacher Details lookup
# ----------------------------------------------------------------------

elif page == "🔎 Teacher Details":
    st.subheader("Look up a teacher")
    emp_id_input = st.text_input("Employee ID")
    if st.button("Search", use_container_width=True):
        t = find_teacher(emp_id_input.strip())
        if t:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(f"### {t['name']}")
            c1, c2 = st.columns(2)
            c1.metric("Employee ID", t["employee_id"])
            c2.metric("Subject", t["subject"])
            st.write(f"**Age:** {t['age']}")
            st.write(f"**Email:** {t['email']}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No teacher found with that employee ID.")