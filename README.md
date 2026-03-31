# AI Expense Tracker (BYOP Capstone Project)

Welcome to the official repository for my **Bring Your Own Project (BYOP)** submission for the *Fundamentals of AI and ML* course. 

This repository contains the complete source code, architectural documentation, and implementation logic for my terminal-based **AI Expense Tracker**. This project bridges the gap between traditional financial ledger applications and modern Generative Artificial Intelligence by creating a frictionless, Natural Language-driven interface for logging daily transactions.

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
When we were assigned the BYOP project, I wanted to build an application that I could genuinely use in my daily life, rather than another generic calculator or tic-tac-toe game. Tracking expenses is notoriously difficult because human behavior often resists constant, friction-heavy data entry. 

Most conventional finance applications (even the expensive ones) require you to manually click through endless dropdown menus just to specify that a $5 charge at Starbucks belongs in the "Food & Dining" category, or that a subway ticket is "Transport". I realized this text-classification problem is a perfect, textbook use case for **Artificial Intelligence**, specifically **Natural Language Processing (NLP)**. 

I decided to build a fast, lightweight Command Line Interface (CLI) application in Python. In this tool, you simply type exactly what you bought in plain English, and the AI assumes the burden of categorizing it. It is built entirely for the terminal because CLI apps are remarkably fast, consume virtually zero system memory (RAM), and allow power-users to accomplish tasks without lifting their hands from the keyboard.

---

## The Core Problem Statement
The exact problem this software solves can be defined by three critical pillars:

1. **Friction in Data Entry:** Typing "Bought 2 coffees for 10 bucks" takes exactly 2 seconds. Conversely, opening a GUI application, waiting for it to load, clicking a '+' button, typing the amount, and scrolling through a static list of 50 categories takes 30+ seconds. This latency leads to users abandoning expense tracking altogether.
2. **Inconsistent Categorization Variables:** A human tracking their own expenses is often inconsistent. One month you might categorize Amazon as "Shopping", and the next month you might categorize it as "Groceries". An AI standardizes these inputs based on absolute context, maintaining perfectly structured data over time.
3. **Data Privacy Intrusions:** Many modern budget trackers upload your highly sensitive financial data, location data, and transaction histories to third-party cloud servers. By designing this app to securely use a local SQLite instance, none of your financial history is stored outside your hard drive. The only piece of data transmitted to the cloud is the raw string of the purchased item for semantic NLP classification.

---

## Key Features & Capabilities

- **Secure Session Authentication:** The application enforces a strict user ecosystem. Users must register an account and log in. Passwords are actively encrypted using SHA-256 hashing via Python's native `hashlib` cryptography library.
- **Relational Data Storage:** Built entirely on SQLite, ensuring that multiple users can utilize the same terminal application on the same machine without cross-contaminating their financial ledgers.
- **Generative AI Integration:** Hooked directly into the Google Gemini 1.5 Flash API. It takes unstructured user prompts and forces the LLM to return a strictly structured classification noun.
- **Offline NLP Failsafe System:** If you venture offline, hit an API rate limit, or haven't configured your `.env` keys, the application gracefully degrades. It shifts seamlessly to a custom, local Keyword-Matching algorithm that scans substrings to categorize text offline (e.g., detecting "uber" triggers the "Transport" classification).
- **Formatted ASCII Tabular Views:** The data is pulled dynamically from the SQL database and algorithmically formatted into mathematically aligned, responsive ASCII tables for terminal readability.
- **Protection Against Edge Cases:** The main loop utilizes strict Exception block catching (`try/except ValueError`, `EOFError`, and `KeyboardInterrupt`) so that invalid float amounts, random characters, or immediate terminal shutdowns do not corrupt the database schema.

---

## System Architecture & Tech Stack Details
I intentionally kept the stack highly modular and rigorously lightweight. There is absolutely no need to run Docker containers or heavy Node.js runtimes just to track an expense.

### The Stack:
- **Programming Language:** Python 3.8+ (Strictly typed variables where applicable)
- **Database Architecture:** SQLite3 (A serverless SQL engine built directly into Python binaries)
- **AI/ML API Endpoint:** Google Generative AI (`google-generativeai` SDK)
- **Environment Management:** `python-dotenv` for safely injecting secret variables into runtime memory without exposing them to code repositories.

