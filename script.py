"""
Scrapes multiple headlines from The Daily Pennsylvanian website and saves them to a 
JSON file that tracks headlines over time.
"""

import os
import sys
import json
import bs4
import requests
import loguru
import daily_event_monitor


def scrape_data_point():
    """
    Scrapes the top headline from the "Featured", "News", "Sports", and "Opinion" 
    sections on the homepage and the latest article from the full "News", "Sports", and "Opinion" pages.

    Returns:
        dict: A dictionary containing the top headlines from each section.
    """
    headers = {
        "User-Agent": "cis3500-scraper"  # Identifying the scraper to avoid 403 errors
    }
    
    base_url = "https://www.thedp.com/"
    categories = ["news", "sports", "opinion"]
    
    headlines = {}

    # Fetch homepage content
    req = requests.get(base_url, headers=headers)
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")

        # Scrape Featured section
        featured = soup.find("div", class_="featured-story")
        if featured:
            headline = featured.find("a").text.strip()
            headlines["Featured"] = headline

        # Scrape News, Sports, and Opinion sections from the homepage
        for category in categories:
            section = soup.find("section", class_=category)
            if section:
                headline = section.find("a").text.strip()
                headlines[category.capitalize()] = headline

    else:
        loguru.logger.error("Failed to retrieve the homepage.")

    # Fetch the latest article from full "News", "Sports", and "Opinion" pages
    for category in categories:
        url = f"{base_url}section/{category}"
        req = requests.get(url, headers=headers)
        loguru.logger.info(f"Requesting: {url} | Status: {req.status_code}")

        if req.ok:
            soup = bs4.BeautifulSoup(req.text, "html.parser")
            article = soup.find("a", class_="article-link")  # Adjust this class if needed
            if article:
                headlines[f"{category.capitalize()} (Full Page)"] = article.text.strip()
        else:
            loguru.logger.error(f"Failed to retrieve {category} page")

    loguru.logger.info(f"Extracted headlines: {headlines}")
    return headlines


if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data_point = scrape_data_point()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data
    if data_point is not None:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
