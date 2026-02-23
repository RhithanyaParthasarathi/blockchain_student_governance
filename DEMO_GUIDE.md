# 🗳️ Student Governance System: Step-by-Step Guide

This guide will show you how to set up, run, and test the blockchain voting system from start to finish.

---

## 🚀 Phase 1: Getting Everything Running

### 1. Install Dependencies
Open your terminal in the project folder and run:
```bash
pip install -r requirements.txt
```

### 2. Start the Blockchain (3 Nodes)
The blockchain stores the votes securely.
- Open a **new terminal**.
- Run these commands:
  ```bash
  cd blockchain_model
  sh start_nodes.sh
  ```
*Leave this terminal running.*

### 3. Start the Backend API
The backend handles student accounts and talking to the blockchain.
- Open **another new terminal**.
- Run this command (from the main project folder):
  ```bash
  python3 -m uvicorn backend.main:app --reload --port 8000
  ```
*Leave this terminal running too.*

---

## 📊 Phase 2: Visual Testing (Recommended for Demo)

The Dashboard provides a premium, visual interface to test the entire system easily.

### 1. Open the Dashboard
In your browser, go to: **[http://localhost:8000/dashboard](http://localhost:8000/dashboard)**

### 2. Check Network Health
At the top, verify that **Node 1, Node 2, and Node 3** have green indicators. This confirms your private blockchain network is active.

### 3. Register & Login
*   **Create Account**: Click the **Register** tab on the left. Enter a roll number (e.g., `STU_101`) and a password. Click **Create Account**.
*   **Login**: Switch to the **Login** tab, enter your details, and click **Login to Vote**.
*   *Once logged in, your student ID will appear in a green box on the left.*

### 4. Cast Your Vote
*   Select a candidate (Alice or Bob) from the dropdown.
*   Click **Submit Encrypted Vote**.
*   A confirmation alert will appear.

### 5. Verify the Ledger
*   Look at the **Live Verified Ledger** on the right side of the screen.
*   Your vote (Roll Number + Choice) will appear here once confirmed.
*   **Pro Tip**: If it doesn't appear immediately, click the **⚒️ Solidify Blockchain (Mine)** link at the bottom left to force a new block.

---

## 🧪 Phase 3: Alternative Testing (Interactive Docs)

If you want to show the underlying API calls:
Go to: **[http://localhost:8000/docs](http://localhost:8000/docs)**
1. **POST /register**: Create a student account.
2. **POST /login**: Get your `"access_token"`.
3. **Authorize**: Click the green button at the top and paste your token.
4. **POST /vote**: Submit a vote manually.
5. **GET /results**: See the raw json tallies from the blockchain.

---

### Tips for a Great Presentation:
- **Double Voting**: Try voting twice with the same account. The system will block you!
- **Transparency**: No one can delete or change a vote once it is on the "Verified Ledger."
- **Resilience**: Even if one blockchain node is closed, the others keep the election running!
