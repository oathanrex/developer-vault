"""
AdSenseReady-AI: Dynamic SVG Badge Generator
--------------------------------------------
Generates crisp, Retina-ready SVG status badges for websites, GitHub READMEs, and portfolios.
"""

def generate_svg_badge(score: float, status_label: str = "Ready") -> str:
    """Creates a Shields-style SVG badge representing AdSense readiness score."""
    int_score = int(score)
    color = "#10b981" if int_score >= 85 and status_label in ["Ready", "Passing", "APPROVED_READY"] else ("#f59e0b" if int_score >= 65 else "#ef4444")
    
    # Shorten long enum verdicts
    clean_label = status_label
    if status_label == "APPROVED_READY":
        clean_label = "Passing"
    elif status_label == "AT_RISK":
        clean_label = "At Risk"
    elif status_label == "REJECTION_GUARANTEED":
        clean_label = "Action Req"

    text_right = f"{int_score}/100 {clean_label}"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="180" height="24" viewBox="0 0 180 24" role="img" aria-label="AdSense Readiness: {int_score}/100">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="a">
    <rect width="180" height="24" rx="4" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#a)">
    <rect width="95" height="24" fill="#1e293b"/>
    <rect x="95" width="85" height="24" fill="{color}"/>
    <rect width="180" height="24" fill="url(#b)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="11" font-weight="600">
    <text x="47.5" y="16" fill="#010101" fill-opacity=".3">AdSense Ready</text>
    <text x="47.5" y="15">AdSense Ready</text>
    <text x="137.5" y="16" fill="#010101" fill-opacity=".3">{text_right}</text>
    <text x="137.5" y="15">{text_right}</text>
  </g>
</svg>"""
    return svg
