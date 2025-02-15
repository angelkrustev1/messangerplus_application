# messangerplus_application
A basic social media web application, that allows users to have chats, pusblish posts and interact with them.
The application is designed with user roles and permissions for save and secure experience, as well as a cusotm admin site.

## General Requirements
Python: Version 3.11.1 or higher
PostgreSQL: Database
pip: For installing dependencies
Browser: Browsers such as Opera, Chorome etcetera
Python Virtual Environment: Optional, but recommended

## Setup Instructions
# Step One
Download the sorce code from the github repo
# Install Dependencies
run the following command to install all the required dependecies of the project
pip install -r requirements.txt
# Step 3: Create a .env File
Create a .env file and populate it with the same environment variables as in the .env.templates file and assign the appropriate values
# Step 4: Database Migration
Run the following command to apply migrations:
python manage.py migrate
# Step 6: Run the app
Use this command to run the app:
python manage.py runserver


