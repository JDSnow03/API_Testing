# Print-A-Test

---

## Project Overview

This is the Flask-based backend API for Print-A-Test. It supports Teachers, Publishers, and Webmasters 
by providing secure API endpoints for user authentication, course and test management, QTI file imports, 
attachment handling, feedback tracking, and system-level operations.

## Authentication & Roles

Supabase Auth manages user registration and JWT-based login. Three roles are supported:

- **Teacher**: Create private/public questions, build tests from templates, view/leave feedback, and access published material.
- **Publisher**: Create private/public questions, contribute to the public question pool, and view/leave feedback.
- **Webmaster**: Full access to user, question, textbook, and course database tables for downloading and review.

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

## Project Credits
CS 499 - 01 Professor James Williamson

Team 8B: Test Creation Manager P18

Members:
Paige Smith - Team Leader
Lauren Williams - Technical Writer
Rodridguez Stuckey - Technical Lead
Derrick Snow - Test Lead

Students of UAH, Spring 2025