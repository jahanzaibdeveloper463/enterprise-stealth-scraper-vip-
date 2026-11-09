"""
Project: Enterprise Stealth Web Scraper & Data Pipeline
Author: Jahanzaib
Description: Advanced production-grade web extraction engine featuring dynamic 
             User-Agent rotation, robust exception recovery, multi-page pagination 
             traversal, and automated dual-format data persistence (Excel & CSV).
"""

import sys
import time
import logging
import random
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Configure enterprise-grade logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (Thread-ID: %(_thread)d) %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Enterprise configuration constants
TARGET_BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
EXCEL_OUTPUT = "enterprise_harvested_data.xlsx"
CSV_OUTPUT = "enterprise_harvested_data.csv"
MAX_PAGES_TO_CRAWL = 3

# Pool of enterprise User-Agents to bypass basic bot-detection filters (Anti-Scraping Shield)
USER_AGENT_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

def get_stealth_headers():
    """Generates randomized request headers to mimic genuine human browser traffic."""
    return {
        "User-Agent": random.choice(USER_AGENT_POOL),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive"
    }

def execute_stealth_crawl():
    """Executes resilient multi-page crawl with randomized throttling and error recovery."""
    master_dataset = []
    
    logging.info("=== INITIALIZING ENTERPRISE STEALTH CRAWL PIPELINE ===")

    for page_idx in range(1, MAX_PAGES_TO_CRAWL + 1):
        target_url = TARGET_BASE_URL.format(page_idx)
        headers = get_stealth_headers()
        
        logging.info(f"Targeting Page {page_idx} | Dispatching HTTP GET with stealth headers...")

        try:
            # Randomized polite throttling to prevent server rate-limiting / IP bans
            time.sleep(random.uniform(1.2, 2.8))
            
            response = requests.get(target_url, headers=headers, timeout=12)
            
            if response.status_code == 404:
                logging.warning(f"Endpoint returned 404 Not Found on page {page_idx}. Halting pagination.")
                break
                
            response.raise_for_status()

        except requests.exceptions.RequestException as net_err:
            logging.error(f"Network transport fault encountered on page {page_idx}: {net_err}")
            continue # Fault-tolerant skip: moves to next page instead of crashing pipeline

        # Parse DOM markup tree
        soup = BeautifulSoup(response.text, "html.parser")
        product_cards = soup.find_all("article", class_="product_pod")

        if not product_cards:
            logging.warning(f"DOM tree validation failed: No target nodes found on page {page_idx}.")
            continue

        for idx, card in enumerate(product_cards, start=1):
            try:
                title = card.find("h3").find("a").get("title", "N/A").strip()
                raw_price = card.find("p", class_="price_color").text
                clean_price = float(raw_price.replace("Â£", "").replace("£", "").strip())
                stock_status = card.find("p", class_="instock availability").text.strip()
                
                # Append structured record
                master_dataset.append({
                    "Record UID": f"ENT-2026-P{page_idx}-{idx:03d}",
                    "Item Title": title,
                    "Unit Price (GBP)": clean_price,
                    "Inventory Status": stock_status,
                    "Extraction Engine": "StealthCrawler-v4"
                })
            except AttributeError as parse_err:
                logging.debug(f"Skipping malformed DOM element due to parsing exception: {parse_err}")
                continue

    logging.info(f"Crawl sequence completed. Total valid records harvested: {len(master_dataset)}")
    return master_dataset

def persist_enterprise_data(records):
    """Performs dual-format data serialization into high-performance Excel and CSV buffers."""
    if not records:
        logging.warning("Master dataset is empty. Aborting file persistence.")
        return

    logging.info("Compiling dataset into high-performance pandas DataFrame...")
    df = pd.DataFrame(records)

    # Dual persistence: Exporting directly to Excel and CSV simultaneously
    df.to_excel(EXCEL_OUTPUT, index=False)
    df.to_csv(CSV_OUTPUT, index=False)
    
    logging.info(f"SUCCESS: Data successfully flushed to disk -> '{EXCEL_OUTPUT}' & '{CSV_OUTPUT}'")

if __name__ == "__main__":
    harvested_records = execute_stealth_crawl()
    persist_enterprise_data(harvested_records)
