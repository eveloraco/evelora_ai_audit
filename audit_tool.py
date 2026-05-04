"""
Evelora Co — AI Readiness Audit Tool
Free interactive audit for founders and executives.
Scores your company's AI readiness out of 100.
"""

import streamlit as st
import plotly.graph_objects as go

# ── Brand colors ────────────────────────────────────────────────────────────
GOLD    = "#C5AA6D"
CREAM   = "#F7E7CE"
BLUSH   = "#E7C1B3"
DARK    = "#7C6657"
BLACK   = "#1a1a1a"
BG2     = "#1e1e1e"

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Readiness Audit — Evelora Co",
    page_icon="✦",
    layout="centered",
)

# ── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"], .stApp {
    background-color: #1a1a1a !important;
    color: #F7E7CE !important;
    font-family: 'Lato', sans-serif !important;
}
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="block-container"],
.block-container { background: #1a1a1a !important; }
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
.element-container, .stMarkdown,
div[class*="st-emotion-cache"] { background: transparent !important; }

p, span, li, label, div { color: #F7E7CE !important; font-family: 'Lato', sans-serif !important; }
h1, h2, h3,
h1 *, h2 *, h3 *,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
div[class*="st-emotion-cache"] h1,
div[class*="st-emotion-cache"] h2,
div[class*="st-emotion-cache"] h3 {
    font-family: 'Playfair Display', serif !important;
    color: #C5AA6D !important;
}
#MainMenu, footer, header { visibility: hidden; }
hr { border-color: #2a2a2a !important; }

/* Radio buttons */
.stRadio label { color: #F7E7CE !important; font-size: 0.95rem !important; }
.stRadio > div { gap: 0.4rem; }

/* Slider */
.stSlider label { color: #F7E7CE !important; }
.stSlider [data-testid="stSliderThumb"] { background: #C5AA6D !important; }
.stSlider [data-testid="stSliderTrackFill"] { background: #C5AA6D !important; }

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #C5AA6D, #a08c5b) !important;
    color: #1a1a1a !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.75rem 2.5rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    transition: opacity 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Question cards */
.q-card {
    background: #1e1e1e;
    border: 1px solid #2a2a2a;
    border-left: 3px solid #C5AA6D;
    border-radius: 4px;
    padding: 1.2rem 1.4rem 0.6rem;
    margin-bottom: 1.2rem;
}
.q-number {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7C6657 !important;
    margin-bottom: 0.3rem;
}
.q-text {
    font-size: 1rem;
    color: #F7E7CE !important;
    line-height: 1.5;
    margin-bottom: 0.8rem;
}

/* Score card */
.score-big {
    font-family: 'Playfair Display', serif;
    font-size: 5rem;
    font-weight: 700;
    color: #C5AA6D !important;
    line-height: 1;
    text-align: center;
}
.tier-label {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    color: #F7E7CE !important;
    text-align: center;
    margin-top: 0.3rem;
}
.tier-desc {
    font-size: 0.95rem;
    color: #E7C1B3 !important;
    text-align: center;
    margin-top: 0.5rem;
    line-height: 1.6;
}

/* Rec cards */
.rec-card {
    background: rgba(197,170,109,0.07);
    border: 1px solid rgba(197,170,109,0.2);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.rec-card b { color: #C5AA6D !important; }

/* Section label */
.sec-label {
    font-size: 0.65rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #7C6657 !important;
    margin-bottom: 0.3rem;
}

/* Footer */
.evelora-footer {
    text-align: center;
    padding: 2rem 0 1rem;
    border-top: 1px solid #2a2a2a;
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# SCORING LOGIC
# ══════════════════════════════════════════════════════════════════════════

# Each question maps to a category and has a max score
# answers are 0-indexed option values

CATEGORIES = {
    "current_usage":   {"label": "Current Usage",      "max": 25},
    "leadership":      {"label": "Leadership Adoption", "max": 20},
    "data_infra":      {"label": "Data Infrastructure", "max": 20},
    "strategy":        {"label": "Strategy & Investment","max": 20},
    "execution":       {"label": "Execution History",   "max": 15},
}

TIERS = [
    (0,  20,  "AI Unaware",    "Your organisation has not meaningfully started. The opportunity cost is growing every quarter."),
    (21, 40,  "AI Curious",    "Awareness is there, but execution is missing. Most companies sit here and stay here."),
    (41, 60,  "AI Developing", "You have made real moves. The gap now is system, not intent."),
    (61, 80,  "AI Ready",      "Strong foundation. You are ahead of most. The next step is scaling what works."),
    (81, 100, "AI Leader",     "Genuinely embedded. You are in the top tier of AI-integrated organisations globally."),
]

RECOMMENDATIONS = {
    "current_usage": {
        "low":  ("Start with one team, not the whole company.", "Pick the department with the clearest, most repetitive workflow and deploy one AI tool there. Prove the ROI in 60 days, then expand. Trying to transform everyone at once is why most AI initiatives stall."),
        "high": ("Deepen usage, do not just widen it.", "You have good adoption. Now measure quality — which teams are using AI strategically vs. which ones are just using it to reformat emails? Depth of integration drives real productivity gains."),
    },
    "leadership": {
        "low":  ("The leadership gap is your most urgent problem.", "Data consistently shows that organisations where senior leadership does not personally use AI make worse AI investment decisions. Start with one AI tool for your leadership team this week. Not a workshop — actual daily use."),
        "high": ("Turn leadership usage into leadership advocacy.", "Because your leaders use AI personally, they can credibly champion it internally. Document their use cases and share them with the wider team. Top-down authenticity accelerates adoption faster than any training programme."),
    },
    "data_infra": {
        "low":  ("Clean data is the foundation everything else depends on.", "AI tools are only as useful as the data they work with. Before investing in more AI, invest in data hygiene — structured customer records, consistent formats, centralised storage. This is unsexy but it is the work that makes everything else possible."),
        "high": ("Your data foundation is a competitive asset.", "Most companies underestimate how valuable structured, clean data is. Consider what proprietary data you have that competitors do not — that is where your AI advantage will compound over time."),
    },
    "strategy": {
        "low":  ("You need a written AI strategy, not just an AI opinion.", "An AI strategy does not need to be long. It needs to answer three questions: What problem are we solving with AI? Who owns it? How will we measure success in 90 days? Without a written answer to these three questions, every AI initiative will drift."),
        "high": ("Your strategy is strong. Now build accountability into it.", "Having a strategy is rare. Executing it consistently is rarer. Build a monthly review cadence where you assess AI initiatives against the original goals. What is working, what is stalling, what needs to be cut."),
    },
    "execution": {
        "low":  ("Execution is the gap between knowing and doing.", "Most organisations that score low here have had conversations about AI but have not shipped a single real project. Pick the smallest possible AI initiative — one that can go from idea to result in 30 days — and ship it. Momentum matters more than perfection."),
        "high": ("You have execution credibility. Use it.", "Because you have shipped real AI projects, you have something most organisations lack — internal case studies. Document what worked and what failed. These stories are your most powerful internal advocacy tools and your most credible external positioning."),
    },
}


def get_tier(score):
    for lo, hi, name, desc in TIERS:
        if lo <= score <= hi:
            return name, desc
    return "AI Leader", TIERS[-1][3]


def get_recommendations(category_scores):
    """Return 3 recommendations for the 3 lowest-scoring categories."""
    sorted_cats = sorted(category_scores.items(), key=lambda x: x[1] / CATEGORIES[x[0]]["max"])
    recs = []
    for cat_key, score in sorted_cats[:3]:
        max_score = CATEGORIES[cat_key]["max"]
        threshold = max_score * 0.5
        level = "low" if score <= threshold else "high"
        title, body = RECOMMENDATIONS[cat_key][level]
        recs.append((CATEGORIES[cat_key]["label"], title, body))
    return recs


def make_radar(category_scores, category_maxes):
    """Build a radar chart of the 5 category scores."""
    labels = [CATEGORIES[k]["label"] for k in category_scores]
    values = [round(v / category_maxes[k] * 100) for k, v in category_scores.items()]
    values_closed = values + [values[0]]
    labels_closed = labels + [labels[0]]

    fig = go.Figure()

    # Fill area
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill="toself",
        fillcolor="rgba(197,170,109,0.15)",
        line=dict(color=GOLD, width=2),
        marker=dict(size=7, color=GOLD),
        hovertemplate="%{theta}: %{r}/100<extra></extra>",
    ))

    fig.update_layout(
        polar=dict(
            bgcolor=BG2,
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix="%",
                tickfont=dict(color=DARK, size=9),
                gridcolor="#2a2a2a",
                linecolor="#2a2a2a",
            ),
            angularaxis=dict(
                tickfont=dict(color=CREAM, size=11, family="Lato"),
                gridcolor="#2a2a2a",
                linecolor="#2a2a2a",
            ),
        ),
        paper_bgcolor=BLACK,
        height=360,
        margin=dict(l=50, r=50, t=30, b=30),
        showlegend=False,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════
# APP
# ══════════════════════════════════════════════════════════════════════════

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:2.5rem 0 1rem; text-align:center;">
    <p style="font-size:0.65rem; letter-spacing:0.22em; text-transform:uppercase;
              color:#7C6657; margin-bottom:0.5rem;">
        Evelora Co &nbsp;✦&nbsp; Free Tool
    </p>
    <h1 style="font-family:'Playfair Display',serif; font-size:2.4rem;
               color:#C5AA6D !important; line-height:1.15; margin-bottom:0.6rem;">
        AI Readiness Audit
    </h1>
    <p style="font-size:1rem; color:#E7C1B3; max-width:520px;
              margin:0 auto; line-height:1.7;">
        10 questions. 3 minutes. A personalised score that tells you exactly
        where your organisation stands on AI — and what to do next.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Context questions (not scored — used for personalisation) ─────────────
st.markdown('<p class="sec-label">About your organisation</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    company_name = st.text_input("Company / Organisation name (optional)", placeholder="e.g. Acme Inc")
with col2:
    role = st.selectbox("Your role", [
        "Founder / CEO", "C-Suite Executive", "Senior Manager",
        "Manager", "Individual Contributor", "Other"
    ])

team_size = st.selectbox("Team size", [
    "Just me (solo founder)", "2-10", "11-50", "51-200", "201-1000", "1000+"
])

industry = st.selectbox("Industry", [
    "Technology / Software", "Financial Services", "Healthcare",
    "Professional Services", "Retail & Consumer", "Manufacturing",
    "Media & Entertainment", "Education", "Legal Services",
    "Government & Public Sector", "Agriculture", "Other"
])

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════
# THE 10 QUESTIONS
# ══════════════════════════════════════════════════════════════════════════

st.markdown('<p class="sec-label">The Audit — 10 Questions</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# We store all answers in a dict then compute scores at the end

# ── CATEGORY 1: CURRENT USAGE (25 pts) ─────────────────────────────────────

st.markdown("""
<div class="q-card">
    <p class="q-number">Question 01 &nbsp;·&nbsp; Current Usage</p>
    <p class="q-text">What percentage of your team actively uses AI tools in their daily work?</p>
</div>
""", unsafe_allow_html=True)
q1 = st.radio("", [
    "Less than 10% — most people are not using AI at all",
    "10-30% — a handful of early adopters",
    "31-60% — roughly half the team",
    "61-80% — most of the team uses AI regularly",
    "More than 80% — it is embedded in how we work",
], key="q1", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="q-card">
    <p class="q-number">Question 02 &nbsp;·&nbsp; Current Usage</p>
    <p class="q-text">How would you describe the quality of AI use in your organisation?</p>
</div>
""", unsafe_allow_html=True)
q2 = st.radio("", [
    "We experiment occasionally but nothing is consistent",
    "Some teams have useful workflows but it is not systematic",
    "We have a few strong AI workflows that run reliably",
    "AI is embedded in our core processes and saves measurable time",
], key="q2", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# ── CATEGORY 2: LEADERSHIP ADOPTION (20 pts) ───────────────────────────────

st.markdown("""
<div class="q-card">
    <p class="q-number">Question 03 &nbsp;·&nbsp; Leadership Adoption</p>
    <p class="q-text">Does your senior leadership or founding team personally use AI tools in their own daily work?</p>
</div>
""", unsafe_allow_html=True)
q3 = st.radio("", [
    "No — leadership discusses AI but does not use it personally",
    "Occasionally — some leaders use it sporadically",
    "Yes — most senior leaders have AI in their daily workflow",
    "Yes — and leadership actively advocates for it internally",
], key="q3", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="q-card">
    <p class="q-number">Question 04 &nbsp;·&nbsp; Leadership Adoption</p>
    <p class="q-text">Have your leadership or founders made a concrete investment decision specifically for AI in the last 12 months?</p>
</div>
""", unsafe_allow_html=True)
q4 = st.radio("", [
    "No — AI has not been a budget priority",
    "We have subscribed to a few AI tools informally",
    "Yes — we have made a deliberate budget allocation for AI",
    "Yes — and we have a dedicated person or team responsible for AI",
], key="q4", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# ── CATEGORY 3: DATA INFRASTRUCTURE (20 pts) ───────────────────────────────

st.markdown("""
<div class="q-card">
    <p class="q-number">Question 05 &nbsp;·&nbsp; Data Infrastructure</p>
    <p class="q-text">How would you describe the state of your company's data?</p>
</div>
""", unsafe_allow_html=True)
q5 = st.radio("", [
    "Scattered — data lives in spreadsheets, emails, and people's heads",
    "Partially organised — some structure but inconsistent",
    "Reasonably clean — we have systems but they could be better",
    "Well structured — data is centralised, clean, and accessible",
], key="q5", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="q-card">
    <p class="q-number">Question 06 &nbsp;·&nbsp; Data Infrastructure</p>
    <p class="q-text">Do you regularly analyse data to make business decisions?</p>
</div>
""", unsafe_allow_html=True)
q6 = st.radio("", [
    "Rarely — decisions are mostly made on instinct or experience",
    "Sometimes — we look at data but not systematically",
    "Often — data informs most major decisions",
    "Always — we have dashboards and metrics reviewed regularly",
], key="q6", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# ── CATEGORY 4: STRATEGY & INVESTMENT (20 pts) ─────────────────────────────

st.markdown("""
<div class="q-card">
    <p class="q-number">Question 07 &nbsp;·&nbsp; Strategy & Investment</p>
    <p class="q-text">Does your organisation have a written AI strategy or roadmap?</p>
</div>
""", unsafe_allow_html=True)
q7 = st.radio("", [
    "No — we think about AI informally",
    "We have informal discussions but nothing written",
    "We have a basic plan but it is not formalised",
    "Yes — we have a clear written AI strategy with goals and timelines",
], key="q7", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="q-card">
    <p class="q-number">Question 08 &nbsp;·&nbsp; Strategy & Investment</p>
    <p class="q-text">How does your organisation view AI relative to competitors?</p>
</div>
""", unsafe_allow_html=True)
q8 = st.radio("", [
    "We have not thought about it in competitive terms",
    "We are aware competitors are using AI but are not worried yet",
    "We feel urgency to close a gap with competitors on AI",
    "We believe AI is a core part of our competitive advantage",
], key="q8", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# ── CATEGORY 5: EXECUTION HISTORY (15 pts) ─────────────────────────────────

st.markdown("""
<div class="q-card">
    <p class="q-number">Question 09 &nbsp;·&nbsp; Execution History</p>
    <p class="q-text">Has your organisation successfully shipped any AI-powered project or automation in the last 12 months?</p>
</div>
""", unsafe_allow_html=True)
q9 = st.radio("", [
    "No — nothing has been shipped yet",
    "We started projects but none completed successfully",
    "Yes — one or two small automations or tools",
    "Yes — multiple projects with measurable results",
], key="q9", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="q-card">
    <p class="q-number">Question 10 &nbsp;·&nbsp; Execution History</p>
    <p class="q-text">How does your team respond when an AI project fails or does not deliver results?</p>
</div>
""", unsafe_allow_html=True)
q10 = st.radio("", [
    "We have not had a failure yet because nothing has been tried",
    "Failures have made leadership more cautious about AI",
    "We treat failures as learning and try again differently",
    "We have a systematic review process for AI initiatives",
], key="q10", label_visibility="collapsed")

st.markdown("<br><br>", unsafe_allow_html=True)

# ── CALCULATE BUTTON ─────────────────────────────────────────────────────────
calculate = st.button("Calculate My AI Readiness Score  ✦")

# ══════════════════════════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════════════════════════

if calculate:

    # ── Score each question ───────────────────────────────────────────────
    # Radio options are 0-indexed. Map to score contribution.

    # Q1 — current usage: 5 options → 0,4,8,12,16 pts (out of ~16 of the 25)
    q1_score = [0, 4, 8, 12, 16][[
        "Less than 10% — most people are not using AI at all",
        "10-30% — a handful of early adopters",
        "31-60% — roughly half the team",
        "61-80% — most of the team uses AI regularly",
        "More than 80% — it is embedded in how we work",
    ].index(q1)]

    # Q2 — usage quality: 4 options → 0,3,6,9 pts (remaining 9 of 25)
    q2_score = [0, 3, 6, 9][[
        "We experiment occasionally but nothing is consistent",
        "Some teams have useful workflows but it is not systematic",
        "We have a few strong AI workflows that run reliably",
        "AI is embedded in our core processes and saves measurable time",
    ].index(q2)]

    current_usage_score = q1_score + q2_score  # max 25

    # Q3 — leadership personal use: 4 options → 0,3,7,10 pts (out of 10)
    q3_score = [0, 3, 7, 10][[
        "No — leadership discusses AI but does not use it personally",
        "Occasionally — some leaders use it sporadically",
        "Yes — most senior leaders have AI in their daily workflow",
        "Yes — and leadership actively advocates for it internally",
    ].index(q3)]

    # Q4 — investment decision: 4 options → 0,3,7,10 pts (remaining 10)
    q4_score = [0, 3, 7, 10][[
        "No — AI has not been a budget priority",
        "We have subscribed to a few AI tools informally",
        "Yes — we have made a deliberate budget allocation for AI",
        "Yes — and we have a dedicated person or team responsible for AI",
    ].index(q4)]

    leadership_score = q3_score + q4_score  # max 20

    # Q5 — data state: 4 options → 0,3,7,10 pts (out of 10)
    q5_score = [0, 3, 7, 10][[
        "Scattered — data lives in spreadsheets, emails, and people's heads",
        "Partially organised — some structure but inconsistent",
        "Reasonably clean — we have systems but they could be better",
        "Well structured — data is centralised, clean, and accessible",
    ].index(q5)]

    # Q6 — data-driven decisions: 4 options → 0,3,7,10 pts
    q6_score = [0, 3, 7, 10][[
        "Rarely — decisions are mostly made on instinct or experience",
        "Sometimes — we look at data but not systematically",
        "Often — data informs most major decisions",
        "Always — we have dashboards and metrics reviewed regularly",
    ].index(q6)]

    data_infra_score = q5_score + q6_score  # max 20

    # Q7 — written strategy: 4 options → 0,3,7,10 pts
    q7_score = [0, 3, 7, 10][[
        "No — we think about AI informally",
        "We have informal discussions but nothing written",
        "We have a basic plan but it is not formalised",
        "Yes — we have a clear written AI strategy with goals and timelines",
    ].index(q7)]

    # Q8 — competitive view: 4 options → 0,3,7,10 pts
    q8_score = [0, 3, 7, 10][[
        "We have not thought about it in competitive terms",
        "We are aware competitors are using AI but are not worried yet",
        "We feel urgency to close a gap with competitors on AI",
        "We believe AI is a core part of our competitive advantage",
    ].index(q8)]

    strategy_score = q7_score + q8_score  # max 20

    # Q9 — shipped projects: 4 options → 0,2,7,10 pts (out of 10)
    q9_score = [0, 2, 7, 10][[
        "No — nothing has been shipped yet",
        "We started projects but none completed successfully",
        "Yes — one or two small automations or tools",
        "Yes — multiple projects with measurable results",
    ].index(q9)]

    # Q10 — failure response: 4 options → 0,0,3,5 pts (remaining 5)
    q10_score = [0, 0, 3, 5][[
        "We have not had a failure yet because nothing has been tried",
        "Failures have made leadership more cautious about AI",
        "We treat failures as learning and try again differently",
        "We have a systematic review process for AI initiatives",
    ].index(q10)]

    execution_score = q9_score + q10_score  # max 15

    # ── Total ─────────────────────────────────────────────────────────────
    total = current_usage_score + leadership_score + data_infra_score + strategy_score + execution_score
    tier_name, tier_desc = get_tier(total)

    category_scores = {
        "current_usage": current_usage_score,
        "leadership":    leadership_score,
        "data_infra":    data_infra_score,
        "strategy":      strategy_score,
        "execution":     execution_score,
    }
    category_maxes = {k: v["max"] for k, v in CATEGORIES.items()}

    # ── Results UI ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="sec-label" style="text-align:center;">Your Results</p>',
                unsafe_allow_html=True)

    # Score and tier
    name_line = f"{company_name}'s" if company_name else "Your"
    st.markdown(f"""
    <div style="padding:2rem 1rem 1rem; text-align:center;">
        <p style="font-size:0.85rem; color:#7C6657; margin-bottom:0.3rem;">
            {name_line} AI Readiness Score
        </p>
        <div class="score-big">{total}</div>
        <p style="font-size:0.75rem; color:#7C6657; margin:0.2rem 0 0.8rem;">out of 100</p>
        <div class="tier-label">{tier_name}</div>
        <p class="tier-desc" style="max-width:480px; margin:0.5rem auto 0;">{tier_desc}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Radar chart
    st.markdown('<p class="sec-label" style="text-align:center;">Score Breakdown by Category</p>',
                unsafe_allow_html=True)
    fig = make_radar(category_scores, category_maxes)
    st.plotly_chart(fig, use_container_width=True)

    # Category breakdown table
    st.markdown("<br>", unsafe_allow_html=True)
    for cat_key, score in category_scores.items():
        max_s   = CATEGORIES[cat_key]["max"]
        label   = CATEGORIES[cat_key]["label"]
        pct     = round(score / max_s * 100)
        bar_col = GOLD if pct >= 60 else (BLUSH if pct >= 35 else DARK)
        st.markdown(f"""
        <div style="margin-bottom:0.8rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="font-size:0.88rem; color:#F7E7CE;">{label}</span>
                <span style="font-size:0.88rem; color:{bar_col}; font-weight:700;">
                    {score}/{max_s}
                </span>
            </div>
            <div style="background:#2a2a2a; border-radius:2px; height:6px;">
                <div style="background:{bar_col}; border-radius:2px;
                            height:6px; width:{pct}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Recommendations
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p class="sec-label">Your Three Priority Actions</p>',
                unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:0.9rem; color:#E7C1B3; line-height:1.6; margin-bottom:1.2rem;">
        Based on your lowest-scoring areas, these are the three things that will
        move your score the most if you act on them in the next 90 days.
    </p>
    """, unsafe_allow_html=True)

    recs = get_recommendations(category_scores)
    for i, (category, title, body) in enumerate(recs, 1):
        st.markdown(f"""
        <div class="rec-card">
            <p style="font-size:0.65rem; letter-spacing:0.15em; text-transform:uppercase;
                      color:#7C6657; margin-bottom:0.3rem;">Priority {i} &nbsp;·&nbsp; {category}</p>
            <p style="font-size:1rem; color:#C5AA6D; font-family:'Playfair Display',serif;
                      margin-bottom:0.4rem;"><b>{title}</b></p>
            <p style="font-size:0.9rem; color:#F7E7CE; line-height:1.65; margin:0;">{body}</p>
        </div>
        """, unsafe_allow_html=True)

    # CTA
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"""
    <div style="background:rgba(197,170,109,0.07); border:1px solid rgba(197,170,109,0.2);
                border-radius:4px; padding:1.5rem 1.8rem; text-align:center;">
        <p style="font-family:'Playfair Display',serif; color:#C5AA6D;
                  font-size:1.1rem; margin-bottom:0.5rem;">
            Want a deeper analysis for {company_name if company_name else 'your organisation'}?
        </p>
        <p style="font-size:0.9rem; color:#E7C1B3; line-height:1.6; margin-bottom:1rem;">
            Evelora Co works with founders and executives to build bespoke AI solutions,
            automation systems, and data intelligence tools. If your score revealed gaps
            you want to close, let's talk.
        </p>
        <a href="https://linkedin.com/company/evelora-co"
           style="color:#C5AA6D; font-weight:700; letter-spacing:0.08em;
                  text-transform:uppercase; font-size:0.85rem;">
            Connect on LinkedIn &nbsp;→
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Share nudge
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <p style="text-align:center; font-size:0.88rem; color:#7C6657; line-height:1.6;">
        Share your score on LinkedIn and tag <b style="color:#C5AA6D;">Evelora Co</b>.<br>
        We will comment with one additional insight specific to your industry.
    </p>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="evelora-footer">
    <p style="font-family:'Playfair Display',serif; color:#C5AA6D;
              font-size:0.95rem; letter-spacing:0.1em; margin-bottom:0.3rem;">
        EVELORA CO
    </p>
    <p style="font-size:0.65rem; color:#7C6657; letter-spacing:0.15em;
              text-transform:uppercase; margin-bottom:0.8rem;">
        Where Elegance Meets Intelligence
    </p>
    <p style="font-size:0.78rem; color:#555;">
        Free tool. No data stored. No login required.<br>
        <a href="https://github.com/eveloraco" style="color:#7C6657;">github.com/eveloraco</a>
        &nbsp;·&nbsp;
        <a href="https://linkedin.com/company/evelora-co" style="color:#7C6657;">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)
