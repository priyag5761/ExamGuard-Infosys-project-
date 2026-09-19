import streamlit as st
import pandas as pd
import os
import sqlite3


# -----------------------------------
# Page configuration
# -----------------------------------

st.set_page_config(
    page_title="ExamGuard Analytics",
    page_icon="🛡️",
    layout="wide"
)


# -----------------------------------
# Title
# -----------------------------------

st.title("🛡️ ExamGuard Analytics Dashboard")

st.write(
    "Invigilator dashboard for integrity scores, "
    "risk classification, and exam behavior analytics."
)


# -----------------------------------
# Load student cluster data
# -----------------------------------

if not os.path.exists("student_clusters.csv"):

    st.error("student_clusters.csv not found.")

    st.stop()


data = pd.read_csv("student_clusters.csv")


# -----------------------------------
# Validate required columns
# -----------------------------------

required_columns = [
    "Username",
    "Integrity_Score",
    "Total_Suspicious_Events",
    "Risk_Level"
]

missing_columns = [
    column
    for column in required_columns
    if column not in data.columns
]

if missing_columns:

    st.error(
        f"Missing columns: {', '.join(missing_columns)}"
    )

    st.stop()


# -----------------------------------
# Calculate dashboard metrics
# -----------------------------------

total_students = len(data)

low_risk = (
    data["Risk_Level"] == "Low Risk"
).sum()

medium_risk = (
    data["Risk_Level"] == "Medium Risk"
).sum()

high_risk = (
    data["Risk_Level"] == "High Risk"
).sum()

average_integrity = round(
    data["Integrity_Score"].mean(),
    2
)

total_suspicious_events = int(
    data["Total_Suspicious_Events"].sum()
)


# -----------------------------------
# Dashboard metrics
# -----------------------------------

st.subheader("Risk Overview")

col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.metric(
        "Total Students",
        total_students
    )


with col2:
    st.metric(
        "Low Risk",
        low_risk
    )


with col3:
    st.metric(
        "Medium Risk",
        medium_risk
    )


with col4:
    st.metric(
        "High Risk",
        high_risk
    )


with col5:
    st.metric(
        "Average Integrity",
        average_integrity
    )


# -----------------------------------
# Suspicious events
# -----------------------------------

st.metric(
    "Total Suspicious Events",
    total_suspicious_events
)


# -----------------------------------
# Student Risk Analysis
# -----------------------------------

st.subheader("Student Risk Analysis")

display_columns = [
    "Username",
    "Integrity_Score",
    "Face_Absent",
    "Multiple_Faces",
    "Tab_Switches",
    "Total_Suspicious_Events",
    "Risk_Level"
]

available_columns = [
    column
    for column in display_columns
    if column in data.columns
]

st.dataframe(
    data[available_columns],
    use_container_width=True,
    hide_index=True
)





# -----------------------------------
# Student Details
# -----------------------------------

st.subheader("Student Details")

student_names = sorted(
    data["Username"].dropna().unique()
)

selected_student = st.selectbox(
    "Select a student",
    student_names
)

student_data = data[
    data["Username"] == selected_student
].iloc[0]


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Integrity Score",
        student_data["Integrity_Score"]
    )


with col2:
    st.metric(
        "Face Absent",
        student_data["Face_Absent"]
    )


with col3:
    st.metric(
        "Tab Switches",
        student_data["Tab_Switches"]
    )


with col4:
    st.metric(
        "Suspicious Events",
        student_data["Total_Suspicious_Events"]
    )


st.write(
    "**Risk Level:**",
    student_data["Risk_Level"]
)







# -----------------------------------
# Incidents and Evidence
# -----------------------------------

st.subheader("Incidents & Evidence")

