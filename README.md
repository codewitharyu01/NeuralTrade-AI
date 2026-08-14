NeuralTrade AI 📈

NeuralTrade AI is a hybrid AI-powered stock prediction and analysis dashboard that combines historical market data, technical indicators, and financial news sentiment analysis to provide data-driven stock insights.

🚀 Features

- 📊 Historical stock price visualization
- 📈 Technical indicators and market analysis
- 📰 Financial news sentiment analysis
- 🤖 AI-based stock price prediction
- 🟢 BUY / 🟡 HOLD / 🔴 SELL recommendations
- 🎯 Prediction confidence score
- 📋 Stock watchlist
- 🔮 Recent predictions
- 💡 AI-generated market insights
- 🔐 User registration and login system

🧠 Machine Learning

The project uses a hybrid prediction approach combining:

- LSTM — for learning patterns from historical stock-price data
- Random Forest — for additional prediction and feature-based analysis
- Sentiment Analysis — to analyze financial news headlines and determine market sentiment

Financial news sentiment is analyzed using Times of India financial news headlines.

🛠️ Tech Stack

- Python
- Flask
- Jinja2
- HTML5
- CSS3
- JavaScript
- Pandas
- NumPy
- Scikit-learn
- TensorFlow / Keras
- SQLite
- Chart.js

📂 Project Structure

NeuralTrade-AI/
│
├── app.py
├── database.py
├── requirements.txt
│
├── models/
│   └── predictor.py
│
├── utils/
│   ├── data_fetcher.py
│   ├── indicators.py
│   ├── news.py
│   └── sentiment.py
│
├── templates/
│   └── dashboard.html
│
├── static/
│   └── ...
│
└── .gitignore

⚙️ Installation

Clone the repository:

git clone https://github.com/codewitharyu01/NeuralTrade-AI.git
cd NeuralTrade-AI

Install dependencies:

pip install -r requirements.txt

Run the Flask application:

python app.py

Open the application in your browser:

http://127.0.0.1:5000

📌 Note

The trained model and large stock dataset are excluded from this repository because of GitHub file-size limitations.

🔮 Future Improvements

- Real-time market data integration
- Improved prediction accuracy
- Portfolio tracking
- Advanced deep-learning models
- Cloud deployment
- More financial news sources

👨‍💻 Author

Aryan

B.Tech — Computer Science (AI/ML)
