"""Fetch raw data from the internet."""

import logging
from pathlib import Path

import pandas as pd

URLS = {
    "2006": "https://raw.githubusercontent.com/stan-dev/"
    "example-models/master/knitr/pool-binary-trials/baseball-hits-2006.csv",
    "bdb-main": "https://raw.githubusercontent.com/cbwinslow/"
    "baseballdatabank/master/core/Batting.csv",
    "bdb-post": "https://raw.githubusercontent.com/cbwinslow/"
    "baseballdatabank/master/core/BattingPost.csv",
    "bdb-apps": "https://raw.githubusercontent.com/cbwinslow/"
    "baseballdatabank/master/core/Appearances.csv",
}
RAW_DIR = Path("data") / "raw"
OUT_FILES = {
    "2006": RAW_DIR / "2006.csv",
    "bdb-main": RAW_DIR / "bdb-main.csv",
    "bdb-post": RAW_DIR / "bdb-post.csv",
    "bdb-apps": RAW_DIR / "bdb-apps.csv",
}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    for name, url in URLS.items():
        logging.info("Fetching %s data from %s", name, url)
        data = pd.read_csv(url, comment="#")
        logging.info("Writing %s data to %s", name, OUT_FILES[name])
        data.to_csv(OUT_FILES[name])