if os.path.exists("examguard.db"):

    conn = sqlite3.connect("examguard.db")

    incidents_df = pd.read_sql_query(
        """
        SELECT
            id,
            username,
            event_type,
            details,
            timestamp,
            severity,
            screenshot_path
        FROM incidents
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    student_incidents = incidents_df[
        incidents_df["username"].str.lower()
        == selected_student.lower()
    ]

    if student_incidents.empty:

        st.info(
            "No incidents recorded for this student."
        )

    else:

        st.dataframe(
            student_incidents[
                [
                    "event_type",
                    "details",
                    "timestamp",
                    "severity"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.write("### Evidence")

        for _, incident in student_incidents.iterrows():

            screenshot_path = incident["screenshot_path"]

            if (
                pd.notna(screenshot_path)
                and os.path.exists(str(screenshot_path))
            ):

                st.image(
                    str(screenshot_path),
                    caption=(
                        f"{incident['event_type']} - "
                        f"{incident['timestamp']}"
                    )
                )

else:

    st.warning(
        "examguard.db not found."
    )









# -----------------------------------
# AI Integrity Report
# -----------------------------------

st.subheader("AI Integrity Report")

ai_report_file = f"AI_Report_{selected_student}.txt"

if os.path.exists(ai_report_file):

    with open(
        ai_report_file,
        "r",
        encoding="utf-8"
    ) as file:

        ai_report = file.read()

    st.text_area(
        "Generated AI Report",
        ai_report,
        height=500
    )

else:

    st.info(
        "AI report has not been generated for this student yet."
    )







# -----------------------------------
# Risk Distribution
# -----------------------------------

st.subheader("Risk Distribution")

risk_counts = (
    data["Risk_Level"]
    .value_counts()
)

st.bar_chart(risk_counts)


# -----------------------------------
# Integrity Score by Student
# -----------------------------------

st.subheader("Integrity Score by Student")

integrity_data = (
    data
    .set_index("Username")["Integrity_Score"]
)

st.bar_chart(integrity_data)


# -----------------------------------
# Suspicious Events by Student
# -----------------------------------

st.subheader("Suspicious Events by Student")

event_data = (
    data
    .set_index("Username")["Total_Suspicious_Events"]
)

st.bar_chart(event_data)



# -----------------------------------
# K-Means / PCA Analysis
# -----------------------------------

st.subheader("K-Means Student Behavior Analysis")

if os.path.exists("static/kmeans_clusters.png"):

    st.image(
        "static/kmeans_clusters.png",
        caption="Student Behavior Clusters using PCA"
    )

else:

    st.warning(
        "K-Means visualization not found. "
        "Run kmeans_analysis.py first."
    )
    
    
    
    
    





# -----------------------------------
# Export Data
# -----------------------------------

st.subheader("Export Data")

if os.path.exists("event_logs.csv"):

    with open("event_logs.csv", "rb") as file:

        st.download_button(
            label="📥 Download Event Logs",
            data=file,
            file_name="ExamGuard_Event_Logs.csv",
            mime="text/csv"
        )

else:

    st.warning("Event logs file not found.")
    
    
    
    


if os.path.exists("student_behavior.csv"):

    with open("student_behavior.csv", "rb") as file:

        st.download_button(
            label="📥 Download Integrity Scores",
            data=file,
            file_name="ExamGuard_Integrity_Scores.csv",
            mime="text/csv"
        )

else:

    st.warning("Integrity scores file not found.")
    
    


if os.path.exists("student_clusters.csv"):

    with open("student_clusters.csv", "rb") as file:

        st.download_button(
            label="📥 Download Cluster Results",
            data=file,
            file_name="ExamGuard_Cluster_Results.csv",
            mime="text/csv"
        )

else:

    st.warning("Cluster results file not found.")
    
    
    
    
# -----------------------------------
# Download Incident Records
# -----------------------------------

if os.path.exists("incident_records.csv"):

    with open("incident_records.csv", "rb") as file:

        st.download_button(
            label="📥 Download Incident Records",
            data=file,
            file_name="ExamGuard_Incident_Records.csv",
            mime="text/csv"
        )

else:

    st.warning("Incident records file not found.")
    
    
    
    
    

# -----------------------------------
# Download Complete Session JSON
# -----------------------------------

if os.path.exists("ExamGuard_Complete_Session_Data.json"):

    with open(
        "ExamGuard_Complete_Session_Data.json",
        "rb"
    ) as file:

        st.download_button(
            label="📥 Download Complete Session JSON",
            data=file,
            file_name="ExamGuard_Complete_Session_Data.json",
            mime="application/json"
        )

else:

    st.warning(
        "Complete session JSON file not found."
    )