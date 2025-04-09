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

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SARIMA](https://img.shields.io/badge/SARIMA-FF6F00?style=for-the-badge&logo=python&logoColor=white)
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
- Built a forecasting model using **SARIMA** to predict the next 5 trading days.
- Evaluated the model using metrics such as RMSE and MAPE.
- Selected the best-performing parameters for deployment.

### 💬 Sentiment Analysis
- Parsed the scraped news headlines and summaries.
- Used the **OpenAI API** to classify news sentiment as **positive**, **negative**, or **neutral** in relation to BBAS3 stocks.
- Displayed the sentiment result alongside each news item.

### 🧱 Web Application Development
- Developed the backend using **Python** and **FastAPI**.
- Built the frontend with **HTML**, **CSS**, and **JavaScript**, integrating visualizations with **Chart.js** or **Plotly**.
- Implemented dynamic routes to serve forecasts, historical data, and sentiment-analyzed news.

![Logo](/Backend/Targ.png)
