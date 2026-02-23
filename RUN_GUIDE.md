# How to Run and Test the Student Governance System

This guide will help you get the entire system running on your computer from scratch.

## Prerequisites
Before you start, make sure you have these installed:
1. **Python**: [Download here](https://www.python.org/downloads/)
2. **MongoDB**: [Download here](https://www.mongodb.com/try/download/community) (Make sure the MongoDB service is **Running**)

---

## Step 1: Install Dependencies
Open your terminal and run this command in the main project folder:
```bash
pip install -r requirements.txt
```

---

## Step 2: Start the Blockchain Nodes
The blockchain needs to be running first to record the votes.
1. Open a **new terminal**.
2. Run these commands:
   ```bash
   cd blockchain_model
   sh start_nodes.sh
   ```
*Keep this terminal open.*

---

## Step 3: Start the Backend API
The backend handles student logins and talks to the blockchain.
1. Open **another new terminal**.
2. Stay in the **main project folder** (do not cd into backend).
3. Run this command:
   ```bash
   python3 -m uvicorn backend.main:app --reload --port 8000
   ```
*Keep this terminal open as well.*

---

## Step 4: How to Test (The Simple Way)
We will use the "Interactive Documentation" to test the system without writing any code.

1. Open your web browser and go to: **[http://localhost:8000/docs](http://localhost:8000/docs)**
2. You will see a list of actions you can perform:

### A. Register a Student
- Click on **POST /register**.
- Click **Try it out**.
- Change the `roll_number` and `password` to whatever you like.
- Click **Execute**. (Result: Student created in MongoDB!)

### B. Login & Get Access
- Click on **POST /login**.
- Click **Try it out**.
- Enter your `username` (roll number) and `password`.
- Click **Execute**.
- **Copy the text** inside the `"access_token": "..."` quotes.
- Scroll to the top of the page and click the green **Authorize** button.
- Paste the token and click **Authorize**, then **Close**.

### C. Cast a Vote
- Click on **POST /vote**.
- Click **Try it out**.
- Enter a candidate ID (e.g., `"cand_1"`).
- Click **Execute**.
- (The backend now sends your vote to the blockchain and updates MongoDB!)

### D. Check Results
- Click on **GET /results**.
- Click **Try it out** -> **Execute**.
- You will see the live vote counts directly from the blockchain!

---

## Step 5: Visualizing the Blockchain Dashboard (Premium)
For a better experience, you can use our built-in real-time dashboard:
1. Open your browser to: **[http://localhost:8000/dashboard](http://localhost:8000/dashboard)**
2. You will see all 3 blockchain nodes in real-time.
3. You can manually:
   - **Add Votes**: Directly to a specific node.
   - **Mine Blocks**: To solidify pending votes.
   - **Sync Chain**: To resolve any differences between nodes using our consensus algorithm.
