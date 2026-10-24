"""
ScamShield AI - Rule-Based Scam Detection Engine
================================================
This file contains the logic that analyzes SMS and email text messages
for common patterns found in scams, phishing attacks, and fraud.

For beginners:
- A "rule" looks for specific trigger words or patterns using regular expressions (regex).
- Each rule adds points to a "risk score".
- Total risk score determines the final Risk Level (Low, Medium, High).
"""

import re
from typing import Dict, List, Any


# 1. Suspicious Links & Web Patterns
LINK_PATTERNS = [
    # Shortened URLs frequently used to disguise malicious sites
    (r"\b(bit\.ly|tinyurl\.com|t\.co|goo\.gl|is\.gd|cutt\.ly|ow\.ly|rb\.gy)\b", 
     "Uses a shortened URL (scammers hide actual destination URLs behind short links)",
     "High"),
    # IP address directly inside a link (e.g. http://192.168.1.1/login)
    (r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", 
     "Contains a direct numeric IP address link instead of a legitimate domain name",
     "Critical"),
    # Suspicious domain extensions often abused by free or cheap domains
    (r"https?://[^\s]+\.(xyz|top|club|work|buzz|icu|live|click|tk|ml|ga|cf|gq)\b", 
     "Link contains a high-risk or suspicious top-level domain (.xyz, .top, etc.)",
     "High"),
    # Phishing lookalike words in links
    (r"https?://[^\s]*(verify|secure|update-account|login|signin|banking|support-team)[^\s]*", 
     "Link includes security-themed keywords often used in fake login pages",
     "Medium"),
]

# 2. Urgent / Threatening Language (Pressure Tactics)
URGENT_PATTERNS = [
    (r"\b(urgent|urgently|act now|immediate action|respond immediately|within 24 hours|within 12 hours|last chance|final notice|final warning)\b", 
     "Uses extreme urgency to pressure you into acting without thinking",
     "Medium"),
    (r"\b(account suspended|account blocked|account will be terminated|unauthorized transaction|unusual activity detected|security breach)\b", 
     "Threatens immediate negative consequences like account suspension or loss of funds",
     "High"),
    (r"\b(arrest warrant|law enforcement|legal action|police|court summons)\b", 
     "Impersonates authorities or threatens legal action to cause panic",
     "Critical"),
]

# 3. Prize, Lottery, and Free Money Scams (Too Good To Be True)
PRIZE_PATTERNS = [
    (r"\b(you have won|winner|won a lottery|cash prize|free gift|claim your prize|selected as a winner|jackpot)\b", 
     "Claims you won an unearned prize or lottery (classic advance-fee scam)",
     "High"),
    (r"\b(crypto bonus|bitcoin giveaway|double your deposit|guaranteed return|risk-free investment)\b", 
     "Promotes unrealistic investment returns or cryptocurrency giveaways",
     "High"),
    (r"\b(inheritance|unclaimed funds|beneficiary|foreign diplomat|million dollars)\b", 
     "Mentions unexpected inheritance or millions of dollars in unclaimed funds",
     "Medium"),
]

# 4. Sensitive Data & Financial Requests (Credential Harvesting)
CREDENTIAL_PATTERNS = [
    (r"\b(enter your password|send password|confirm your pin|reset your pin|share otp|one-time code|auth code)\b", 
     "Asks for your password, PIN, or One-Time Passcode (legitimate companies will NEVER ask for these)",
     "Critical"),
    (r"\b(social security|ssn|credit card number|cvv|cvc|expiration date|card details)\b", 
     "Demands sensitive identity or credit card security codes",
     "Critical"),
    (r"\b(wire transfer|western union|moneygram|buy gift cards|apple gift card|pay with gift card)\b", 
     "Requests untraceable payment methods such as wire transfers or retail gift cards",
     "High"),
    (r"\b(send your bank account|routing number|online banking credentials)\b", 
     "Requests direct banking credentials or routing numbers",
     "Critical"),
]


