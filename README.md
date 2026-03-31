# AI Expense Tracker - BYOP Project

This is my official repository for the "Bring Your Own Project" submission for the Fundamentals of AI and ML course. 

The entire codebase inside this repository is a command-line interface (CLI) application that tracks expenses for you using Artificial Intelligence. Instead of building something generic, I wanted to solve the problem of how annoying it is to manually log daily expenses. With this python script, you just type the amount you spent and what you bought in plain English, and the Generative AI model automatically figures out what category it belongs in.

---

## Table of Contents
1. Core Motivation Behind the Project
2. The Specific Problem I Am Solving
3. Key Technical Features
4. System Architecture and Tools Used
5. Setup and Installation Instructions
6. Walkthrough of the Application (With Screenshots)
7. How the AI Fallback Logic Actually Works
8. Database Schema
9. Security and Data Privacy
10. Edge Cases and Error Handling
11. Future Ideas for Scaling
12. Acknowledgments

---

## Core Motivation Behind the Project

When we got the prompt for the BYOP capstone, I really wanted to avoid making just another tic-tac-toe game or standard web calculator. I try to track my personal budget, but the reality is that typing data into standard financial apps is way too tedious. If I buy a coffee, I have to unlock my phone, open the app, find the big plus button, type the amount, scroll down a list of fifty categories, click "Food and Dining", and hit save. 

I realized this is exactly the type of text-classification problem that Large Language Models and NLP are designed for. I decided to build a lightweight CLI script where the user just types "coffee" and the AI assumes the burden of picking the category. I specifically built it for the terminal because command-line tools don't eat up your laptop's RAM like heavy Electron apps do, and you can just leave it running in the background while you study.

---

## The Specific Problem I Am Solving

If I had to break down the exact issues this software fixes, it comes down to these three things:

First, entry friction is way too high in most apps. It literally takes two seconds to type "Bought 2 coffees for 10 bucks" into a terminal prompt. By cutting down the time it takes to record a transaction, a person is way more likely to actually stick with their budgeting habit over the whole month.

Second, human categorization is wildly inconsistent. One month I might put an Amazon purchase under "Shopping", and three weeks later I might put it under "Electronics". This ruins your financial data when you try to calculate averages. Because the AI model looks at the context, it standardizes the inputs so your data stays perfectly clean over time.

Third, I don't really trust random free budgeting apps with my financial history. Most of them upload your data to remote cloud servers to sell ads. Because my application uses a local SQLite database that lives directly on your computer's hard drive, your actual financial history never leaves your machine. The only thing sent to the cloud is the specific string you type when it queries the AI for a category.

---

## Key Technical Features

Here are the main capabilities I programmed into the system:

- User Authentication System: I wanted it to be somewhat realistic, so you have to register and log in. I used Python's built-in hashlib library to encrypt the passwords with SHA-256 hashing so they aren't saved as plain text.
- Relational Local Storage: By building it entirely around SQLite, multiple users can technically run the script on the same computer using different logins without ever seeing each other's ledgers.
- Gemini AI Integration: The script connects to the Google Gemini 1.5 Flash API. I pass the unstructured text the user types into a custom prompt that forces the LLM to return exactly one word.
- Offline NLP Failsafe: I knew relying totally on Wi-Fi was a bad idea for a grading submission. If the user's internet drops, or if they don't have an API key, the script detects it and silently shifts over to a custom Keyword-Matching algorithm I wrote to guess the category offline.
- Formatted Text Tables: I wrote a printing algorithm that pulls the data dynamically from the SQL database and prints it into mathematically aligned ASCII tables in the terminal.
- Strict Exception Handling: The main application runs in a while loop that utilizes try/except blocks to catch ValueError and KeyboardInterrupt exceptions. If someone types letters into the price float variable, it politely asks them to try again instead of crashing the database connection.

---

## System Architecture and Tools Used

I intentionally made the backend stack very lightweight so anyone can clone this and run it immediately without messing with heavy virtual machines or Docker setups.

