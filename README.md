# ⚽ European Football League Standings Checker

A Python-based CLI tool that connects to a SQLite database to calculate and display league standings for major European football leagues between the **2008/2009** and **2015/2016** seasons.

## 📊 About the Project
This project uses a relational database containing comprehensive match data from Europe's top leagues. It dynamically calculates team statistics including **Points (P)**, **Goals For (GF)**, **Goals Against (GA)**, and **Goal Difference (GD)** to generate a live standing table based on historical data.

### Supported Leagues
* 🏴󠁧󠁢󠁥󠁮󠁧󠁿 England Premier League
* 🇪🇸 Spain LIGA BBVA
* 🇮🇹 Italy Serie A
* 🇫🇷 France Ligue 1
* 🇩🇪 Germany 1. Bundesliga and others...

### Supported Seasons
* 8 Seasons ranging from **2008/2009** to **2015/2016**.

---

## 🚀 Features
* **Live SQL Queries:** Calculates points and goal statistics on-the-fly using advanced SQL queries (CTEs and Unions).
* **Tie-Breaking Logic:** Standings are sorted primarily by **Points** and secondarily by **Goal Difference**.
* **Data Validation:** Includes robust input checking using `.isdigit()` and range validation to ensure smooth user experience.
* **Error Handling:** Uses `try-except` blocks to manage database connection issues or query errors gracefully.

---

## 🛠️ Requirements
* **Python 3.x**
* **SQLite3** (built-in with Python)
* **`database.sqlite`** that you can find in kaggle via this link: https://www.kaggle.com/datasets/hugomathien/soccer
2. Run the script:
   ```bash
   python query.py
