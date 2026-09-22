# WhatsApp Conversation Intelligence System

🚀 **Live Demo:** [Open the deployed app](https://whatsapp-conversation-intelligence-epshvdv9oaacl6wpvxxvvj.streamlit.app/)



An interactive **NLP and Machine Learning based WhatsApp chat analysis system** that extracts meaningful insights from exported WhatsApp conversations and predicts conversational response behavior.

## ✨ Features

### 📊 Conversation Analytics
- Total messages, words, media and links shared
- Daily and monthly conversation timelines
- Most active days and months
- Weekly activity heatmap
- Most active users

### 📝 Text Analysis
- WordCloud generation
- Most frequently used words
- Emoji frequency analysis
- Hinglish-aware stop-word filtering
- Text preprocessing and cleaning

### 🤖 Machine Learning Features
- **Reply Probability:** Predicts whether a message is likely to receive a reply
- **First Responder Prediction:** Predicts which participant is most likely to reply first
- **Response Time Prediction:** Estimates how quickly a reply may arrive
- Uses conversational, temporal and text-based features

### 💻 Interactive Dashboard

Built using **Streamlit**, allowing users to upload their exported WhatsApp chat and interactively explore conversation patterns and ML predictions.

---

## 🛠️ Tech Stack

**Programming:** Python

**Data Processing:** Pandas, NumPy

**Machine Learning:** Scikit-learn

**NLP:** TF-IDF, Text Preprocessing

**Visualization:** Matplotlib, Seaborn, WordCloud

**Dashboard:** Streamlit

**Other Libraries:** Emoji, URLExtract

---

## 🧠 Machine Learning Workflow

```text
WhatsApp Chat Export
        ↓
Data Parsing & Preprocessing
        ↓
Feature Extraction
        ↓
Text + Temporal + Conversation Features
        ↓
Machine Learning Models
        ↓
Reply Prediction
        ↓
First Responder Prediction
        ↓
Response Time Prediction