Language: Python 3.8 or newer
Database: SQLite3 (Since this comes built into Python, you don't need to install a SQL server)
AI/ML Endpoint: Google Generative AI using the google-generativeai pip package
Environment Variables: python-dotenv to inject API keys into memory safely.

I separated the code into three different modules to keep things clean:
First is main.py, which acts as the controller. It handles the continuous while loop, prints the menus, and manages the inputs.
Second is database.py, which acts as the repository layer handling the SQL queries. It automatically creates the tables the first time you run it.
Third is ai_helper.py, which is the logic layer that bridges the user text to the Gemini API and holds the offline backup dictionary.

---

## Setup and Installation Instructions

If you need to run this project locally to grade it, just follow these terminal commands.

Step 1: Clone the Repository
Pull my code down to your local machine using Git:
git clone https://github.com/Anushka-Chatterjee-128/AI-Expense-Tracker.git
cd AI-Expense-Tracker

Step 2: Initialize a Virtual Environment
It is highly recommended that you sandbox the python dependencies so they don't mess with your global packages.
On Windows:
python -m venv venv
venv\Scripts\activate
On Mac or Linux:
python3 -m venv venv
source venv/bin/activate

Step 3: Install Required Dependencies
Once you are inside the activated virtual environment, install the required packages. 
![Installing Requirements](images/installing-req.png)
pip install -r requirements.txt

Step 4: Configure the Generative AI Node
To see the generative AI portion actually work, you need to provide an API key. 
Go to Google AI Studio in your browser and generate a free developer key. Look at the template file in my folder named .env.example and rename it to just .env. Finally, open the .env file and paste your token inside.
If you skip this step, don't worry. The application watches out for missing keys and will automatically just run the offline keyword matcher instead so it won't break.

Step 5: Boot the Application
Run the main script:
python main.py

---

## Walkthrough of the Application

Once you start the script, this is how the program flows.

Registering and Logging In
Because you are running a fresh database, you need to press 2 to enter the Registration menu. You make a username and a password. Inside database.py, that password gets hashed permanently with SHA-256. Once that finishes, hit 1 to log in.
![Register and Login](images/registering-and-login.png)

Logging an Expense
Once logged in, the menu updates and you can press 1 to add a transaction. The interface prompts you for an amount and a description. In my testing, I typed "uber to the airport" for a 35 dollar amount. The script intercepts that string, routes it to ai_helper.py, and asks the Gemini model for a one-word classification. Usually within half a second, the AI replies with "Transport". The application takes that string and automatically saves the whole row into SQLite.
![Adding Expenses](images/adding-expenses.png)

Reviewing the Ledger
After entering a few more expenses like buying lunch and paying my electric bill, I pressed 2 to view my history. The system connects to the SQL instance, requests all expenses tied exclusively to my user_id, sorts them by the date, and prints them out. You can visually see how perfectly the AI identified the context and tagged each row in the terminal screenshot.
![Viewing Expenses](images/viewing-expense-table.png)

Logging Out
When you are done, press 3 to terminate the active session token, which drops you back to the unauthorized menu. From there another user could log into their own account, or you can press 3 again to trigger a sys.exit(0) call closing the Python process.
![Logout and Exit](images/logout-and-exit.png)

---

## How the AI Fallback Logic Actually Works

The absolute core of the AI logic lives in ai_helper.py. I wrote a dual-system setup so it never completely fails.

The Primary NLP Mechanism 
When you type a description, I don't just send the raw string to Google. I wrap it in a specific engineering prompt:
Categorize the following expense description into a single short category name (e.g., Food & Dining, Transport, Entertainment, Utilities, Shopping, Health, etc.). Just return the category name, nothing else. Description: [User Input]

Because Large Language Models inherently want to be incredibly chatty, if you just send "uber", they will respond with a giant paragraph. By explicitly commanding the prompt to "Just return the category name, nothing else", I basically force the LLM to act strictly as a classification function. This means I get a clean string back that I can safely insert into my SQL database.

The Offline Failsafe Mechanism
What if the api key is wrong or the user is offline?
I developed a fallback mechanism nested inside a standard try/except error block. If the API invocation throws any exception whatsoever, my code ignores it and silently drops down into my local dictionary algorithm.
It turns whatever the user typed into lowercase letters, loops through multiple arrays mapping semantic keywords, and checks for overlaps. If the algorithm spots the substring "netflix", it automatically assigns "Entertainment". If no keywords match, it just safely assigns "Miscellaneous". This ensures 100% uptime during the grading process no matter what happens to the network.

---

## Database Schema

For full academic transparency on how I built the backend, here is the exact relational schema currently executing strictly inside the expense_tracker.db file. I used a 1-to-Many foreign key relationship mapping users to their expenses.

SQL Table: users
id | INTEGER | PRIMARY KEY, AUTOINCREMENT
username | TEXT | UNIQUE, NOT NULL
password_hash | TEXT | NOT NULL

SQL Table: expenses
id | INTEGER | PRIMARY KEY, AUTOINCREMENT
user_id | INTEGER | FOREIGN KEY (users.id), NOT NULL
amount | REAL | NOT NULL
description | TEXT | NOT NULL
category | TEXT | NOT NULL
date | TEXT | NOT NULL

---

## Security and Data Privacy
Even though this is just a CLI terminal project, I adhered to real security frameworks:
Password Protection: By utilizing .encode() and hashlib.sha256(), end-user passwords are protected against database breaches.
SQL Injection Armor: By using question mark placeholder parameters inside the cursor.execute() statements, I made sure nobody can type SQL payloads like ' OR '1'='1 into the username field to dump the tables.
Ignored Variables: My .gitignore file physically guarantees that the .env file containing the secret Google API key and the actual local SQLite database binary are completely rejected by Git, meaning no traces of sensitive data are ever pushed to the internet.

---

## Edge Cases and Error Handling
A great terminal application shouldn't crash just because you fat-fingered a typo. 
Handling Invalid Floats: If someone is asked for a price amount and types in words instead of numbers, the terminal uses try/except ValueError loops to reject the input, display a polite human-readable warning, and continuously loop until they provide a valid float.
Handling Control Sequences: Pressing CTRL+C in a terminal usually throws an ugly KeyboardInterrupt traceback error. My application universally catches this around the main function, allowing it to print "Exiting..." and properly close the SQL connection before terminating.

---

## Future Ideas for Scaling
While this MVP completes all the requirements for the capstone, scaling the application out would probably involve building the following systems next:
Interactive Graphics: Integrating a library like plotext would allow me to natively render colorful bar graphs directly in the bash terminal, grouping user spending by AI categories without needing a web interface.
Exporting to Excel: I could add a -export command line switch that queries all rows matching the user_id and dumps them into a CSV file so they could easily map their spending habits in Excel.
Budget Constraints: Letting the user hardcode strict budget ceilings (like limiting themselves to 200 dollars on entertainment a month). The SQL engine would just SUM their total rows and the CLI would print a red warning if they exceed it.

---

## Acknowledgments
Built completely from scratch in Python 3.8.
Project conceived and engineered for the Fundamentals of AI and ML evaluated BYOP capstone submission.