def analyze_message(text: str) -> Dict[str, Any]:
    """
    Analyzes a given text message or email and returns a rich analysis result
    including category breakdown, detected snippets, threat score, and actions.
    """
    if not text or not text.strip():
        return {
            "risk_level": "Low",
            "risk_score": 0,
            "category_scores": {
                "links": 0,
                "urgency": 0,
                "prizes": 0,
                "credentials": 0
            },
            "findings": [],
            "matched_snippets": [],
            "action_items": ["Paste a message in the input box to start scanning."],
            "advice": "Please enter a message to analyze.",
            "disclaimer": "This analysis is an educational rule-based estimate, not a guarantee."
        }

    clean_text = text.strip()
    findings: List[Dict[str, Any]] = []
    matched_snippets: List[str] = []
    score = 0

    category_scores = {
        "links": 0,
        "urgency": 0,
        "prizes": 0,
        "credentials": 0
    }

    # Helper function to check pattern categories
    def run_checks(patterns, category_key: str, category_label: str, points_per_hit: int):
        nonlocal score
        found = False
        for pattern, reason, severity in patterns:
            match = re.search(pattern, clean_text, re.IGNORECASE)
            if match:
                matched_text = match.group(0)
                findings.append({
                    "category": category_label,
                    "category_key": category_key,
                    "reason": reason,
                    "severity": severity,
                    "matched_text": matched_text
                })
                matched_snippets.append(matched_text)
                score += points_per_hit
                category_scores[category_key] += points_per_hit
                found = True
        return found

    # Run checks across all 4 categories
    has_links = run_checks(LINK_PATTERNS, "links", "Suspicious Links", 25)
    has_urgency = run_checks(URGENT_PATTERNS, "urgency", "Urgent Pressure", 20)
    has_prize = run_checks(PRIZE_PATTERNS, "prizes", "Prize / Reward Bait", 25)
    has_creds = run_checks(CREDENTIAL_PATTERNS, "credentials", "Credential Harvesting", 30)

    # General check: generic greeting + link or money request
    greeting_match = re.search(r"\b(dear customer|dear user|valued customer|attn:)\b", clean_text, re.IGNORECASE)
    if greeting_match and (has_links or has_urgency or has_creds):
        matched_greeting = greeting_match.group(0)
        findings.append({
            "category": "Generic Greeting",
            "category_key": "urgency",
            "reason": "Uses a vague greeting ('Dear Customer') instead of addressing you by your actual name",
            "severity": "Medium",
            "matched_text": matched_greeting
        })
        matched_snippets.append(matched_greeting)
        score += 10
        category_scores["urgency"] += 10

    # Cap category scores and total score at 100
    score = min(score, 100)
    for k in category_scores:
        category_scores[k] = min(category_scores[k], 100)

    # Determine Risk Level and Action Items
    if score >= 45:
        risk_level = "High"
        advice = (
            "CRITICAL ALERT: Multiple high-confidence fraud indicators detected! This message displays classic "
            "tactics used by phishing networks and scam operations. Do NOT tap any links, do NOT reply, and NEVER provide OTP codes or banking credentials."
        )
        action_items = [
            "Do NOT click any web links or dial numbers mentioned in the message.",
            "Do NOT share one-time passcodes (OTP), passwords, PINs, or card digits.",
            "Block the sender's phone number or email address immediately.",
            "Report the message as spam to your cellular provider (forward SMS to 7726) or email provider."
        ]
    elif score >= 20:
        risk_level = "Medium"
        advice = (
            "ELEVATED RISK: Warning indicators were identified. Scammers often use subtle phrasing or external redirects. "
            "Verify the claimed sender independently through an official app, website, or customer support phone number."
        )
        action_items = [
            "Inspect links carefully before clicking; do not enter login details on unverified pages.",
            "Contact the institution directly using the official phone number on your card or bill.",
            "Verify whether any urgent account status changes actually appear in your official account portal."
        ]
    else:
        risk_level = "Low"
        advice = (
            "LOW RISK: No recognized scam patterns were flagged. The message appears to be standard communication. "
            "However, always stay observant—cybercriminals frequently devise novel wording."
        )
        action_items = [
            "Standard security hygiene applies: keep your device software updated.",
            "Never share passwords or confidential credentials over text message."
        ]

    return {
        "risk_level": risk_level,
        "risk_score": score,
        "category_scores": category_scores,
        "findings": findings,
        "matched_snippets": list(set(matched_snippets)),
        "advice": advice,
        "action_items": action_items,
        "character_count": len(clean_text),
        "disclaimer": "Notice: ScamShield AI provides rule-based estimates for educational purposes, not an absolute security guarantee."
    }
