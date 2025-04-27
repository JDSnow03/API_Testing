# my-vue-app/README.md

# Print-A-Test App

## Project Overview

This project is a Vue.js application that serves as a Test Creation Manager. It allows users to log in as different roles, including Teacher, Publisher, and Webmaster.
This application allows the Teacher users to import QTI files for new testbanks with imported questions, or create new testbanks from scratch. These testbanks are used
for the creation of paper test documents. Teachers will also have access to public materials from other teachers as well as textbook publishers. Publisher users are able
to create testbanks from scratch per their textbook and publish these resources accordingly after finalizing. Webmaster users can download parts or all of the database
information into .csv files for administrative use. This project was made by Team 8B and is called Print-A-Test.

## Project Folder Structure

### Frontend

my-vue-app
├── src
│   ├── assets
│   │   |── publisher_styles.css # Styling formats for the publisher pages
│   │   |── teacher_styles.css   # Styling formats for the teacher pages
│   │   |── webmaster_styles.css # Styling formats for the webmaster pages
│   ├── components
│   │   |── PubHome.vue          # Vue component for the Publisher Home page
│   │   |── PubLog.vue           # Vue component for the Publisher Login page
│   │   |── PubNewBook.vue       # Vue component for the Publisher Book Creation page
│   │   |── PubQuestions.vue     # Vue component for the Publisher Question page
│   │   |── PubViewTB.vue        # Vue component for the Publisher Testbank view page
│   │   |── TeacherHome.vue      # Vue component for the Teacher Home page
│   │   |── TeacherLog.vue       # Vue component for the Teacher Login page
│   │   |── TeacherNewClass.vue  # Vue component for the Teacher Class Creation page
│   │   |── TeacherNewTB.vue     # Vue component for the Teacher Testbank Creation page
│   │   |── TeacherPubQ.vue      # Vue component for the Teacher view Published Testbanks/Tests page
│   │   |── TeacherQuestions.vue # Vue component for the Teacher Question page
│   │   |── TeacherTemplate.vue  # Vue component for the Teacher viewing the Test page
│   │   |── TeacherViewTB.vue    # Vue component for the Teacher Testbank View page
│   │   |── WebmasterHome.vue    # Vue component for the Webmaster Home page
│   │   |── WebmasterLog.vue     # Vue component for the Webmaster Login page
│   │   └── Welcome.vue          # Vue component for the welcome page
│   ├── router
│   │   |── index.js             # Routing table for the Vue application
│   ├── App.vue                  # Root component of the Vue application
│   └── main.js                  # Entry point of the Vue application
├── package.json                 # Configuration file for npm dependencies
├── README.md                    # Documentation for the project
└── vue.config.js                # Configuration file for Vue CLI
---

## Setup Instructions
All dependencies are located in the package-lock.json file. Please ensure you have 
Node Packet Manager and Node.js installed to the latest version to run the dependency
bash install.
Current versions:
NPM: 11.2.0
Node: v22.13.0
Vue: 1.0.0

1. **Navigate to Vue project folder:**
   cd my-vue-app
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the application:**
   ```bash
   npm run serve
   ```

4. **Open your browser:**
   Navigate to `http://localhost:8080` to view the application.


## Project Credits
CS 499 - 01 Professor James Williamson

Team 8B: Test Creation Manager P18

Members:
Paige Smith - Team Leader
Lauren Williams - Technical Writer
Rodridguez Stuckey - Technical Lead
Derrick Snow - Test Lead

Students of UAH, Spring 2025