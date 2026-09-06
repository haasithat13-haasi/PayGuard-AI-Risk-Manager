# 🛡️ PayGuard — AI Transaction Risk Manager

An AI-powered transaction risk assessment prototype designed to identify potentially fraudulent payment behavior before approval.


## 🚀 Live Demo

Try the live PayGuard application here:

👉 https://payguard-ai-risk-manager.onrender.com

> Note: The demo is hosted temporarily using a Gradio share link and may not always be available.
## 🎯 Problem

Payment fraud can involve multiple behavioral signals such as unusually large transactions, repeated failed payment attempts, rapid transaction activity, device changes, international transactions, and unusual transaction timing.

PayGuard combines these signals to estimate transaction risk and provide an actionable recommendation.

## 💡 Solution

PayGuard uses a Random Forest machine learning classifier trained on simulated payment-risk transaction data.

The system takes transaction details as input and produces:

- Fraud probability
- Risk score from 0–100
- Risk classification
- Key risk signals
- Recommended action

### Risk Levels

🟢 **Low Risk** — Transaction appears relatively safe to approve.

🟠 **Medium Risk** — Additional verification is recommended.

🔴 **High Risk** — Transaction should be blocked or sent for manual review.

## ⚙️ How It Works

Transaction Data  
↓  
Machine Learning Model  
↓  
Fraud Probability  
↓  
Risk Score  
↓  
Risk Classification  
↓  
Actionable Explanation

## 🤖 Machine Learning

The prototype uses a Random Forest classifier.

Features include:

- Transaction amount
- Account age
- Transactions in the last 24 hours
- Device changes in the last 30 days
- Failed payment attempts
- International transaction indicator
- New device indicator
- Transaction hour

## 📊 Model Results

- Training samples: **12,000**
- Testing samples: **3,000**
- Accuracy: **77%**
- ROC-AUC: **0.7519**
- Simulated fraud rate: **21.73%**

The model is intended as a prototype and uses simulated transaction data rather than production payment data.

## 🖥️ Demo

The project includes an interactive Gradio interface where users can enter transaction details and receive an AI-generated risk assessment.

## 📁 Project Files

- `PayGuard_AI_Risk_Manager.ipynb` — Main development notebook
- `transactions.csv` — Simulated transaction dataset


## 🚀 Future Improvements

- Train on larger real-world fraud datasets
- Add explainable AI techniques such as SHAP
- Add real-time transaction monitoring
- Integrate with payment APIs
- Improve fraud recall and reduce false negatives
- Add transaction history and alerting

## ⚠️ Disclaimer

This is a prototype built for demonstration and experimentation. It is not intended for making real financial or payment decisions.
