# =============================================================================
# GUI "BANQUE ABC CUSTOMER CHURN DETECTOR"
# =============================================================================

# 1. INSTALL TOOLS - auto run
!pip install -q gradio pandas matplotlib

import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import gradio as gr

# 2. DEMO DATABASE: 20 sample emails Banque ABC.
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

# 3. AI BRAIN: classify churn reason
MOTIFS = {
  "High Fees": ["fee", "fees", "charged", "charge", "maintenance", "inactivity", "debit", "robbery"],
  "Poor Service": ["queue", "line", "wait", "waiting", "agent", "rude", "respect", "staff", "paperwork", "branch", "counter"],
  "App/System Failure": ["app", "application", "system", "crash", "bug", "doesn't work", "won't open", "mobile banking", "transfer", "down"],
  "Lack of Transparency": ["don't explain", "don't know", "don't understand", "transparency", "disappearing"]
}

def classify_email(texte):
  texte = texte.lower()
  for motif, mots_cles in MOTIFS.items():
    if any(mot in texte for mot in mots_cles):
      return motif
  return "Other"

# 4. MAIN FUNCTION: triggered by button
def analyze_churn_abc(texte_emails):
  # If user pastes emails, use them. Else use demo
  if texte_emails.strip():
    emails = [ligne.strip() for ligne in texte_emails.split('\n') if ligne.strip()]
  else:
    emails = EMAILS_ABC_DEMO

  # Analysis
  resultats = [classify_email(email) for email in emails]
  contagem = Counter(resultats)
  total = len(emails)

  # Create chart
  fig, ax = plt.subplots(figsize=(6,6))
  ax.pie(contagem.values(), labels=contagem.keys(), autopct='%1.0f%%', startangle=90)
  ax.set_title(f'Why {total} customers are leaving Banque ABC')

  # Create text report
  top1 = contagem.most_common(1)[0]
  relatorio = f"""
=== BANQUE ABC CUSTOMER CHURN REPORT ===
Total emails analyzed: {total}

TOP 3 REASONS FOR CHURN:
"""
  for i, (motif, qtd) in enumerate(contagem.most_common(3), 1):
    percent = (qtd/total)*100
    relatorio += f"{i}. {motif}: {qtd} customers = {percent:.0f}%\n"

  relatorio += f"\nURGENT ACTION FOR BANQUE ABC:\n"
  if top1[0] == "High Fees":
    relatorio += "-> Review fee structure + better communication in branches.\n"
  elif top1[0] == "Poor Service":
    relatorio += "-> Train counter staff + reduce wait times in branches.\n"
  elif top1[0] == "App/System Failure":
    relatorio += "-> Fix iPhone bugs + transfer errors. IT Priority.\n"

  clients_saved = int(total * 0.02 * 30) # 2% saved over 30 days
  revenue = clients_saved * 40 # Assumption: $40 margin per customer
  relatorio += f"\nROI: Saving just 2% of churn = +${revenue:,}/month for Banque ABC."
  relatorio += f"\nSolution Cost: $1,200/month. Free 14-day pilot."

  return fig, relatorio

# 5. CREATE GUI 1-BUTTON
demo = gr.Interface(
  fn=analyze_churn_abc,
  inputs=gr.Textbox(
    label="Paste Banque ABC emails here (1 per line) or leave blank to use 20 demo emails",
    lines=8,
    placeholder="Paste emails like 'I want to close my account'..."
  ),
  outputs=[
    gr.Plot(label="Chart for Banque ABC Management"),
    gr.Textbox(label="Report + Recommendation + ROI", lines=15)
  ],
  title="Banque ABC - Customer Churn Detector",
  description="Click 'Analyze'. AI analyzes in 2s and tells why customers leave + how much the bank loses. 100% tablet ready.",
  submit_btn="Analyze Now",
  clear_btn="Clear"
)

# 6. LAUNCH INTERFACE
demo.launch(share=True, debug=False)
