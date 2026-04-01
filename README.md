# ⚽ European Football League Standings Checker

A modern Desktop Application (GUI) built with Python that connects to a SQLite database to visualize football standings for major European leagues from **2008** to **2016**.

---

## 📊 Project Overview
This application provides a user-friendly interface to explore historical football data. It uses complex SQL queries to calculate real-time statistics—including **Points (P)**, **Wins/Draws/Losses**, **Goal Difference (GD)**, and detailed match-by-match pathways.


### Supported Data Range
* **Leagues:** Premier League, La Liga, Serie A, Ligue 1, and Bundesliga.
* **Seasons:** 8 seasons from **2008/2009** through **2015/2016**.

---

## 🚀 Key Features
* **Multi-Page Navigation:** A clean home menu to toggle between the **League Standing Checker** and the **Team Pathway Tracker**.
* **Final Standings:** Calculates full league tables with Position, Team Name, W/D/L records, Goals For (GF), Goals Against (GA), Goal Difference (GD), and Total Points (P).
* **Team Pathway:** A dedicated tool to view every match a specific team played in a chosen season, including dates, scores, and Home (H) / Away (A) indicators.
* **Responsive UI (Multithreading):** Database queries run in background threads using Python's `threading` module, ensuring the GUI never freezes during heavy data retrieval.
* **Dynamic Team Selection:** The Team menu automatically updates based on the selected League and Season to ensure valid queries.
* **Scrollable Match History:** Uses `CTkScrollableFrame` to handle full 38-game season lists gracefully without cluttering the interface.
---

## 🛠️ Requirements

To run the application, you must install the following Python libraries:

```bash
pip install customtkinter CTkTable pillow
Don't forget to downloas the database database.sqlite from this link and put in the project folder:  https://www.kaggle.com/datasets/hugomathien/soccer
