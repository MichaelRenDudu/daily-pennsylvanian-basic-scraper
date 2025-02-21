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


# GitHub Actions Schedule Explanation

The `on.schedule` key in `.github/workflows/scrape.yaml` uses a **cron expression** to define when the scraper runs.

## **Current Schedule:**

- **0** → Minute (`0`) → The script runs at the start of the hour.
- **3** → Hour (`3`) → The script runs at **3:00 AM UTC**.
- **\*** → Day of the month (`*`) → Runs every day of the month.
- **\*** → Month (`*`) → Runs every month.
- **\*** → Day of the week (`*`) → Runs every day of the week.

### **Interpretation:**
The scraper currently **runs once per day at 3:00 AM UTC**. This ensures we capture a snapshot of headlines every day.

## **Modifying the Schedule**
To **increase the frequency**, we can update the cron expression to **run the scraper twice a day**:

- **3,15** → Runs at both **3 AM and 3 PM UTC**.

Updating `.github/workflows/scrape.yaml`:
```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 3,15 * * *"  # 📅 Runs twice daily at 3 AM & 3 PM UTC








