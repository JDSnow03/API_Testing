# Print-A-Test

> Instantly convert Canvas quizzes into clean, printable exams — no formatting headaches, just full control for educators.

---

## Overview

**Print-A-Test** is a full-stack web application built for teachers and education professionals to streamline the creation of printable tests. It supports manual question creation and Canvas QTI file imports, complete with answer key generation, attachment handling, and custom templates. The platform is role-based and includes permission control for **Teachers**, **Publishers**, and **Webmasters**.

---

## Tech Stack

- **Backend:** Python, Flask, PostgreSQL, Supabase (Storage & Auth)
- **Frontend:** Vue.js
- **Authentication:** JWT (with Supabase)
- **Database:** PostgreSQL/Supabase
- **File Uploads:** Supabase Buckets
- **Deployment:** `.env` support and modular Flask blueprint structure

---

## Project Folder Structure

### Backend

API-Testing/
├── run.py                        # Entry point to start the Flask application
├── app/
│   ├── __pycache__/               # Python cache files (can be ignored)
│   ├── __init__.py                # Initializes the Flask app and registers blueprints
│   ├── attachments.py             # Handles file attachments for questions
│   ├── auth.py                    # Authentication and authorization logic (token validation)
│   ├── config.py                  # Database configuration and connection setup
│   ├── courses.py                 # API endpoints for managing courses
│   ├── downloads.py               # API endpoints for downloading CSV data (users, etc.)
│   ├── feedback.py                # API endpoints for teacher feedback on questions
│   ├── qti_import.py              # API endpoints for importing QTI files into the system
│   ├── questions.py               # API endpoints for creating and managing questions
│   ├── resource_page.py           # API endpoints for managing resource pages
│   ├── testbanks.py               # API endpoints for creating and managing test banks
│   ├── tests.py                   # API endpoints for managing tests
│   └── textbook.py                # API endpoints for managing textbooks
├── utilities/
│   ├── __pycache__/               # Python cache files (can be ignored)
│   ├── file_handler.py            # Helper functions for handling file uploads and downloads
│   └── qti_parser.py              # Helper functions for parsing QTI files




### Frontend






---

## Authentication & Roles

Supabase Auth manages user registration and JWT-based login. Three roles are supported:

- **Teacher**: Create private/public questions, build tests from templates, view/leave feedback, and access published material.
- **Publisher**: Create private/public questions, contribute to the public question pool, and view/leave feedback.
- **Webmaster**: Full access to system-level operations, including downloading test archives and viewing analytics.

---

## Core Features

- **QTI File Importing**: Seamlessly parse Canvas exports and convert them into usable questions.
- **Manual Question Creation**: Supports Multiple Choice, Matching, Fill-in-the-Blank, Essay, and True/False.
- **Test Template System**: Teachers can generate printable tests using styled templates with custom point values.
- **Attachment Handling**: Upload and link images or files to questions via Supabase Buckets.
- **Role-Based Access Control**: Tailored views and permissions for teachers, publishers, and webmasters.
- **Feedback System**: Leave comments on questions/tests with duplicate feedback prevention.
- **Download Tools (Webmaster)**: Export CSV data and manage system-wide test/report downloads.

---

## Installation Guide

### Backend Setup

---Installation---
Follow these steps to set up the Flask API of the project.

1. Install Python 3
	This project requires Python 3.
	If you don't have it installed, download it from python.org.

	To check if Python 3 is already installed, run:

	python --version

	or

	python3 --version

	You should see a version like Python 3.x.x.
	If not, install Python 3 before proceeding.

2. Navigate to the project directory:

	cd your-project-folder


3. Install the required Python dependencies
	Install all project dependencies listed in requirements.txt by running:

	pip install -r requirements.txt

4. Run the project:

	flask run

	or

	python run.py
