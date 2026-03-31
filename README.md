# ⚽ European Football League Standings Checker

A modern Desktop Application (GUI) built with Python that connects to a SQLite database to visualize football standings for major European leagues from **2008** to **2016**.

---

## 📊 Project Overview
This application provides a user-friendly interface to explore historical football data. It calculates real-time league tables—including **Points (P)**, **Goals For (GF)**, **Goals Against (GA)**, and **Goal Difference (GD)**—by querying a comprehensive match database.

### Supported Data Range
* **Leagues:** Premier League, La Liga, Serie A, Ligue 1, and Bundesliga.
* **Seasons:** 8 seasons from **2008/2009** through **2015/2016**.

---

## 🚀 Key Features
* **Modern UI:** Built using `customtkinter` for a sleek, dark-themed desktop experience.
* **Multithreading:** Database queries run in a background `threading` task to keep the UI responsive and prevent "freezing" during heavy calculations.
* **Visual Progress:** Includes an indeterminate progress bar to notify the user when data is being fetched.
* **Dynamic Tables:** Uses `CTkTable` to display standings in a clean, professional grid.
* **Smart Sorting:** Teams are automatically ranked by **Points**, with **Goal Difference** used as the primary tie-breaker.

---

## 🛠️ Requirements

To run the application, you must install the following Python libraries:

```bash
pip install customtkinter CTkTable
Don't forget to downloas the database database.sqlite from this link and put in the project folder:  https://www.kaggle.com/datasets/hugomathien/soccer
