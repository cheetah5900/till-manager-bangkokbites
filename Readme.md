# Till cashier manager

## Background
I created this web application to help me clear customers' bills everyday I worked faster than the manual way 50%.

Furthermore, it can input various data to show a report as a mockup to copy to paper template again later. Additionally, there are a scraping feature from online shop to the system automatically and an Excel reading feature to read and fill the system automatically.

## Technology
- Python
- Django Framework
- SQLite3 for Database
- Selenium for web scraping
- Excel

## Requirement.
- Python 3.0

## How to Deploy on local

### Step 1 : set up Python
1. Download & Install python (https://www.python.org/downloads)
2. Check Python's version by `python -v`

### Step 2 : Set up package in project
1. Open terminal at project folder
2. run command `pip install -r requirements.txt` to install required packages.

### Step 3 : Set up Google Chrome for web scraping
3. Download and Check `Google Chrome` version
4. Download `chromedriver` depend on Google Chrome version for controlling Google Chrome. 
- ex. Google Chrome version 104, You need to download chromedriver version 104.
5. Place downloaded chromedriver to project folder.

### Step 4 : Run project
1. Open terminal at project folder
2. run command `python manage.py runserver` to run project


### Step 5 : Login to web app
1. Open new tab browser
2. Go to `localhost:8000`
3. There is no need to login.
   
## How to use
1. Choose date and branch.
2. Input data to every menu exept a Report menu.
3. Click Report menu to see if credit card is correct.
4. In the next page is a mockup paper to copy to template paper again.

