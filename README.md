# ExamGuard

## Online Examination Monitoring & Integrity Analytics Platform

## Project Overview

ExamGuard is a web-based online examination monitoring and integrity analytics platform designed to assist invigilators during and after online examinations.

The system combines real-time face detection, browser activity monitoring, event logging, rule-based integrity scoring, risk classification, behavioral analytics, incident management, and AI-assisted report generation.

The platform consists of a Flask-based examination and monitoring application and a Streamlit-based analytics dashboard.

ExamGuard is designed as an invigilator-assistance system. The AI component is used only to generate natural-language reports from information already produced by the system. It does not independently calculate integrity scores, determine the official risk classification, or make disciplinary decisions.

---

## Key Features

- Student registration and authentication
- Examination session management
- Webcam-based face presence monitoring
- Multiple-face detection using OpenCV and Haar Cascade
- Browser tab-switch monitoring
- Examination event logging
- Rule-based integrity score calculation
- Low, Medium, and High risk classification
- K-Means behavioral clustering
- PCA-based behavioral visualization
- SQLite-based incident management
- AI-assisted integrity report generation
- LangChain and Google Gemini API integration
- Flask-based invigilator dashboard
- Streamlit-based analytics dashboard
- Student-level behavioral analysis
- CSV and JSON data export
- End-to-end system testing and validation

---

## System Workflow

The overall ExamGuard workflow is:

```text
Student Registration & Login
          ↓
Examination Session
          ↓
Face Detection + Browser Monitoring
          ↓
Event Logging
          ↓
Rule-Based Integrity Scoring
          ↓
Risk Classification
          ↓
K-Means / PCA Behavioral Analysis
          ↓
┌───────────────────────┬────────────────────────┐
│                       │                        │
AI Integrity Report     Flask / Streamlit       │
Generation              Analytics Dashboards     │
│                       │                        │
└───────────────────────┴────────────────────────┘