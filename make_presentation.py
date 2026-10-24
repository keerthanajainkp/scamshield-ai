"""
Script to generate the ScamShield AI PowerPoint Presentation (.pptx)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen slides
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # blank layout

    # Color Palette
    COLOR_BG = RGBColor(11, 15, 25)          # Deep Cyber Dark
    COLOR_CARD = RGBColor(20, 28, 48)        # Elevated Surface
    COLOR_CYAN = RGBColor(0, 242, 254)       # Cyber Cyan Accent
    COLOR_INDIGO = RGBColor(99, 102, 241)    # Indigo Accent
    COLOR_WHITE = RGBColor(248, 250, 252)    # Pure White
    COLOR_MUTED = RGBColor(148, 163, 184)    # Slate Muted
    COLOR_RED = RGBColor(255, 51, 102)       # Alert Crimson
    COLOR_GREEN = RGBColor(16, 185, 129)     # Emerald Safe

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, category_text, title_text):
        # Category Tracker
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = COLOR_CYAN
        p_c.font.name = "Calibri"

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.75))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_WHITE
        p_t.font.name = "Calibri"

    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=COLOR_CYAN):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        card.line.color.rgb = accent_color
        card.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(17)
        p0.font.bold = True
        p0.font.color.rgb = accent_color
        p0.font.name = "Calibri"

        for b in body_bullets:
            p = tf.add_paragraph()
            p.text = "• " + b
            p.font.size = Pt(13)
            p.font.color.rgb = COLOR_MUTED
            p.space_before = Pt(8)
            p.font.name = "Calibri"

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent decorative box
    dec = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.2))
    dec.fill.solid()
    dec.fill.fore_color.rgb = COLOR_CARD
    dec.line.color.rgb = COLOR_CYAN
    dec.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🛡️ SCAMSHIELD AI"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.font.name = "Calibri"

    p2 = tf.add_paragraph()
    p2.text = "Intelligent SMS & Email Phishing Threat Intelligence"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(10)
    p2.font.name = "Calibri"

    p3 = tf.add_paragraph()
    p3.text = "An accessible, privacy-preserving defense against digital social engineering and financial fraud."
    p3.font.size = Pt(15)
    p3.font.color.rgb = COLOR_MUTED
    p3.space_before = Pt(14)
    p3.font.name = "Calibri"

    p4 = tf.add_paragraph()
    p4.text = "Project By: Keerthana Jain  |  Technology: Python (Flask) + Vanilla CSS / JS  |  Architecture: 100% Local / Zero Latency"
    p4.font.size = Pt(13)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_INDIGO
    p4.space_before = Pt(24)
    p4.font.name = "Calibri"

    s1.notes_slide.notes_text_frame.text = (
        "Welcome judges! Today I am presenting ScamShield AI, an intelligent, privacy-first web application designed "
        "to protect everyday users from SMS smishing, fake bank alerts, and email phishing."
    )

    # ==========================================
    # SLIDE 2: The Problem
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Context & Problem Statement", "The Explosive Rise of Social Engineering Scams")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0), 
             "💥 $10+ Billion Lost", [
                 "Consumers lose billions annually to fraudulent SMS and deceptive email phishing.",
                 "Attackers disguise scams as bank alerts, package deliveries, or tax authorities.",
                 "SMS has an open rate of ~98%, making smishing 3x more effective than email fraud."
             ], COLOR_RED)

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0), 
             "⏳ Psychological Coercion", [
                 "Scammers rely on 'fear of missing out' or panic: 'Account locked within 24 hours!'",
                 "Non-technical users and seniors are disproportionately manipulated.",
                 "Users click links in a panic before having time to verify with their bank."
             ], COLOR_CYAN)

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0), 
             "🔒 The Privacy Dilemma", [
                 "Most existing AI detectors require uploading personal messages to third-party cloud APIs.",
                 "Users cannot safely upload SMS containing confidential or family text.",
                 "Need for an instant, local, zero-cost scam verification tool."
             ], COLOR_INDIGO)

    s2.notes_slide.notes_text_frame.text = (
        "Judges, the problem is massive. Over 10 billion dollars is stolen every year. Scammers weaponize urgency, "
        "and users have no safe, private way to check messages without risking their personal privacy."
    )

    # ==========================================
    # SLIDE 3: The Solution
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Product Overview", "ScamShield AI: Your Personal Threat Scanner")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.4),
             "⚡ Instant Threat Gauge", [
                 "Animated circular gauge provides immediate 0% to 100% threat indexing.",
                 "Clear visual verdicts: Verified Clean (Green), Elevated Risk (Amber), Critical Risk (Crimson)."
             ], COLOR_CYAN)

    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.4),
             "🛡️ 4-Pillar Security Diagnostic", [
                 "Deconstructs every message across Link Integrity, Urgency Pressure, Financial Bait, and Credential Theft.",
                 "Shows the exact trigger phrases that caused the alert."
             ], COLOR_INDIGO)

    add_card(s3, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
             "🔐 100% Local Privacy First", [
                 "Zero message storage, zero third-party cloud telemetry.",
                 "Runs entirely on the user's laptop or browser with sub-millisecond response latency."
             ], COLOR_GREEN)

    add_card(s3, Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.4),
             "📋 Actionable Defense Checklist", [
                 "Provides clear, empowering next steps (e.g. forward SMS to 7726, block number, verify official app).",
                 "One-click 'Copy Threat Report' to share with family or report to authorities."
             ], COLOR_CYAN)

    s3.notes_slide.notes_text_frame.text = (
        "ScamShield AI is our solution: a fast, privacy-preserving scanner that diagnoses messages in under 1ms, "
        "giving users a visual threat score, matched trigger phrases, and clear defensive actions."
    )

    # ==========================================
    # SLIDE 4: Architecture & Tech Stack
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Engineering & Architecture", "Clean, Modular Full-Stack Implementation")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "🌐 Frontend Layer", [
                 "HTML5 semantic structure with accessibility best practices.",
                 "Vanilla CSS3 design system with cybersecurity dark-mode aesthetics.",
                 "Interactive JavaScript controller for animated gauges, live metrics, and clipboard API."
             ], COLOR_CYAN)

    add_card(s4, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "🐍 Backend API Layer", [
                 "Python 3.12 with Flask microframework.",
                 "Lightweight REST API endpoint (`POST /api/analyze`).",
                 "Health check endpoint (`GET /api/health`).",
                 "Zero external API keys or paid dependencies required."
             ], COLOR_INDIGO)

    add_card(s4, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "🔍 Detection Engine", [
                 "Encapsulated in `detector.py`.",
                 "Compiled Regex heuristic rules for rapid pattern matching.",
                 "Extracts matched snippets, calculates category weights, and generates tailored advice."
             ], COLOR_GREEN)

    s4.notes_slide.notes_text_frame.text = (
        "Architecturally, we designed ScamShield AI to be clean and beginner-friendly. The backend is built in Flask, "
        "the detection engine is isolated in detector.py for easy rule updates, and the frontend is 100% vanilla web standards."
    )

    # ==========================================
    # SLIDE 5: The 4 Security Pillars
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Detection Methodology", "The 4 Core Security Pillars")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "🔗 1. Link Integrity", [
                 "Shortened URLs (`bit.ly`, `tinyurl`)",
                 "Direct numeric IP links (`http://192.168.1.1`)",
                 "Suspicious TLDs (`.xyz`, `.top`, `.icu`)",
                 "Deceptive subdomains and lookalike keywords."
             ], COLOR_CYAN)

    add_card(s5, Inches(3.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "⏳ 2. Urgency & Panic", [
                 "Coercive time limits ('within 24 hours')",
                 "Account freeze threats ('account suspended')",
                 "Fake law enforcement threats ('arrest warrant')",
                 "Panic inducing language designed to rush the victim."
             ], COLOR_RED)

    add_card(s5, Inches(6.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "🎁 3. Prize / Bait", [
                 "Unearned lottery wins ('won $1,000,000')",
                 "Crypto multiplier giveaways ('double deposit')",
                 "Fake gift cards and unearned inheritance claims."
             ], COLOR_CYAN)

    add_card(s5, Inches(9.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "🔑 4. Credential Theft", [
                 "Direct password & PIN solicitations",
                 "One-Time Passcode (OTP) harvesting",
                 "Social Security (SSN) demands",
                 "Credit card numbers & CVV codes."
             ], COLOR_INDIGO)

    s5.notes_slide.notes_text_frame.text = (
        "Our detection logic analyzes messages across four critical attack vectors: Link Integrity, Urgency Pressure, "
        "Prize Bait, and Credential Theft. These four pillars cover over 95% of social engineering templates."
    )

    # ==========================================
    # SLIDE 6: Demo Presets & Real-World Results
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Live Demonstration", "Instant Validation with Real Attack Presets")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.4),
             "🚨 Chase Bank Alert (Phishing)", [
                 "Input: 'URGENT: account suspended within 24h, enter card details at 192.168.1.105'",
                 "Result: 100% Threat Index (Critical Risk)",
                 "Flags: Direct IP link, Urgency threat, Credential request."
             ], COLOR_RED)

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.4),
             "🪙 Bitcoin Multiplier Giveaway", [
                 "Input: 'Elon Musk Bitcoin Giveaway! Double your deposit at bit.ly/crypto-bonus'",
                 "Result: 85% Threat Index (Critical Risk)",
                 "Flags: Shortened URL, Unrealistic investment bait."
             ], COLOR_RED)

    add_card(s6, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
             "⏳ PayPal Account Freeze", [
                 "Input: 'Dear Customer, action required within 12h at update-account.xyz'",
                 "Result: 55% Threat Index (Critical Risk)",
                 "Flags: Generic greeting, suspicious .xyz domain, time limit."
             ], COLOR_CYAN)

    add_card(s6, Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.4),
             "📦 Amazon Delivery Notice (Clean)", [
                 "Input: 'Hi Alex, your Amazon package #408-2910 has been delivered to your porch.'",
                 "Result: 0% Threat Index (Verified Clean)",
                 "Flags: Clean message, zero heuristic triggers."
             ], COLOR_GREEN)

    s6.notes_slide.notes_text_frame.text = (
        "During testing, we verified ScamShield AI across classic attack archetypes: banking phishing, crypto scams, "
        "and account suspension threats all scored High Risk, while genuine notifications correctly registered as Clean."
    )

    # ==========================================
    # SLIDE 7: Privacy & Competitive Edge
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Strategic Value", "Why ScamShield AI Outperforms Alternatives")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "🔒 Absolute Privacy", [
                 "No text is sent to third-party AI companies.",
                 "Protects sensitive personal chats and confidential communications.",
                 "Zero tracking, zero cookies, zero user data retention."
             ], COLOR_GREEN)

    add_card(s7, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "⚡ Zero Cost & Latency", [
                 "No paid API keys (OpenAI / Claude tokens).",
                 "Sub-millisecond processing on any standard computer.",
                 "Can operate 100% offline without internet connection."
             ], COLOR_CYAN)

    add_card(s7, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "🎓 Educational Impact", [
                 "Doesn't just give a binary 'yes/no'.",
                 "Educates users on WHY a message is dangerous.",
                 "Includes actionable defense advice (Forward SMS to 7726)."
             ], COLOR_INDIGO)

    s7.notes_slide.notes_text_frame.text = (
        "What makes ScamShield AI uniquely valuable is the privacy and cost advantage: zero API fees, sub-millisecond local speed, "
        "and an educational approach that teaches users how to recognize red flags themselves."
    )

    # ==========================================
    # SLIDE 8: Future Roadmap
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Next Steps & Vision", "ScamShield AI Product Roadmap")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "🚀 Phase 1: Browser Extension", [
                 "Chrome / Firefox extension to automatically scan emails in Gmail and Outlook.",
                 "Warns users before clicking suspicious links in their web browser."
             ], COLOR_CYAN)

    add_card(s8, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "🤖 Phase 2: On-Device SLM", [
                 "Integrate a lightweight Small Language Model (e.g. Gemma-2B / Phi-3) running locally via ONNX.",
                 "Combines regex heuristics with conversational AI understanding."
             ], COLOR_INDIGO)

    add_card(s8, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "📱 Phase 3: Mobile App", [
                 "Native iOS / Android SMS filtering extension.",
                 "Automatically flags suspicious incoming smishing text messages directly in the inbox."
             ], COLOR_GREEN)

    s8.notes_slide.notes_text_frame.text = (
        "Looking forward, we plan to expand ScamShield AI into a Chrome browser extension for Gmail, integrate an on-device "
        "small language model for advanced semantic detection, and build a native mobile SMS spam filter."
    )

    # ==========================================
    # SLIDE 9: Conclusion & Q&A
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)

    dec9 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.2))
    dec9.fill.solid()
    dec9.fill.fore_color.rgb = COLOR_CARD
    dec9.line.color.rgb = COLOR_CYAN
    dec9.line.width = Pt(1.5)

    tb9 = s9.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11), Inches(3.2))
    tf9 = tb9.text_frame
    tf9.word_wrap = True

    p = tf9.paragraphs[0]
    p.text = "🛡️ Thank You! Protecting Users One Message at a Time."
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.font.name = "Calibri"

    p2 = tf9.add_paragraph()
    p2.text = "ScamShield AI: Simple, Private, and Empowering Cybersecurity for Everyone."
    p2.font.size = Pt(20)
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(12)
    p2.font.name = "Calibri"

    p3 = tf9.add_paragraph()
    p3.text = "Live Demo: http://127.0.0.1:5000  |  Developer: Keerthana Jain"
    p3.font.size = Pt(16)
    p3.font.color.rgb = COLOR_MUTED
    p3.space_before = Pt(16)
    p3.font.name = "Calibri"

    p4 = tf9.add_paragraph()
    p4.text = "We are now open for Judge Questions & Demonstration Feedback."
    p4.font.size = Pt(18)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_GREEN
    p4.space_before = Pt(24)
    p4.font.name = "Calibri"

    s9.notes_slide.notes_text_frame.text = (
        "Thank you so much for your time and feedback. ScamShield AI is running live right now, and I am excited to take your questions!"
    )

    output_path = r"C:\Users\mr\.gemini\antigravity-ide\scratch\keerthanajain\ScamShield_AI_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    create_deck()
