import json
import pandas as pd
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
import google_play_scraper as google
from collections import defaultdict
from FullCategoryApps import scrape_data
import os
from tqdm import tqdm
import datetime
import time
print(os.getcwd())

# Call the scrape_data function from the FullCategoryApps script. 
GOOGLE_PLAY_DATA = scrape_data()

data_dict = defaultdict(list)

for index, row in GOOGLE_PLAY_DATA.iterrows():
    print(index + 1, "/", len(GOOGLE_PLAY_DATA), ".Getting data for: ", row["App ID"])
    
    info = google.app(row["App ID"])
    
    data_dict["Application"].append(row["Application"])
    data_dict["App ID"].append(row["App ID"])
    data_dict["Installs"].append(info["minInstalls"])
    data_dict["Number of Ratings"].append(info["ratings"])
    data_dict["Average Score"].append(info["score"])
    data_dict["Contains Ads"].append(info["containsAds"])
    data_dict["IAP"].append(info["offersIAP"])
    data_dict["In-App Prices Range"].append(info["inAppProductPrice"])
    data_dict["Genre"].append(info["genre"])
    data_dict["Content Rating"].append(info["contentRating"])
    data_dict["Release Date"].append(info["released"]) 
    data_dict["Reviews"].append(info["comments"])

FINAL = pd.DataFrame(data_dict)

# FINAL.to_csv("Google Play Data_{}.csv".format(datetime.date.today()))
