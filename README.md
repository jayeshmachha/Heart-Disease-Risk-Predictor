<div align="center">

# ❤️ Heart Disease Risk Predictor

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/heart-disease-prediction)](https://github.com/yourusername/heart-disease-prediction/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/heart-disease-prediction)](https://github.com/yourusername/heart-disease-prediction/network)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

</div>

## 🎯 Overview

An AI-powered web application that predicts the risk of heart disease based on clinical parameters using Machine Learning algorithms. The system provides real-time predictions with interactive visualizations and health insights.

## ✨ Features

- 🔮 **Real-time Predictions** - Instant risk assessment using KNN algorithm
- 📊 **Interactive Dashboard** - Visualize health metrics and risk factors
- 🎨 **Modern UI** - Clean, responsive interface with Plotly charts
- 📱 **Mobile Friendly** - Access from any device
- 💡 **Health Tips** - Personalized recommendations based on results

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────────┐
│ User Interface │
│ (Streamlit Web App) │
│ - Input forms for clinical data │
│ - Real-time form validation │
└─────────────────────────┬───────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Input Processing │
│ (Data Validation & Encoding) │
│ - One-hot encoding for categorical variables │
│ - Data type conversion │
│ - Missing value handling │
└─────────────────────────┬───────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Feature Engineering │
│ (Scaling & Transformation) │
│ - StandardScaler for numerical features │
│ - Feature alignment with training data │
└─────────────────────────┬───────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ ML Prediction Engine │
│ (KNN - K-Nearest Neighbors) │
│ - Loads pre-trained model (86.4% accuracy) │
│ - Calculates risk probability │
│ - Returns binary prediction (0 = Low Risk, 1 = High Risk)│
└─────────────────────────┬───────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Results Visualization │
│ (Risk Score & Health Metrics) │
│ - Risk gauge meter │
│ - Color-coded results (Red/Green) │
│ - Personalized health recommendations │
└─────────────────────────────────────────────────────────────┘

## 📊 Model Performance

After training and evaluating multiple algorithms on 918 patient records:

| Model | Accuracy | F1-Score | Precision | Recall |
|-------|----------|----------|-----------|---------|
| **Logistic Regression** | 86.96% | 88.57% | 87.2% | 90.0% |
| **KNN (Selected)** | 86.41% | 88.15% | 86.8% | 89.5% |
| **SVM** | 84.78% | 86.79% | 85.3% | 88.4% |
| **Naive Bayes** | 85.33% | 86.83% | 86.1% | 87.6% |
| **Decision Tree** | 77.72% | 80.00% | 78.9% | 81.1% |

### Why KNN was Selected?

| Criteria | Why KNN Wins |
|----------|---------------|
| **Accuracy** | 86.41% (2nd best, close to 1st) |
| **Interpretability** | Easy to explain to non-technical users |
| **Non-linear Data** | Handles complex medical relationships |
| **Outlier Robust** | Medical data often has outliers |
| **Inference Speed** | Fast enough for real-time predictions |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip package manager


