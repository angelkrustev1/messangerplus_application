# MessangerPlus Application

A basic social media web application that allows users to have chats, publish posts, and interact with them. The application is designed with user roles and permissions for a safe and secure experience, as well as a custom admin site.

## Deployment
The application and database are hosted on [Render](https://render.com) and accessible at the following URL:
[MessangerPlus Application](https://messangerplus-application.onrender.com) (#No Longer Available)

## General Requirements

- **Python**: Version 3.11.1 or higher
- **PostgreSQL**: Database
- **pip**: For installing dependencies
- **Browser**: Browsers such as Opera, Chrome, etc.
- **Python Virtual Environment**: Optional, but recommended

## Setup Instructions

### Step 1: Download the Source Code
Download the source code from the GitHub repository.

### Step 2: Install Dependencies
Run the following command to install all the required dependencies of the project:

```sh
pip install -r requirements.txt
```

### Step 3: Create a `.env` File
Create a `.env` file and populate it with the same environment variables as in the `.env.templates` file, assigning the appropriate values.

### Step 4: Apply Database Migrations
Run the following command to apply migrations:

```sh
python manage.py migrate
```

### Step 5: Run the Application
Use this command to run the app:

```sh
python manage.py runserver
