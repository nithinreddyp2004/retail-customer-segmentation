# 🛒 Retail Customer Segmentation App

A machine learning web application that segments retail customers into groups using **K-Means Clustering** and **RFM Analysis** (Recency, Frequency, Monetary). Built with Python, Scikit-learn, and deployed using Streamlit.

---

## 🚀 Live Demo

👉 [Click here to try the live app!](https://retail-customer-segmentation1.streamlit.app/)
> Deployed on Streamlit Cloud

---

## 📌 Problem Statement

Retail businesses struggle to understand their diverse customer base. This app automatically groups customers by purchasing behavior using RFM Analysis, helping businesses target the right customers with the right strategy.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core programming language |
| Pandas & NumPy | Data processing |
| Scikit-learn | K-Means clustering model |
| StandardScaler | Feature scaling |
| Matplotlib & Seaborn | Data visualization |
| Streamlit | Web app deployment |

---

## 📊 Customer Segments

| Segment | Description |
|---|---|
| High Value Customers | Buy frequently, spend the most |
| Loyal Customers | Buy regularly with good spend |
| At Risk Customers | Haven't bought in a while |
| New Customers | Recently joined, low frequency |

---

## 📈 RFM Analysis

| Feature | Description |
|---|---|
| Recency | How recently a customer made a purchase |
| Frequency | How often a customer makes a purchase |
| Monetary | How much a customer spends in total |

---

## 📁 Project Structure

```
retail-customer-segmentation/
│
├── app.py                           # Streamlit web app
├── model_retail.ipynb               # Jupyter notebook with EDA and model training
├── customer_segmentation_model.pkl  # Saved model, scaler and cluster map
├── Online Retail.xlsx               # Dataset
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

---

## ⚙️ How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/nithinreddyp2004/retail-customer-segmentation.git

# 2. Go into the folder
cd retail-customer-segmentation

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

---

## 🙋 Author

**Nithin Reddy P** — [GitHub](https://github.com/nithinreddyp2004)
