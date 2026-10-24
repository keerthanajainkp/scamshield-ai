/**
 * ScamShield AI - Interactive Frontend Controller
 * ===============================================
 * Features:
 * - Animated SVG circular threat gauge (0% - 100%)
 * - Category pillar breakdown (Links, Urgency, Prizes, Credentials)
 * - Preset scenarios loader (Bank, Lottery, PayPal, Crypto, Safe)
 * - One-click clipboard paste & report copy
 * - Live character & word counters
 * - Offline-resilient fallback detection
 */

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const messageInput = document.getElementById("message-input");
    const charCounter = document.getElementById("char-counter");
    const wordCounter = document.getElementById("word-counter");
    const clearBtn = document.getElementById("clear-btn");
    const pasteBtn = document.getElementById("paste-btn");
    const analyzerForm = document.getElementById("analyzer-form");
    const analyzeBtn = document.getElementById("analyze-btn");
    const analyzeBtnText = document.getElementById("analyze-btn-text");
    const btnSpinner = document.getElementById("btn-spinner");

    // Results Dashboard Elements
    const resultsPanel = document.getElementById("results-panel");
    const riskBadge = document.getElementById("risk-badge");
    const scoreText = document.getElementById("score-text");
    const scoreRingBar = document.getElementById("score-ring-bar");
    const threatLevelDesc = document.getElementById("threat-level-desc");
    const adviceBox = document.getElementById("advice-box");
    const adviceCardBox = document.getElementById("advice-card-box");
    const findingsList = document.getElementById("findings-list");
    const findingsCount = document.getElementById("findings-count");
    const actionChecklist = document.getElementById("action-checklist");
    const copyReportBtn = document.getElementById("copy-report-btn");
    const copyBtnLabel = document.getElementById("copy-btn-label");

    // Pillar Elements
    const pillarBars = {
        links: document.getElementById("bar-links"),
        urgency: document.getElementById("bar-urgency"),
        prizes: document.getElementById("bar-prizes"),
        credentials: document.getElementById("bar-credentials")
    };
    const pillarScores = {
        links: document.getElementById("score-links"),
        urgency: document.getElementById("score-urgency"),
        prizes: document.getElementById("score-prizes"),
        credentials: document.getElementById("score-credentials")
    };

    const presetButtons = document.querySelectorAll(".preset-pill");

    // Circumference of the SVG gauge circle (radius = 68)
    const RING_CIRCUMFERENCE = 2 * Math.PI * 68; // ≈ 427.25

    // Current analysis state cache
    let currentAnalysisResult = null;

    // Realistic Test Presets
    const PRESETS = {
        bank: "URGENT from Chase Bank: We detected an unauthorized transaction on your card. Your account will be suspended within 24 hours unless you verify immediately. Visit http://192.168.1.105/login and enter your password and card details.",
        prize: "Congratulations! You have won a $1,000,000 cash prize in our national lottery! Claim your prize now at http://bit.ly/winner-jackpot-2026. Send your bank account and SSN to release funds.",
        urgent: "FINAL NOTICE: Unusual activity detected on your PayPal account. Dear Customer, immediate action required. Confirm your PIN and one-time code at https://update-account-security.xyz within 12 hours.",
        crypto: "Exclusive Elon Musk Bitcoin Giveaway! Double your deposit guaranteed return within 24 hours. Connect your online banking credentials at http://bit.ly/crypto-bonus-vip",
        safe: "Hi Alex, your Amazon package with tracking number #408-2910 has been delivered to your front porch. Have a wonderful weekend!"
    };

    // Live Metrics Update
    function updateMetrics() {
        const text = messageInput.value;
        const charLength = text.length;
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;

        charCounter.textContent = `${charLength} char${charLength === 1 ? "" : "s"}`;
        wordCounter.textContent = `${words} word${words === 1 ? "" : "s"}`;
    }

    messageInput.addEventListener("input", updateMetrics);

    // Preset Buttons Click
    presetButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            const key = btn.getAttribute("data-preset");
            if (PRESETS[key]) {
                messageInput.value = PRESETS[key];
                updateMetrics();
                triggerAnalysis();
            }
        });
    });

    // Paste from Clipboard Button
    pasteBtn.addEventListener("click", async () => {
        try {
            if (navigator.clipboard && navigator.clipboard.readText) {
                const clipText = await navigator.clipboard.readText();
                if (clipText) {
                    messageInput.value = clipText;
                    updateMetrics();
                    messageInput.focus();
                } else {
                    alert("Clipboard is empty.");
                }
            } else {
                alert("Please press CTRL+V inside the text area to paste.");
            }
        } catch (err) {
            alert("Clipboard access was blocked by your browser. Please paste using CTRL+V.");
        }
    });

    // Clear Button
    clearBtn.addEventListener("click", () => {
        messageInput.value = "";
        updateMetrics();
        resultsPanel.style.display = "none";
        currentAnalysisResult = null;
        messageInput.focus();
    });

    // Form Submit
    analyzerForm.addEventListener("submit", (e) => {
        e.preventDefault();
        triggerAnalysis();
    });

    // Trigger Analysis Request
    async function triggerAnalysis() {
        const text = messageInput.value.trim();
        if (!text) {
            alert("Please paste or type a message before scanning.");
            messageInput.focus();
            return;
        }

        setLoading(true);

        try {
            const response = await fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });

            if (!response.ok) {
                throw new Error(`Server returned HTTP ${response.status}`);
            }

            const data = await response.json();
            currentAnalysisResult = data;
            renderResults(data);
        } catch (error) {
            console.warn("Backend API unavailable, using offline heuristic engine:", error);
            const fallbackData = runOfflineHeuristic(text);
            currentAnalysisResult = fallbackData;
            renderResults(fallbackData);
        } finally {
            setLoading(false);
        }
    }

    function setLoading(isLoading) {
        if (isLoading) {
            analyzeBtn.disabled = true;
            btnSpinner.style.display = "inline-block";
            analyzeBtnText.textContent = "Scanning...";
        } else {
            analyzeBtn.disabled = false;
            btnSpinner.style.display = "none";
            analyzeBtnText.textContent = "Scan Message";
        }
    }

    // Render Full Results Dashboard
    function renderResults(data) {
        resultsPanel.style.display = "flex";

        const riskLevel = data.risk_level || "Low";
        const score = data.risk_score || 0;
        const findings = data.findings || [];
        const categoryScores = data.category_scores || { links: 0, urgency: 0, prizes: 0, credentials: 0 };
        const actionItems = data.action_items || [];

        // 1. Update Verdict Badge & Header
        riskBadge.className = "risk-badge";
        scoreRingBar.className = "ring-bar";

        if (riskLevel === "High") {
            riskBadge.textContent = "CRITICAL RISK";
            riskBadge.classList.add("risk-high");
            scoreRingBar.classList.add("ring-high");
            threatLevelDesc.textContent = "Multiple severe fraud heuristics triggered";
        } else if (riskLevel === "Medium") {
            riskBadge.textContent = "ELEVATED RISK";
            riskBadge.classList.add("risk-medium");
            scoreRingBar.classList.add("ring-medium");
            threatLevelDesc.textContent = "Suspicious patterns detected; verify sender";
        } else {
            riskBadge.textContent = "VERIFIED CLEAN";
            riskBadge.classList.add("risk-low");
            scoreRingBar.classList.add("ring-low");
            threatLevelDesc.textContent = "No recognized phishing patterns identified";
        }

        // 2. Animate Circular Score Ring & Counter
        scoreText.textContent = `${score}%`;
        const offset = RING_CIRCUMFERENCE - (score / 100) * RING_CIRCUMFERENCE;
        scoreRingBar.style.strokeDashoffset = offset;

        // 3. Update Category Pillar Bars
        const updatePillar = (key) => {
            const val = categoryScores[key] || 0;
            if (pillarScores[key]) pillarScores[key].textContent = `${val}%`;
            if (pillarBars[key]) {
                pillarBars[key].style.width = `${val}%`;
                pillarBars[key].className = "pillar-fill";
                if (val >= 45) {
                    pillarBars[key].classList.add("fill-high");
                } else if (val >= 20) {
                    pillarBars[key].classList.add("fill-medium");
                } else {
                    pillarBars[key].classList.add("fill-low");
                }
            }
        };
        updatePillar("links");
        updatePillar("urgency");
        updatePillar("prizes");
        updatePillar("credentials");

        // 4. Update Security Recommendation Advice
        adviceBox.textContent = data.advice || "No specific advice available.";

        // 5. Update Detected Indicators List
        findingsCount.textContent = findings.length;
        findingsList.innerHTML = "";

        if (findings.length === 0) {
            findingsList.innerHTML = `
                <div class="clean-message-alert">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                    <div>
                        <strong>Clean Assessment:</strong> No known phishing patterns, deceptive links, or social engineering lures were detected in this message.
                    </div>
                </div>
            `;
        } else {
            findings.forEach((f) => {
                const card = document.createElement("div");
                card.className = "finding-card";

                const sevClass = f.severity === "Critical" ? "sev-critical" : (f.severity === "High" ? "sev-high" : "sev-medium");
                const matchedHtml = f.matched_text ? `
                    <div class="finding-match-snippet">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="4 7 4 4 20 4 20 7"></polyline>
                            <line x1="9" y1="20" x2="15" y2="20"></line>
                            <line x1="12" y1="4" x2="12" y2="20"></line>
                        </svg>
                        Matched: "${escapeHtml(f.matched_text)}"
                    </div>
                ` : "";

                card.innerHTML = `
                    <div class="finding-top-row">
                        <span class="finding-category-pill">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="12" y1="8" x2="12" y2="12"></line>
                                <line x1="12" y1="16" x2="12.01" y2="16"></line>
                            </svg>
                            ${escapeHtml(f.category)}
                        </span>
                        <span class="finding-severity-badge ${sevClass}">${escapeHtml(f.severity || 'High')}</span>
                    </div>
                    <div class="finding-reason-text">${escapeHtml(f.reason)}</div>
                    ${matchedHtml}
                `;
                findingsList.appendChild(card);
            });
        }

        // 6. Update Immediate Action Checklist
        actionChecklist.innerHTML = "";
        actionItems.forEach((item) => {
            const li = document.createElement("li");
            li.className = "checklist-item";
            li.innerHTML = `
                <span class="check-bullet"></span>
                <span>${escapeHtml(item)}</span>
            `;
            actionChecklist.appendChild(li);
        });

        // Smooth Scroll to Results
        resultsPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    // Copy Full Report to Clipboard
    copyReportBtn.addEventListener("click", () => {
        if (!currentAnalysisResult) return;

        const r = currentAnalysisResult;
        let reportText = `🛡️ SCAMSHIELD AI THREAT REPORT\n`;
        reportText += `--------------------------------------\n`;
        reportText += `Risk Verdict : ${r.risk_level.toUpperCase()} RISK (${r.risk_score}% Threat Index)\n`;
        reportText += `Advice       : ${r.advice}\n\n`;
        reportText += `FLAGGED INDICATORS (${(r.findings || []).length}):\n`;
        (r.findings || []).forEach((f, idx) => {
            reportText += `${idx + 1}. [${f.category}] ${f.reason}`;
            if (f.matched_text) reportText += ` (Trigger: "${f.matched_text}")`;
            reportText += `\n`;
        });
        reportText += `\nRECOMMENDED ACTIONS:\n`;
        (r.action_items || []).forEach((act) => {
            reportText += `- ${act}\n`;
        });
        reportText += `--------------------------------------\n`;
        reportText += `Generated locally by ScamShield AI (Educational Estimate)\n`;

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(reportText).then(() => {
                copyBtnLabel.textContent = "Copied!";
                setTimeout(() => { copyBtnLabel.textContent = "Copy Report"; }, 2000);
            }).catch(() => {
                alert("Failed to copy report to clipboard.");
            });
        } else {
            alert("Clipboard write not supported by browser.");
        }
    });

    // Helper: Escape HTML
    function escapeHtml(str) {
        if (!str) return "";
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Offline Heuristic Engine Fallback
    function runOfflineHeuristic(text) {
        const findings = [];
        const matchedSnippets = [];
        let score = 0;
        const categoryScores = { links: 0, urgency: 0, prizes: 0, credentials: 0 };

        const rules = [
            { reg: /\b(bit\.ly|tinyurl\.com|t\.co|goo\.gl|is\.gd|cutt\.ly|ow\.ly|rb\.gy)\b/i, cat: "Suspicious Links", key: "links", reason: "Uses a shortened URL (hiding true destination)", pts: 25, sev: "High" },
            { reg: /https?:\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/i, cat: "Suspicious Links", key: "links", reason: "Direct numeric IP address link instead of domain name", pts: 25, sev: "Critical" },
            { reg: /https?:\/\/[^\s]+\.(xyz|top|club|work|buzz|icu|live|click|tk|ml|ga|cf|gq)\b/i, cat: "Suspicious Links", key: "links", reason: "High-risk or suspicious domain extension (.xyz, .top)", pts: 25, sev: "High" },
            { reg: /\b(urgent|urgently|act now|immediate action|within 24 hours|within 12 hours|last chance|final notice)\b/i, cat: "Urgent Pressure", key: "urgency", reason: "High-pressure urgency to force quick compliance", pts: 20, sev: "Medium" },
            { reg: /\b(account suspended|account blocked|unauthorized transaction|security breach)\b/i, cat: "Urgent Pressure", key: "urgency", reason: "Threatens negative consequence like account block", pts: 25, sev: "High" },
            { reg: /\b(you have won|winner|won a lottery|cash prize|free gift|claim your prize)\b/i, cat: "Prize & Bait", key: "prizes", reason: "Claims unearned prize or lottery jackpot", pts: 25, sev: "High" },
            { reg: /\b(enter your password|send password|confirm your pin|reset your pin|share otp|one-time code)\b/i, cat: "Credential Theft", key: "credentials", reason: "Asks for your password, PIN, or OTP passcode", pts: 30, sev: "Critical" },
            { reg: /\b(social security|ssn|credit card number|cvv|bank account|routing number)\b/i, cat: "Credential Theft", key: "credentials", reason: "Demands sensitive identity or banking numbers", pts: 30, sev: "Critical" }
        ];

        rules.forEach((r) => {
            const m = text.match(r.reg);
            if (m) {
                findings.push({
                    category: r.cat,
                    category_key: r.key,
                    reason: r.reason,
                    severity: r.sev,
                    matched_text: m[0]
                });
                matchedSnippets.push(m[0]);
                score += r.pts;
                categoryScores[r.key] += r.pts;
            }
        });

        score = Math.min(score, 100);
        let riskLevel = "Low";
        let advice = "LOW RISK: No recognized scam patterns were flagged. Always remain observant.";
        let actionItems = ["Standard security hygiene applies.", "Never share passwords over text."];

        if (score >= 45) {
            riskLevel = "High";
            advice = "CRITICAL ALERT: Multiple high-confidence fraud indicators detected! Do NOT tap links or provide credentials.";
            actionItems = [
                "Do NOT click any web links or dial numbers mentioned in the message.",
                "Do NOT share one-time passcodes (OTP), passwords, or card digits.",
                "Block the sender's phone number or email address immediately.",
                "Forward SMS to 7726 (SPAM) to alert your carrier."
            ];
        } else if (score >= 20) {
            riskLevel = "Medium";
            advice = "ELEVATED RISK: Warning indicators were identified. Verify the claimed sender independently.";
            actionItems = [
                "Inspect links carefully before clicking.",
                "Contact the institution directly using official channels."
            ];
        }

        return {
            risk_level: riskLevel,
            risk_score: score,
            category_scores: categoryScores,
            findings: findings,
            matched_snippets: matchedSnippets,
            advice: advice,
            action_items: actionItems,
            character_count: text.length
        };
    }

    // PWA Service Worker Registration & Install Prompt
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/sw.js').catch((err) => {
                console.log('ServiceWorker registration skipped:', err);
            });
        });
    }

    let deferredPrompt;
    const installBtn = document.getElementById('install-app-btn');

    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        if (installBtn) {
            installBtn.style.display = 'inline-flex';
            installBtn.addEventListener('click', () => {
                installBtn.style.display = 'none';
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    deferredPrompt = null;
                });
            });
        }
    });
});
