# AI Expense Tracker (BYOP Capstone Project)

Welcome to the repository for my "Bring Your Own Project" (BYOP) submission for our Fundamentals of AI and ML course. 

This repository holds all the source code, explanations, and programming logic I wrote for my terminal-based AI Expense Tracker. Basically, the whole point of this project is to try and fix the annoying parts of normal budgeting apps by adding some Generative Artificial Intelligence into the mix. I wanted to create a tool where you can just type what you bought in plain English instead of clicking a bunch of menus.

---

## Comprehensive Table of Contents
1. [Executive Summary & Motivation](#executive-summary--motivation)
2. [The Core Problem Statement](#the-core-problem-statement)
3. [Key Features & Capabilities](#key-features--capabilities)
4. [System Architecture & Tech Stack Details](#system-architecture--tech-stack-details)
5. [Complete Setup & Installation Guide](#complete-setup--installation-guide)
6. [Step-by-Step Walkthrough (with UI Screenshots)](#step-by-step-walkthrough)
7. [Deep Dive: How the AI Engine Works](#deep-dive-how-the-ai-engine-works)
8. [Database Schema & ERD Mapping](#database-schema--erd-mapping)
9. [Security Considerations & Best Practices](#security-considerations--best-practices)
10. [Error Handling & Edge Cases](#error-handling--edge-cases)
11. [Future Scope & Production Enhancements](#future-scope--production-enhancements)
12. [Acknowledgments](#acknowledgments)

---

## Executive Summary & Motivation
When the professor gave us the BYOP project instructions, I spent a lot of time thinking about what to make. I really wanted to build an application that I could actually use in my everyday life, rather than just submitting another standard calculator app or a generic game. I realized that tracking expenses is something we all know we should do, but we usually stop doing it because typing all the data in is super tedious. 

If you look at most finance apps on our phones right now, they force you to manually tap through a ton of dropdown menus simply to say that a $5 charge at a coffee shop belongs in the "Food & Dining" category, or that a cheap train ticket is "Transport". I thought about this and realized that classifying text is actually a perfect textbook use case for Artificial Intelligence—specifically Natural Language Processing (NLP). 

So, I decided to code a very fast Command Line Interface (CLI) application using Python. With this tracker, you simply type out whatever you bought just like you are texting a friend, and the AI takes over and figures out the category for you. I chose to build it completely for the terminal because CLI programs load instantly, they use almost zero RAM on your laptop, and you don't even have to take your hands off the keyboard to get things done.

---

## The Core Problem Statement
The exact problem my software is trying to solve comes down to three main points:

1. **Too Much Friction in Data Entry:** It takes maybe two seconds to type "Bought 2 coffees for 10 bucks". On the other hand, opening a mobile app, waiting for the logo screen, clicking the floating plus button, manually typing the number, and then scrolling through a list of 50 different categories takes way longer. Because it takes so long, people just give up on tracking their money halfway through the month.
2. **Inconsistent Categorization:** When a person tracks their own spending manually, they change their mind a lot. Fast forward a few months, and you might have put Amazon purchases under "Shopping" one week, and then under "Groceries" the next week. An AI model solves this by looking at the context and standardizing everything so your data stays perfectly clean.
3. **Data Privacy Concerns:** A lot of the popular budgeting trackers actually take your highly sensitive financial history and upload it to random cloud servers. By designing my app to only use a local SQLite database right on your hard drive, none of your actual money history leaves your computer. The only thing the app ever sends to the internet is the specific item name when it asks the AI for the category.

---

## Key Features & Capabilities

- **Secure Session Authentication:** I wanted to make sure the app was safe to use, so users have to register an account and log in. The passwords aren't just saved as plain text either; they are actively encrypted using SHA-256 hashing through Python's built-in `hashlib` library.
- **Relational Data Storage:** Everything is built on SQLite. This means multiple people can actually use the same terminal application on the same computer without accidentally seeing each other's financial logs.
- **Generative AI Integration:** The program hooks directly into the Google Gemini 1.5 Flash API. It takes whatever unstructured text the user types and forces the LLM to return exactly one structured category word.
- **Offline NLP Failsafe System:** I knew that relying only on an internet connection was a bad idea. If you go offline, or if you simply haven't set up your API keys yet, the application won't crash. Instead, it seamlessly switches over to a custom Keyword-Matching algorithm I wrote that scans your string to guess the category offline (like realizing the word "uber" should trigger the "Transport" tag).
- **Formatted ASCII Tabular Views:** When you view your expenses, the data is pulled directly from the SQL database and then formatted into cleanly aligned text tables so it looks nice in the terminal.
- **Protection Against Edge Cases:** I put a lot of work into the main loop using strict `try/except` blocks. If someone accidentally types letters into the price amount, or tries to forcibly close the terminal with `CTRL+C`, the app catches the error safely instead of corrupting the database.

---

## System Architecture & Tech Stack Details
I tried my best to keep the technology stack lightweight so that anyone can download this and run it immediately without having to install complicated Docker containers.

### The Stack:
- **Programming Language:** Python 3.8+ 
- **Database Architecture:** SQLite3 (This is a serverless SQL engine that comes built directly into Python, so no separate installs are needed)
- **AI/ML API Endpoint:** Google Generative AI (using the `google-generativeai` package)
- **Environment Management:** `python-dotenv` which I used so I could test my API keys without accidentally uploading my secret tokens to GitHub.

### Modular Codebase Organization:
To make sure my code was clean and followed good Software Engineering principles, I split the project into three separate Python files:
1. `main.py` - This is the controller. It handles the main continuous loop, prints the visual menus to the screen, takes in what the user types, and manages the whole application lifecycle.
2. `database.py` - This is the database layer. It handles all the direct SQL queries. It automatically builds the tables the very first time you run it, and it uses parameterized inputs to make sure nobody can do SQL Injection attacks.
3. `ai_helper.py` - This is the brains of the operation. It acts as the bridge between the raw user text and the Gemini AI model. It also holds the backup offline dictionary string-matching logic.

---

## Complete Setup & Installation Guide

If you are grading this BYOP project or just want to try it out on your own machine, follow these exact instructions in your terminal.

### Step 1: Clone the Repository
First, pull the code down to your computer using Git:
```bash
git clone https://github.com/Anushka-Chatterjee-128/AI-Expense-Tracker.git
cd AI-Expense-Tracker
```

### Step 2: Initialize a Virtual Environment (Highly Recommended)
It's always a good idea to put Python dependencies in a sandbox. Create a virtual environment (`venv`) to keep the google AI packages separate from your main system.

**For Windows Users:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**For macOS / Linux OS Users:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
Once you are inside your virtual sandbox, install the required packages. 
![Installing Requirements](images/installing-req.png)
```bash
pip install -r requirements.txt
```

### Step 4: Configure the Generative AI Node (Optional API Setup)
To actually see the LLM portion work, you will need to give it an API key. 
1. Go to your internet browser and visit [Google AI Studio](https://aistudio.google.com/) to get a free developer key.
2. Go back to your folder and find the file called `.env.example`. Rename it so it is just called `.env`.
3. Open the `.env` file in Notepad or VS Code, and paste your actual token inside.
```text
GEMINI_API_KEY=AIzaSyYourSecretKeyHere...
```
*(By the way, if you skip this step because you don't want to make an account, the application will automatically notice the missing key and fallback to the offline keyword matcher instead of crashing!)*

### Step 5: Boot the Application
Now that everything is ready, just run the main script:
```bash
python main.py
```

---

## Step-by-Step Walkthrough

Once you start the script, here is what using the app is actually like.

### 1. Registering and Validating User Sessions
The very first thing it does is ask you to log in. Since you probably just installed it and have a fresh database, type `2` to enter the Registration menu. It will ask you to make a username and a password. Behind the scenes, `database.py` takes your password, hashes it permanently with SHA-256, and saves it. Once that is done, you can hit `1` to log in normally.
![Register and Login](images/registering-and-login.png)

### 2. Dynamically Logging an Expense using the AI Engine
Once you are logged into your new account, the main menu changes. Press `1` to add an expense.
It's going to quickly ask for two things:
1. **Amount ($)** 
2. **Expense Description** 

When I was testing it, I typed the phrase: `"uber to the airport"` for `$35.0`. 
The application takes that string and sends it straight to `ai_helper.py`. The helper talks to the Gemini model and asks it to classify the sentence using only one word. Usually in less than half a second, the AI replies with exactly: **Transport**. The app then takes that and saves the whole row (User ID, Amount, Description, Category, Date) into the SQLite database file.
![Adding Expenses](images/adding-expenses.png)

### 3. Reviewing the Financial Ledger
After I spent a few minutes logging other expenses (like buying a burger, paying my electricity bill, and grabbing a Netflix subscription), I pushed `2` to view my history. 

What happens here is `main.py` asks the SQL database for every single expense that matches my specific `user_id`, orders them so the newest ones are at the top, and prints them out as a really nice text table. If you look at the screenshot, you can see the AI did a perfect job figuring out what category everything belonged to!
![Viewing Expenses](images/viewing-expense-table.png)

### 4. Session Termination (Logout & Exit)
When you are completely finished logging your expenses for the day, you can securely press `3` to log out, which drops you back to the main startup menu. From there, your roommate or friend could theoretically log into their own account, or you can just press `3` again to close the Python program entirely.
![Logout and Exit](images/logout-and-exit.png)

---

## Deep Dive: How the AI Engine Works Under the Hood

The really cool part of this application lives inside the `ai_helper.py` file. Here is an explanation of my dual-system setup.

### The Primary NLP Mechanism (Generative AI API)
When a user types in a description of what they bought, I don't just send their raw text to the Google servers. I wrapped their text in a very specific, carefully engineered prompt before handing it to the `gemini-1.5-flash` model:

> *"Categorize the following expense description into a single short category name (e.g., Food & Dining, Transport, Entertainment, Utilities, Shopping, Health, etc.). Just return the category name, nothing else. Description: [User Input]"*

The issue with Large Language Models is that they inherently want to talk to you like a chatbot. If you just send the word "uber", they will respond with a giant paragraph about how "Uber is a multinational transportation network company...". By explicitly coding the prompt to say "Just return the category name, nothing else", I basically force the AI to act strictly as a classification function. This means I get a clean string back that I can safely insert into my SQL database.

### The Offline Failsafe Mechanism (Local Hardcoded NLP)
One thing we talk about in backend programming is redundancy. I had to ask myself: What if the user gets on an airplane without Wi-Fi? What if their Google API key stops working? 

To handle this, I wrote a fallback mechanism inside a `try / except` block. If the API call fails for any reason at all, the code ignores the error and immediately drops down to use my local dictionary algorithm instead.

```python
FALLBACK_CATEGORIES = {
    "Transport": ["uber", "lyft", "taxi", "bus", "train", "flight", "gas"],
    "Entertainment": ["movie", "cinema", "game", "netflix", "spotify"]
}
```
This backup algorithm turns whatever the user typed into lowercase letters, loops through these different keyword lists, and checks to see if any words match using Python's `any()` function. If the algorithm sees the substring "netflix", it automatically assigns "Entertainment". If it doesn't recognize anything, it just safely assigns "Miscellaneous". This completely guarantees that the app will never crash during grading or while you're offline!

---

## Database Schema & ERD Mapping

In the interest of fully explaining my backend, here is the exact database schema running inside the `expense_tracker.db` file. I used a standard 1-to-Many foreign key relationship mapping the users to their expenses.

**SQL Table: `users`**
| Column Target | SQL Data Type | Absolute Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| username | TEXT | UNIQUE, NOT NULL |
| password_hash | TEXT | NOT NULL |

**SQL Table: `expenses`**
| Column Target | SQL Data Type | Absolute Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| user_id | INTEGER | FOREIGN KEY (users.id), NOT NULL |
| amount | REAL | NOT NULL |
| description | TEXT | NOT NULL |
| category | TEXT | NOT NULL |
| date | TEXT | NOT NULL |

---

## Security Considerations & Best Practices
Even though this is just a CLI academic project, I wanted to treat it like real software, so I added some actual security features:
1. **Password Protection:** Like I mentioned earlier, using `.encode()` and `hashlib.sha256()` protects user passwords so they can't be easily stolen if someone copies the database file.
2. **SQL Injection Armor:** I made sure to use `?` placeholder parameters inside all my `cursor.execute()` statements. This means a malicious user can't just type SQL payloads like `' OR '1'='1` into the username prompt to try and dump the entire database.
3. **Ignored Runtime Variables:** I added a strict `.gitignore` file to the project. This guarantees that the `.env` file holding the secret API key and the physical `expense_tracker.db` file are blocked by Git. That way, nothing sensitive is ever accidently uploaded to my public GitHub repository.

---

## Error Handling & Edge Cases
I firmly believe that command line apps shouldn't crash just because a human made a minor typo. 
- **Handling Invalid Floats**: If my app asks for a price amount and the user accidentally types `--` or text instead of a number, the code catches it with a `try/except ValueError`. Instead of violently crashing the entire app with a Traceback error, it just shows a polite warning saying "Please enter a valid positive number" and lets them try again.
- **Handling Control Sequences**: Pressing `CTRL+C` while working in a terminal will normally throw a `KeyboardInterrupt` which looks really messy. My app catches this exception globally in the `main()` function, so it can quickly print `Exiting...` and safely shut down the process without an ugly error log.

---

## Future Scope & Production Enhancements
While this initial product totally fulfills all the requirements for the BYOP project, scaling the application out to be something I could release in the real world would probably require building the following things:
1. **Interactive Ascii Graphics:** While the terminal outputs text grids perfectly right now, integrating a library like `plotext` would let me draw actual colorful bar charts in the terminal. That way the user could visually see how much they spent on Food versus Shopping over a 30-day period.
2. **Export capabilities (CSV/JSON/PDF):** Adding an extra menu button that triggers a SQL query to gather all of the user's rows and export them as a clean CSV file so they could look at their data in Microsoft Excel.
3. **Hard Budget Constraints:** I would like to let users set hardcoded budget caps (like telling the app "I only want to spend $200 on Entertainment every month"). The database engine would then add up those specific expenses and visually warn the user directly in the CLI if they are getting too close to their limit!

---

## Acknowledgments
- Concepted, coded, and built for the *Fundamentals of AI and ML* course as my final evaluated BYOP capstone project.
- Powered by Python 3.8 and the speedy Google Generative AI APIs.
