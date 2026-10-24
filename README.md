# 🛡️ ScamShield AI - SMS & Email Scam Detector

Welcome to **ScamShield AI**! This is a beginner-friendly web application designed to help you analyze suspicious SMS messages, emails, and chat messages for signs of phishing, urgency tactics, fake lottery scams, and banking fraud.

---

## 📂 Project Structure & What Each File Does

Here is a breakdown of every file in this folder:

| File / Folder | Purpose |
| :--- | :--- |
| [`app.py`](file:///C:/Users/mr/.gemini/antigravity-ide/scratch/keerthanajain/app.py) | **The Backend Server**: A Python application built with Flask. It serves the web page to your browser and provides an API endpoint (`/api/analyze`) that receives messages and returns scam analysis results. |
| [`detector.py`](file:///C:/Users/mr/.gemini/antigravity-ide/scratch/keerthanajain/detector.py) | **The Detection Engine**: Contains pure, easy-to-read Python rules (using regular expressions) that check for suspicious links, pressure language, fake prizes, and credential harvesting. |
| [`requirements.txt`](file:///C:/Users/mr/.gemini/antigravity-ide/scratch/keerthanajain/requirements.txt) | **Dependencies List**: Lists the required Python library (`Flask`) needed to run the project. |
| [`templates/index.html`](file:///C:/Users/mr/.gemini/antigravity-ide/scratch/keerthanajain/templates/index.html) | **The Web Interface**: Modern, accessible HTML structure featuring a large text area, quick example buttons, a threat score meter, and warning badges. |
| [`static/style.css`](file:///C:/Users/mr/.gemini/antigravity-ide/scratch/keerthanajain/static/style.css) | **Visual Styling**: Sleek, responsive dark-mode styling with smooth animations, glowing risk indicators, and clean cards. |
| [`static/script.js`](file:///C:/Users/mr/.gemini/antigravity-ide/scratch/keerthanajain/static/script.js) | **Frontend Interactivity**: Handles button clicks, preset loading, character counting, calling the Flask backend, and updating the results card. |

---

## 🚀 How to Run ScamShield AI on Your Laptop

### Step 1: Open PowerShell or Terminal
Open Windows PowerShell and navigate to the project directory:
```powershell
cd C:\Users\mr\.gemini\antigravity-ide\scratch\keerthanajain
```
*Explanation: `cd` stands for "change directory" and moves your terminal into the ScamShield AI project folder.*

### Step 2: Install Dependencies
Run the following command to install Flask:
```powershell
python -m pip install -r requirements.txt
```
*Explanation: `pip` is Python's package installer. This command installs `Flask` so Python can run web servers.*

### Step 3: Start the Application
Start the Flask web server by typing:
```powershell
python app.py
```
*Explanation: This starts the local server. You will see output stating that the server is running on `http://127.0.0.1:5000`.*

### Step 4: Open in Your Browser
Open your favorite browser (Google Chrome, Microsoft Edge, Firefox, Brave, etc.) and go to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

### Step 5: Stop the Server When Finished
To stop the server at any time, return to your PowerShell window and press:
`CTRL + C`

---

## 🧪 Testing ScamShield AI

You can test the app using the built-in preset buttons or by pasting your own text:

1. **🚨 Bank Alert (High Risk Example):**
   > *"URGENT from Chase Bank: We detected an unauthorized transaction on your card. Your account will be suspended within 24 hours unless you verify immediately. Visit http://192.168.1.105/login and enter your password and card details."*
   - Flags: Suspicious IP link, urgency, credential request.
   - Result: **High Risk (90% - 100%)**

2. **🎁 Lottery Prize (High Risk Example):**
   > *"Congratulations! You have won a $1,000,000 cash prize in our national lottery! Claim your prize now at http://bit.ly/winner-jackpot-2026. Send your bank account and SSN to release funds."*
   - Flags: Shortened link, lottery scam, sensitive banking info request.
   - Result: **High Risk (80% - 100%)**

3. **✅ Safe Delivery (Low Risk Example):**
   > *"Hi Alex, your Amazon package with tracking number #408-2910 has been delivered to your front porch. Have a wonderful weekend!"*
   - Flags: None.
   - Result: **Low Risk (0%)**

---

## ⚠️ Important Educational Notice
ScamShield AI uses rule-based keyword and pattern matching. It serves as an educational aid and provides an **estimate**, not an absolute 100% guarantee. Always verify suspicious communications directly with the official company or institution.
