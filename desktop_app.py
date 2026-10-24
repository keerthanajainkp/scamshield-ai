"""
ScamShield AI - Native Python Desktop Application
=================================================
A standalone GUI application built with Python's standard tkinter library.
Runs directly on Windows without requiring a browser or external dependencies!
"""

import tkinter as tk
from tkinter import ttk, messagebox
from detector import analyze_message

# Theme Palette
BG_DARK = "#070a13"
BG_CARD = "#111827"
BG_INPUT = "#0b1120"
CYAN = "#00f2fe"
INDIGO = "#818cf8"
TEXT_WHITE = "#f8fafc"
TEXT_MUTED = "#94a3b8"
RED = "#ff3366"
AMBER = "#f59e0b"
GREEN = "#10b981"


class ScamShieldDesktopApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ScamShield AI - Desktop Threat Scanner")
        self.geometry("900x750")
        self.minsize(800, 650)
        self.configure(bg=BG_DARK)

        # Style configuration
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.build_ui()

    def build_ui(self):
        # Header Frame
        header = tk.Frame(self, bg=BG_CARD, padx=20, pady=14, relief=tk.FLAT)
        header.pack(fill=tk.X, padx=16, pady=(16, 10))

        title_lbl = tk.Label(
            header,
            text="🛡️ ScamShield AI Desktop",
            font=("Segoe UI", 18, "bold"),
            fg=CYAN,
            bg=BG_CARD
        )
        title_lbl.pack(side=tk.LEFT)

        subtitle_lbl = tk.Label(
            header,
            text="Local Heuristic Threat Intelligence",
            font=("Segoe UI", 10),
            fg=TEXT_MUTED,
            bg=BG_CARD
        )
        subtitle_lbl.pack(side=tk.LEFT, padx=(12, 0), pady=(4, 0))

        status_chip = tk.Label(
            header,
            text="● ENGINE ACTIVE",
            font=("Segoe UI", 9, "bold"),
            fg=GREEN,
            bg="#064e3b",
            padx=10,
            pady=4
        )
        status_chip.pack(side=tk.RIGHT)

        # Preset Buttons Row
        preset_frame = tk.Frame(self, bg=BG_DARK)
        preset_frame.pack(fill=tk.X, padx=16, pady=4)

        preset_lbl = tk.Label(preset_frame, text="Quick Presets:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=BG_DARK)
        preset_lbl.pack(side=tk.LEFT, padx=(0, 8))

        presets = [
            ("🚨 Bank Alert", "URGENT from Chase Bank: unauthorized transaction detected. Account suspended within 24h. Visit http://192.168.1.105/login and enter password and card details."),
            ("🎁 Lottery Winner", "Congratulations! You won $1,000,000 cash prize in our lottery! Claim prize now at http://bit.ly/winner-jackpot-2026. Send bank account and SSN."),
            ("⏳ PayPal Freeze", "FINAL NOTICE: Unusual activity detected on PayPal. Action required within 12 hours at https://update-account.xyz"),
            ("📦 Safe Delivery", "Hi Alex, your Amazon package with order #408-2910 has been delivered to your front porch. Have a great day!")
        ]

        for label, text in presets:
            btn = tk.Button(
                preset_frame,
                text=label,
                font=("Segoe UI", 8, "bold"),
                fg=TEXT_WHITE,
                bg="#1f2937",
                activebackground=CYAN,
                activeforeground="#000",
                relief=tk.FLAT,
                padx=8,
                pady=3,
                cursor="hand2",
                command=lambda t=text: self.load_preset(t)
            )
            btn.pack(side=tk.LEFT, padx=4)

        # Input Frame
        input_frame = tk.Frame(self, bg=BG_CARD, padx=16, pady=12)
        input_frame.pack(fill=tk.BOTH, expand=False, padx=16, pady=8)

        input_title = tk.Label(input_frame, text="Message Input (SMS / Email / Chat):", font=("Segoe UI", 10, "bold"), fg=TEXT_WHITE, bg=BG_CARD)
        input_title.pack(anchor="w", pady=(0, 6))

        self.text_input = tk.Text(
            input_frame,
            height=6,
            font=("Segoe UI", 11),
            bg=BG_INPUT,
            fg=TEXT_WHITE,
            insertbackground=CYAN,
            relief=tk.FLAT,
            padx=12,
            pady=10,
            wrap=tk.WORD
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)

        # Action Buttons Row
        btn_row = tk.Frame(input_frame, bg=BG_CARD)
        btn_row.pack(fill=tk.X, pady=(10, 0))

        self.scan_btn = tk.Button(
            btn_row,
            text="🔍 Scan Message with ScamShield",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#2563eb",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.run_scan
        )
        self.scan_btn.pack(side=tk.LEFT)

        clear_btn = tk.Button(
            btn_row,
            text="Clear",
            font=("Segoe UI", 10),
            fg=TEXT_MUTED,
            bg="#1f2937",
            activebackground="#374151",
            activeforeground=TEXT_WHITE,
            relief=tk.FLAT,
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.clear_input
        )
        clear_btn.pack(side=tk.LEFT, padx=10)

        # Results Frame
        self.results_frame = tk.Frame(self, bg=BG_CARD, padx=16, pady=14)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(8, 16))

        res_header = tk.Frame(self.results_frame, bg=BG_CARD)
        res_header.pack(fill=tk.X, pady=(0, 8))

        res_title = tk.Label(res_header, text="Threat Assessment Results", font=("Segoe UI", 12, "bold"), fg=TEXT_WHITE, bg=BG_CARD)
        res_title.pack(side=tk.LEFT)

        self.risk_badge = tk.Label(
            res_header,
            text="READY TO SCAN",
            font=("Segoe UI", 10, "bold"),
            fg=CYAN,
            bg="#0f172a",
            padx=12,
            pady=4
        )
        self.risk_badge.pack(side=tk.RIGHT)

        # Score Row
        score_row = tk.Frame(self.results_frame, bg=BG_CARD)
        score_row.pack(fill=tk.X, pady=6)

        self.score_label = tk.Label(score_row, text="Threat Index: 0%", font=("Segoe UI", 11, "bold"), fg=CYAN, bg=BG_CARD)
        self.score_label.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(score_row, orient=tk.HORIZONTAL, length=400, mode="determinate")
        self.progress.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(20, 0))

        # Advice Text
        self.advice_label = tk.Label(
            self.results_frame,
            text="Paste a message above and click 'Scan Message' to diagnose.",
            font=("Segoe UI", 9),
            fg=TEXT_MUTED,
            bg="#0b1120",
            wraplength=820,
            justify=tk.LEFT,
            padx=12,
            pady=8
        )
        self.advice_label.pack(fill=tk.X, pady=8)

        # Findings Treeview
        findings_lbl = tk.Label(self.results_frame, text="Detected Warning Signs:", font=("Segoe UI", 10, "bold"), fg=TEXT_WHITE, bg=BG_CARD)
        findings_lbl.pack(anchor="w", pady=(6, 4))

        self.findings_box = tk.Text(
            self.results_frame,
            height=6,
            font=("Consolas", 9),
            bg=BG_INPUT,
            fg="#93c5fd",
            relief=tk.FLAT,
            padx=10,
            pady=8,
            wrap=tk.WORD
        )
        self.findings_box.pack(fill=tk.BOTH, expand=True)

    def load_preset(self, text):
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert(tk.END, text)
        self.run_scan()

    def clear_input(self):
        self.text_input.delete("1.0", tk.END)
        self.findings_box.delete("1.0", tk.END)
        self.risk_badge.config(text="READY TO SCAN", fg=CYAN, bg="#0f172a")
        self.score_label.config(text="Threat Index: 0%")
        self.progress["value"] = 0
        self.advice_label.config(text="Paste a message above and click 'Scan Message' to diagnose.")

    def run_scan(self):
        content = self.text_input.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Empty Message", "Please paste or type a message before scanning.")
            return

        result = analyze_message(content)
        risk = result.get("risk_level", "Low")
        score = result.get("risk_score", 0)
        advice = result.get("advice", "")
        findings = result.get("findings", [])

        # Update Score and Progress Bar
        self.score_label.config(text=f"Threat Index: {score}%")
        self.progress["value"] = score

        # Update Badge
        if risk == "High":
            self.risk_badge.config(text="CRITICAL RISK", fg=RED, bg="#450a0a")
        elif risk == "Medium":
            self.risk_badge.config(text="ELEVATED RISK", fg=AMBER, bg="#451a03")
        else:
            self.risk_badge.config(text="VERIFIED CLEAN", fg=GREEN, bg="#064e3b")

        # Update Advice
        self.advice_label.config(text=advice)

        # Update Findings Text
        self.findings_box.delete("1.0", tk.END)
        if not findings:
            self.findings_box.insert(tk.END, "✓ No scam indicators detected. Message appears clean.\n")
        else:
            for i, f in enumerate(findings, 1):
                sev = f.get("severity", "Warning")
                cat = f.get("category", "General")
                reason = f.get("reason", "")
                snippet = f.get("matched_text", "")
                self.findings_box.insert(tk.END, f"[{i}] {cat.upper()} ({sev})\n")
                self.findings_box.insert(tk.END, f"    Reason: {reason}\n")
                if snippet:
                    self.findings_box.insert(tk.END, f"    Trigger: \"{snippet}\"\n")
                self.findings_box.insert(tk.END, "\n")


if __name__ == "__main__":
    app = ScamShieldDesktopApp()
    app.mainloop()
