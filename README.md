# TARG —  Stock Forecast and Analysis Platform

**TARG** (Time-series Analysis & Report Generator) is a web-based platform focused on forecasting and analyzing the stocks of Banco do Brasil (BBAS3).  
The project combines time series modeling and sentiment analysis to deliver insightful information for investors, analysts, and finance enthusiasts.

---

## 🚀 Features

- **BBAS3 Stock Price Forecasting**  
  Interactive charts displaying short-term (5-day) forecasts using time series models.

- **News Sentiment Analysis**  
  Automated extraction of recent news related to Banco do Brasil, each analyzed for sentiment (positive, negative, or neutral) to assess potential market impact.

- **Historical Stock Data Visualization**  
  A dedicated page with detailed historical data of BBAS3 from 2010 to the present, with filtering and analysis options.

---

## 🧰 Technologies Used

![Next JS](https://img.shields.io/badge/Next-black?style=for-the-badge&logo=next.js&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI_API-412991?style=for-the-badge&logo=openai&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![YahooFinance](https://img.shields.io/badge/Yahoo_Finance-6001D2?style=for-the-badge&logo=yahoo&logoColor=white)

---

## 🛠️ Project Building Steps

### 📊 Data Collection
- Collected historical BBAS3 stock data from 2010 onward using the YahooFinance library.
- Cleaned and preprocessed the time series data for modeling.
- Implemented web scraping using **Selenium** to extract the latest news about Banco do Brasil from the **InfoMoney** website.

### 🤖 Time Series Forecasting
- Built a forecasting model using **LSTM** to predict the next 5 trading days.
- Evaluated the model using metrics such as RMSE and MAPE.
- Selected the best-performing parameters for deployment.

### 💬 Sentiment Analysis
- Parsed the scraped news headlines and summaries.
- Used the **OpenAI API** to classify news sentiment as **positive**, **negative**, or **neutral** in relation to BBAS3 stocks.
- Displayed the sentiment result alongside each news item.

### 🧱 Web Application Development
- Developed the backend using **Python** and **FastAPI**.
- Built the frontend with **NextJS**, integrating visualizations with **Chart.js** or **Plotly**.
- Implemented dynamic routes to serve forecasts, historical data, and sentiment-analyzed news.

![Logo](/Backend/Targ.png)