### Modular Codebase Organization:
To ensure the code is maintainable and adheres to the Software Engineering principle of Separation of Concerns (SoC), the codebase is split into three primary modules:
1. `main.py` - The controller. Handles the core `while True` loop, the visual CLI menus, terminal formatting, user input sanitization, and graceful exit handling.
2. `database.py` - The repository layer. Handles all direct SQL queries. It automatically seeds the tables on the first run, executes `INSERT INTO` commands, and performs `SELECT` queries utilizing parameterized inputs (to completely prevent SQL Injection attacks).
3. `ai_helper.py` - The intelligence layer. Acts as the bridge between the raw user text and the Gemini AI model endpoints. It houses both the LLM prompt-engineering logic and the offline local dictionary failsafe.

---

## Complete Setup & Installation Guide

If you are grading this BYOP project or simply want to clone it to use for your own personal finance tracking, follow these terminal instructions exactly.

### Step 1: Clone the Repository to Local Storage
First, pull the codebase to your local environment using Git:
```bash
git clone https://github.com/Anushka-Chatterjee-128/AI-Expense-Tracker.git
cd AI-Expense-Tracker
```

### Step 2: Initialize a Virtual Environment (Highly Recommended)
Python dependencies should be sandboxed. Create a virtual environment (`venv`) to isolate the `google-generativeai` packages from your global OS packages.

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
Once inside your activated sandbox, install the necessary project requirements. 
![Installing Requirements](images/installing-req.png)
```bash
pip install -r requirements.txt
```

