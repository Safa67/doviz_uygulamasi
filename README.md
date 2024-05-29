# Currency Tracking Application

## Overview

This project is a simple **currency tracking desktop application** developed in **Python** during my **first year of Computer Engineering (2024)** as part of my programming practice and learning process.

The main purpose of the project was to gain hands-on experience with fundamental programming concepts such as working with APIs, building graphical user interfaces, managing databases, and performing data processing in Python.

The application retrieves real-time currency exchange rates from an external API and allows users to simulate investments in different currencies. It also keeps track of the user's assets and calculates the current total value as well as potential profit or loss.

---

## Features

* Fetches **live currency exchange rates** from an online API
* Displays a list of available currencies
* Allows users to **simulate currency investments** by entering an amount in Turkish Lira (TRY)
* Stores investment data in a **local SQLite database**
* Calculates the **current value of the user's assets**
* Displays **profit or loss based on updated exchange rates**
* Saves historical exchange rate data
* Allows users to view **previously recorded currency data by date**

---

## Technologies Used

The project was developed using the following technologies:

* **Python** – Main programming language
* **Tkinter** – Graphical User Interface (GUI)
* **SQLite** – Local database for storing data
* **HTTP Client / JSON** – API communication and data processing
* **python-dotenv** – Environment variable management for API keys

---

## How the Application Works

1. When the application starts, it sends a request to a currency exchange rate API.
2. The retrieved currency data is parsed and displayed in the interface.
3. The exchange rates are stored in a local SQLite database along with the current date and time.
4. Users can select a currency and enter the amount of Turkish Lira they want to invest.
5. The system calculates the amount of foreign currency purchased based on the current exchange rate.
6. All investments are saved in the database.
7. The application calculates the **current total value of the user's investments** based on the latest exchange rates.
8. It also displays whether the user is currently in **profit or loss**.
9. Previously recorded exchange rate data can be viewed by selecting a date from the history list.

---

## Learning Goals

This project was created as a learning exercise to practice:

* Consuming data from external APIs
* Building desktop applications with Tkinter
* Working with relational databases using SQLite
* Managing application data
* Structuring Python programs
* Performing financial calculations using real-time data

---

## Installation

1. Clone the repository:

```
git clone https://github.com/Safa67/doviz_uygulamasi.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory and add your API key:

```
API_KEY=your_api_key_here
```

4. Run the application:

```
python main.py
```

---

## Project Structure

```
doviz_uygulamasi
│
├── main.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
```

---

## Notes

This project was developed for **educational purposes** during my early programming experience.
It is intended as a learning project and does not provide financial advice.

---

## Author

Safa
Computer Engineering Student
