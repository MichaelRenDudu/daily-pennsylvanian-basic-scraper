# Daily Pennsylvanian Basic Scraper

## Overview
This project is a web scraper that extracts the top headlines from The Daily Pennsylvanian website. The scraper is implemented in Python and uses GitHub Actions to run automatically on a schedule. The extracted data is stored in a JSON file, tracking headlines over time.

## Features
- **Avoids 403 errors** by setting a `User-Agent` header.
- **Scrapes multiple headlines**:
  - **Top headline** from the **"Featured", "News", "Sports", and "Opinion"** sections on the homepage.
  - **Latest article** from the full **"News", "Sports", and "Opinion"** pages.
- **Automates data collection** using GitHub Actions.
- **Stores headlines in JSON format** with a timestamp.

---

## 📜 **How the Scraper Works**
The scraper fetches data using **requests**, parses the HTML with **BeautifulSoup**, and logs results using **loguru**. The collected headlines are stored in `data/daily_pennsylvanian_headlines.json`.





