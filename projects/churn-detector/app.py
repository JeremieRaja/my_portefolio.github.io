# =============================================================================
# BANQUE ABC - CUSTOMER CHURN DETECTOR
# An AI-powered tool to analyze customer churn reasons from emails.
# Built with Gradio, Pandas, and Matplotlib
# =============================================================================

# 1. INSTALL DEPENDENCIES
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import gradio as gr

# 2. DEMO DATABASE: 20 sample customer emails from Banque ABC
EMAILS_ABC_DEMO = [
    "Hello, I want to close my Banque ABC account. The fees are too high every month.",
    "Terrible service at the downtown branch. 3h in line for nothing. I want to close.",
    "Banque ABC app doesn't work on my phone since the update. I'm switching to the competition.",
    "They charged me $50 and I don't know why. Ghost fees. Please close the account.",
    "Too much waiting at the counter. I waste the whole morning. I'm closing.",
    "They charge account maintenance and inactivity fees. It's robbery. I want to leave Banque ABC.",
    "The agent was very rude to me. Lack of respect. Close my account.",
    "The app crashes every time I try to make a transfer. I'm done.",
    "Huge queue every day at the branch. I don't have time for this.",
    "They don't explain the fees. I just see money disappearing. I want to close.",
    "System is always down when I need it. I'm changing banks.",
    "ATM withdrawal fees at other banks are absurd. Closing account.",
    "Staff don't solve the problem. They pass me from one to another. Enough.",
    "Mobile banking always has bugs. Can't check balance. I give up.",
    "Wrong charge of $20. No one can explain. Close it.",
    "40min wait on customer service line. Horrible service. I'm leaving.",
    "Every time I go to the branch I lose a work day. Not worth it anymore.",
    "Charges I don't understand on statement. Lack of transparency. Goodbye Banque ABC.",
    "App won't open on iPhone. I complained 3 times already. Closing.",
    "Too much paperwork for a simple request. Other banks are better."
]

# 3. AI CLASSIFICATION ENGINE: Keyword-based churn reason classifier
# In a production version, this would be replaced by an LLM or ML model
CHURN_REASONS = {
    "High Fees": ["fee", "fees", "charged", "charge", "maintenance", "inactivity", "debit", "robbery"],
    "Poor Service": ["queue", "line", "wait", "waiting", "agent", "rude", "respect", "staff", "paperwork", "branch", "counter"],
    "App/System Failure": ["app", "application", "system", "crash", "bug", "doesn't work", "won't open", "mobile banking", "transfer", "down"],
    "Lack of Transparency": ["don't explain", "don't know", "don't understand", "transparency", "disappearing"]
}

def classify_email(email_text):
    """
    Classifies a single email into a churn reason category based on keywords.
    Args:
        email_text (str): The customer email content.
    Returns:
        str: The predicted churn reason.
    """
    email_text = email_text.lower()
    for reason, keywords in CHURN_REASONS.items():
        if any(keyword in email_text for keyword in keywords):
            return reason
    return "Other"

# 4. MAIN LOGIC: Process emails and generate insights
def analyze_churn_abc(user_input_emails):
    """
    Main function triggered by the Gradio UI.
    Analyzes emails, generates a chart and a business report with ROI.
    """
    # Use user input if provided, otherwise use demo data
    if user_input_emails.strip():
        emails = [line.strip() for line in user_input_emails.split('\n') if line.strip()]
    else:
        emails = EMAILS_ABC_DEMO

    # Run classification on all emails
    results = [classify_email(email) for email in emails]
    reason_counts = Counter(results)
    total_emails = len(emails)

    # Generate Pie Chart for Management
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(reason_counts.values(), labels=reason_counts.keys(), autopct='%1.0f%%', startangle=90)
    ax.set_title(f'Why {total_emails} customers are leaving Banque ABC')
    ax.axis('equal') # Equal aspect ratio ensures pie is drawn as a circle.

    # Generate Text Report with Recommendations and ROI
    top_reason = reason_counts.most_common(1)[0]
    report = f"""
=== BANQUE ABC CUSTOMER CHURN REPORT ===
Total emails analyzed: {total_emails}

TOP 3 REASONS FOR CHURN:
"""
    for i, (reason, count) in enumerate(reason_counts.most_common(3), 1):
        percentage = (count / total_emails) * 100
        report += f"{i}. {reason}: {count} customers = {percentage:.0f}%\n"

    report += f"\nURGENT ACTION FOR BANQUE ABC:\n"
    if top_reason[0] == "High Fees":
        report += "-> Review fee structure + improve communication about fees in branches.\n"
    elif top_reason[0] == "Poor Service":
        report += "-> Train counter staff + implement queue management to reduce wait times.\n"
    elif top_reason[0] == "App/System Failure":
        report += "-> Prioritize fixing iPhone app bugs + transfer errors. IT Department.\n"
    else:
        report += "-> Conduct deeper qualitative analysis on 'Other' category.\n"

    # ROI Calculation: Assumption of saving 2% of churners
    clients_saved = int(total_emails * 0.02 * 30) # 2% saved over 30 days
    monthly_revenue_saved = clients_saved * 40 # Assumption: $40 margin per customer
    report += f"\nPROJECTED ROI:\n"
    report += f"Saving just 2% of churn = +${monthly_revenue_saved:,}/month for Banque ABC.\n"
    report += f"Estimated Solution Cost: $1,200/month. Free 14-day pilot available."

    return fig, report

# 5. GRADIO UI: 1-Click Interface for Business Users
demo = gr.Interface(
    fn=analyze_churn_abc,
    inputs=gr.Textbox(
        label="Paste Customer Emails Here (1 per line)",
        lines=8,
        placeholder="Paste emails like 'I want to close my account because...' or leave blank for demo data"
    ),
    outputs=[
        gr.Plot(label="Churn Reasons Distribution"),
        gr.Textbox(label="AI Report + Recommendations + ROI", lines=15)
    ],
    title="Banque ABC - Customer Churn Detector",
    description="An AI tool to analyze why customers are leaving. Click 'Analyze' to get insights in 2 seconds. Optimized for tablet use.",
    submit_btn="Analyze Now",
    clear_btn="Clear"
)

# 6. LAUNCH THE APP
if __name__ == "__main__":
    demo.launch(share=True, debug=False)
