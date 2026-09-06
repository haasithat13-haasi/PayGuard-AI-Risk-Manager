import os
import gradio as gr
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load the transaction dataset
df = pd.read_csv("transactions.csv")

# Features used by the model
features = [
    "amount",
    "account_age_days",
    "transactions_last_24h",
    "device_changes_30d",
    "failed_attempts",
    "international",
    "new_device",
    "transaction_hour"
]

# Prepare training data
X = df[features]
y = df["is_fraud"]

# Train the Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


def assess_transaction(
    amount,
    account_age_days,
    transactions_last_24h,
    device_changes_30d,
    failed_attempts,
    international,
    new_device,
    transaction_hour
):
    # Create input data in the same feature order
    data = pd.DataFrame([{
        "amount": amount,
        "account_age_days": account_age_days,
        "transactions_last_24h": transactions_last_24h,
        "device_changes_30d": device_changes_30d,
        "failed_attempts": failed_attempts,
        "international": international,
        "new_device": new_device,
        "transaction_hour": transaction_hour
    }])

    # Get fraud probability
    probability = model.predict_proba(data)[0][1]

    # Convert probability to risk score
    risk_score = round(probability * 100)

    # Determine risk level
    if risk_score >= 60:
        level = "🔴 HIGH RISK"
        recommendation = "Block or send this transaction for manual review."
    elif risk_score >= 40:
        level = "🟠 MEDIUM RISK"
        recommendation = "Request additional verification before approving."
    else:
        level = "🟢 LOW RISK"
        recommendation = "Transaction appears relatively safe to approve."

    # Generate explanations
    reasons = []

    if amount > 50000:
        reasons.append("Unusually high transaction amount")

    if transactions_last_24h > 8:
        reasons.append("High transaction frequency in the last 24 hours")

    if device_changes_30d > 3:
        reasons.append("Multiple device changes recently")

    if failed_attempts > 2:
        reasons.append("Multiple failed payment attempts")

    if international == 1:
        reasons.append("International transaction")

    if new_device == 1:
        reasons.append("Transaction from a new device")

    if transaction_hour < 5 or transaction_hour > 23:
        reasons.append("Transaction occurred during unusual hours")

    if account_age_days < 30:
        reasons.append("Recently created account")

    if not reasons:
        reasons.append("No major behavioral risk signals detected")

    reason_text = "\n".join(
        [f"• {reason}" for reason in reasons]
    )

    result = f"""
# {level}

### Risk Score: {risk_score}/100

## AI Assessment

{recommendation}

### Risk Signals

{reason_text}

### Model Probability

Estimated probability of fraud: **{probability:.1%}**
"""

    return result


# Create the Gradio interface
with gr.Blocks(title="PayGuard AI Risk Manager") as demo:

    gr.Markdown("""
# 🛡️ PayGuard
## AI-Powered Transaction Risk Manager

Analyze payment transactions using machine learning and identify
potentially fraudulent behavior before approval.
""")

    gr.Markdown("### Enter Transaction Details")

    with gr.Row():

        with gr.Column():

            amount = gr.Number(
                label="Transaction Amount (₹)",
                value=5000,
                minimum=50,
                maximum=100000
            )

            account_age_days = gr.Number(
                label="Account Age (days)",
                value=365,
                minimum=1,
                maximum=2000
            )

            transactions_last_24h = gr.Number(
                label="Transactions in Last 24 Hours",
                value=3,
                minimum=0,
                maximum=30
            )

            device_changes_30d = gr.Number(
                label="Device Changes in Last 30 Days",
                value=1,
                minimum=0,
                maximum=10
            )

        with gr.Column():

            failed_attempts = gr.Number(
                label="Failed Payment Attempts",
                value=0,
                minimum=0,
                maximum=10
            )

            international = gr.Radio(
                choices=[0, 1],
                label="International Transaction?",
                value=0
            )

            new_device = gr.Radio(
                choices=[0, 1],
                label="New Device?",
                value=0
            )

            transaction_hour = gr.Slider(
                minimum=0,
                maximum=23,
                step=1,
                value=14,
                label="Transaction Hour (0–23)"
            )

    analyze_button = gr.Button(
        "🔍 Analyze Transaction",
        variant="primary"
    )

    output = gr.Markdown()

    analyze_button.click(
        fn=assess_transaction,
        inputs=[
            amount,
            account_age_days,
            transactions_last_24h,
            device_changes_30d,
            failed_attempts,
            international,
            new_device,
            transaction_hour
        ],
        outputs=output
    )

    gr.Markdown("""
---
### How PayGuard Works

**Transaction Data → ML Model → Fraud Probability → Risk Score → Actionable Explanation**

The underlying model is a Random Forest classifier trained on simulated
payment-risk data for this prototype.
""")


# Run the app on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )
