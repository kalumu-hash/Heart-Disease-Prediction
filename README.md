# ❤️ Heart Disease Prediction using Machine Learning

## 📌 Project Overview
Heart disease remains one of the leading causes of mortality worldwide. 
This project aims to build and evaluate machine learning models capable of predicting the likelihood of heart disease based on clinical patient data.

The project compares classical machine learning models and neural networks to determine which approach performs best for structured medical data.

---

## 📊 Dataset
The dataset contains clinical features such as:

- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol Level
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate
- Exercise-Induced Angina
- Oldpeak
- ST Slope

Target Variable:
- 0 → No Heart Disease
- 1 → Heart Disease

The dataset is relatively balanced, making it suitable for binary classification.

---

## 🧠 Models Implemented

### 1️⃣ Logistic Regression
- Baseline linear model
- Used to establish initial performance benchmark

### 2️⃣ Random Forest Classifier
- Ensemble-based model
- Captures nonlinear feature interactions
- Provides feature importance insights

### 3️⃣ Neural Network (TensorFlow / Keras)
- Multi-layer perceptron architecture
- ReLU activation in hidden layers
- Sigmoid activation in output layer
- Binary cross-entropy loss

---

## 📈 Model Evaluation

Models were evaluated using:

- Accuracy Score
- Confusion Matrix
- Classification Report
- Feature Importance Analysis (Random Forest)
- Training/Validation Accuracy Curves (Neural Network)

Initial results show strong performance (~85–90% accuracy), with ensemble methods slightly outperforming linear models.

---

## 🔬 Research Motivation

This project explores:

- The effectiveness of classical ML vs deep learning for tabular medical data
- The impact of feature scaling
- Model interpretability in healthcare applications

---

## 🚀 Future Improvements

- Hyperparameter tuning (GridSearch / RandomSearch)
- Cross-validation
- ROC-AUC analysis
- Deployment as an interactive web application
- Login-based prediction interface
- Model explainability using SHAP or LIME

---

## 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- TensorFlow / Keras
- Matplotlib
- Seaborn
- Jupyter Notebook

---

## 📂 Project Structure

heart-disease-prediction/
│
├── data/
│   └── heart.csv
│
├── notebook.ipynb
├── README.md
├── requirements.txt
├── .gitignore

## Author
Lilian Maluki
BSc Computer Science
Final year project
