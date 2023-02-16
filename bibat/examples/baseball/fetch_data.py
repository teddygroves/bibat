import os

import pandas as pd
import pyreadr
import requests

URLS = {
    "2006": "https://raw.githubusercontent.com/stan-dev/example-models/master/knitr/pool-binary-trials/baseball-hits-2006.csv",
    "recent": "https://discourse.mc-stan.org/uploads/short-url/cRJtia2jKxiX01ZEraHUVK7jbHI.RData",
}
OUT_FILES = {
    "2006": os.path.join("data", "raw", "baseball-hits-2006.csv"),
    "recent": os.path.join("data", "raw", "recent.RData"),
}

if __name__ == "__main__":
    print(f"Fetching 2006 data from {URLS['2006']}")
    data_2006 = pd.read_csv(URLS["2006"], comment="#")
    print(f"Writing 2006 data to {OUT_FILES['2006']}")
    data_2006.to_csv(OUT_FILES["2006"])
    print(f"Fetching recent data from {URLS['recent']}")
    with requests.get(URLS["recent"]) as f:
        recent = f.text
    print(f"Writing to {OUT_FILES['recent']}")
    with open(OUT_FILES["recent"], "wb") as f:
        f.write(recent.encode("utf8", errors="replace"))
