# TechCrunch Scrapper


## Table of Contents
- [Project Description](#Project-Description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Project Description
The TechCrunch Scraper is a Django and Celery-based project designed to scrape a website, update a Django database daily, and provide 
functionality to scrape the search page of the website.


### Features

1. **Daily Web Scraping:**
   - Utilizes Celery to schedule daily tasks for web scraping.
   - Extracts relevant information from the target website and updates the Django database.

2. **Search Page Scraping:**
   - Implements functionality to scrape specific search pages of the website.
   - Allows users to input search queries and retrieves relevant information.

3. **Django Database Integration:**
   - Utilizes Django models to define the structure of the database.
   - Stores scraped data in the Django database for easy retrieval and analysis.

4. **Export Functionality:**
   - Provides options to export scraped data in various formats (CSV, XLS, JSON).
   - Offers a convenient way to access and share scraped information.

### Technology Stack

- **Backend Framework:** Django
- **Task Queue:** Celery
- **Database:** Django ORM
- **Web Scraping:** Beautiful Soup, Requests
- **Export Formats:** CSV, XLS, JSON
- 
### Project Structure


- **TechCrunchScrapper/**
  - `manage.py`: Django management script.
  - **blog/**
    - `models.py`: Defines Django models for the database.
    - `tasks.py`: Contains Celery tasks for web scraping.
    - `views.py`: Implements views for handling web requests.
    - `urls.py`: Configures URL patterns.
    - `templates/`: HTML templates.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/TechCrunchScraper.git
   cd TechCrunchScraper

## OR

1. **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt

2. **Apply migrations and start the development server:**

    ```bash
    python manage.py migrate
    python manage.py runserver

3. **Start Celery worker for background tasks:**
    ```bash
    celery -A TechCrunchScrapper worker --loglevel=info -P eventlet

4. **Start Django server**
    ```bash
   python manage.py runserver
   
### Usage
Access the web application at http://127.0.0.1:8000/.
Navigate to the search page and input search queries to retrieve relevant information.
Background tasks for daily scraping are handled by Celery and scheduled to run periodically.

### Contribution Guidelines
1. **Fork the repository.**
2. **Create a new branch for your feature or bug fix.**
3. **Make changes and submit a pull request.**