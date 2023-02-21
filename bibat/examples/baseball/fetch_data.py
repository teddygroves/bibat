"""Fetch raw data from the internet."""

import os

import pandas as pd

URLS = {
    "2006": "https://raw.githubusercontent.com/stan-dev/"
    "example-models/master/knitr/pool-binary-trials/baseball-hits-2006.csv",
    "bdb-main": "https://raw.githubusercontent.com/chadwickbureau/"
    "baseballdatabank/master/core/Batting.csv",
    "bdb-post": "https://raw.githubusercontent.com/chadwickbureau/"
    "baseballdatabank/master/core/BattingPost.csv",
    "bdb-apps": "https://raw.githubusercontent.com/chadwickbureau/"
    "baseballdatabank/master/core/Appearances.csv",
}
OUT_FILES = {
    "2006": os.path.join("data", "raw", "2006.csv"),
    "bdb-main": os.path.join("data", "raw", "bdb-main.csv"),
    "bdb-post": os.path.join("data", "raw", "bdb-post.csv"),
    "bdb-apps": os.path.join("data", "raw", "bdb-apps.csv"),
}

if __name__ == "__main__":
    for name, url in URLS.items():
        print(f"Fetching {name} data from {url}")
        data = pd.read_csv(url, comment="#")
        print(f"Writing {name} data to {OUT_FILES[name]}")
        data.to_csv(OUT_FILES[name])