### Step 4: Configure the Generative AI Node (Optional API Setup)
To witness the true LLM in action, you must provide it an API key. 
1. Navigate to your browser and visit [Google AI Studio](https://aistudio.google.com/) to generate a free developer API key.
2. Back in your terminal, locate the template file named `.env.example`. Rename this file to strictly `.env`.
3. Open the `.env` file in VS Code, Vim, or Notepad, and replace the placeholder with your actual token.
```text
GEMINI_API_KEY=AIzaSyYourSecretKeyHere...
```
*(Crucially: If you skip this step or are actively offline, the application will automatically detect the missing environment variable and transition to the offline Keyword Matcher. It will not crash.)*

### Step 5: Boot the Application
With the database and environment primed, execute the primary script:
```bash
python main.py
```

---

## Step-by-Step Walkthrough

Once you initialize the controller script, here is what the user journey looks like.

### 1. Registering and Validating User Sessions
The opening prompt demands authentication. Because this is a fresh database instance, press `2` to enter the Registration flow. You will be asked to instantiate a username and a complex password. Behind the scenes, `database.py` generates a permanent SHA-256 cryptographic hash of your password and binds it to your username in the SQL table. Once successfully created, hit `1` to log in with the plaintext equivalents.
![Register and Login](images/registering-and-login.png)

### 2. Dynamically Logging an Expense using the AI Engine
Once your session is globally verified, the menu state changes. Press `1` to append a new transaction.
The interface will prompt for two distinct strings:
1. **Amount ($)** 
2. **Expense Description** 

In my testing scenario, I entered the phrase: `"uber to the airport"` for `$35.0`. 
The application intercepts the string `"uber to the airport"` and routes it to `ai_helper.py`. The helper executes a prompt to the Gemini model demanding a 1-word classification. Within ~400ms, the AI replies with exactly: **Transport**. The controller intercepts this string and automatically commits the row (User ID, Amount, Raw Description, AI Category, Timestamp) to the SQLite registry.
![Adding Expenses](images/adding-expenses.png)

### 3. Reviewing the Financial Ledger
After utilizing the CLI to log subsequent expenses (e.g., buying a burger for lunch, satisfying a monthly electricity bill, and purchasing a Netflix subscription), I pressed `2` to view my aggregated expenses. 

`main.py` opens a connection to the SQL instance, requests all `expenses` inherently tied to my specific session `user_id`, orders the results algorithmically by `DESC` date parameters, and streams them back to the UI in a perfectly mapped ASCII grid. Visually notice how perfectly the AI identified context and accurately tagged each row!
![Viewing Expenses](images/viewing-expense-table.png)

### 4. Session Termination (Logout & Exit)
Once the data entry is concluded, a user can securely press `3` to terminate their active session token, returning control to the primary unauthorized menu. From there, another user on the same physical machine can log in safely, or the original user can press `3` again to trigger a `sys.exit(0)` terminating the Python runtime entirely.
![Logout and Exit](images/logout-and-exit.png)

---

## Deep Dive: How the AI Engine Works Under the Hood

The crux of the "AI" within this application lives exclusively inside `ai_helper.py`. Let's explore the dual-node setup.

### The Primary NLP Mechanism (Generative AI API)
When a user feeds a description to the application, we don't just send the raw text to Google. We wrap the text in a highly specific, engineered "Few-Shot Prompt" constraint before transmission to the `gemini-1.5-flash` model:

> *"Categorize the following expense description into a single short category name (e.g., Food & Dining, Transport, Entertainment, Utilities, Shopping, Health, etc.). Just return the category name, nothing else. Description: [User Input]"*

Large Language Models inherently want to be chatty. If you just send "uber", they will respond with "Uber is a multinational transportation network company...". By explicitly engineering the prompt to say "Just return the category name, nothing else", we successfully lobotomize the chatbot aspect of the LLM, forcing it to act exclusively as a rigidly typed classification function. This allows us to take its clean `response.text` string and inject it straight into our SQL database without fear of schema corruption.

### The Offline Failsafe Mechanism (Local Hardcoded NLP)
A cardinal rule of backend engineering is redundancy. What if the user loses Wi-Fi connection? What if their API key expires? What if Google's endpoints suffer an outage?

I developed a sophisticated fallback mechanism nested within a standard `try / except` architecture. If the API invocation throws any exception whatsoever, the error is quietly ignored (`pass`) and execution drops vertically into the local dictionary algorithm.

```python
FALLBACK_CATEGORIES = {
    "Transport": ["uber", "lyft", "taxi", "bus", "train", "flight", "gas"],
    "Entertainment": ["movie", "cinema", "game", "netflix", "spotify"]
}
```
The algorithm forces the user input into a `.lower()` case format, iterates through multiple arrays mapping semantic keywords, and checks for overlaps using Python's `any()` function. If the algorithm spots the substring "netflix", it returns "Entertainment". If it finds absolutely no mapped arrays, it returns a safe "Miscellaneous" string. This ensures 100% uptime for the application, even in entirely air-gapped systems!

---

## Database Schema & ERD Mapping

In the interest of full academic transparency, here is the exact relational schema currently executing strictly inside `expense_tracker.db`. We employ a 1-to-Many foreign key relationship mapping `users -> expenses`.

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
Even though this is a CLI academic project, several real-world security paradigms were adhered to:
1. **Password Protection:** As previously analyzed, `.encode()` and `hashlib.sha256()` implementations protect end-user passwords against local database breaches.
2. **SQL Injection Armor:** By utilizing `?` placeholder parameters inside the `cursor.execute()` statements (e.g., `execute("SELECT id FROM users WHERE username = ?", (username,))`), malicious users cannot simply drop SQL payloads like `' OR '1'='1` into the username field to dump the database.
3. **Ignored Runtime Variables:** The inclusion of a robust `.gitignore` file guarantees that the `.env` file containing the physical API key, the `__pycache__` artifacts, and the physical `expense_tracker.db` binary are systematically rejected by Git, meaning no sensitive traces are ever pushed to a public GitHub repository.

---

## Error Handling & Edge Cases
Great CLI's shouldn't crash when humans make mistakes. 
- **Handling Invalid Floats**: If a user is asked for a price amount and typed `--`, `abc`, or an empty character, the terminal uses `try/except ValueError` loops to reject the input, display a human-readable warning ("Please enter a valid positive number"), and safely `continue` the `while` loop, as opposed to throwing a `Traceback` stack and violently crashing the app.
- **Handling Control Sequences**: Pressing `CTRL+C` in a terminal throws a `KeyboardInterrupt`. The app catches this universally wrapping the `main()` function, allowing it to print `Exiting...` and gracefully terminate the process utilizing `sys.exit(0)`.

---

## Future Scope & Production Enhancements
While this MVP (Minimum Viable Product) completely fulfills the requirements of the BYOP project, scaling the application out for production would involve implementing the following systems:
1. **Interactive Ascii Graphics:** While the terminal outputs strict text grids right now, integrating libraries like `plotext` would allow me to natively render colorful bar graphs and pie charts directly in the bash terminal, dynamically grouping user spending by AI categories against variable temporal contexts (e.g., sorting trailing 30-day graphs).
2. **Export capabilities (CSV/JSON/PDF):** Coding a `-export` argument flag that triggers the application to query all `user_id` rows and `.dump()` them via the `csv` python module so users can visually map their algorithmically calculated spending habits in Microsoft Excel.
3. **Hard Budget Constraints & Logic Limits:** Allowing users to hardcode rigid budget caps (e.g., "Max $200 allocated to Entertainment per 30 days"). The backend SQL engine would then be configured to automatically execute `SUM(amount)` aggregation algorithms every time a new expense is logged. If the new sum exceeds the defined constraint, the CLI would trigger an automated text-color altering warning protocol notifying the user of their breach!

---

## Acknowledgments
- Completely concepted, engineered, and executed for the *Fundamentals of AI and ML* course as the final, evaluated BYOP capstone project submission.
- Engineered primarily leveraging Python 3.8 and the incredible efficiency of Google's Generative AI Flash methodologies.
