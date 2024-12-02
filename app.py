#from flask import Flask
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://www.usafis.org/green-card-information/dv-lottery/dv-lottery-results/"

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find("table")

columns = []
data = []

rows = table.find_all("tr")

for index, row in enumerate(rows):
    cols = row.find_all("p")

    if index == 0:
        columns = [col.get_text() for col in cols]
    else:
        data_row = [col.get_text() for col in cols]
        data.append(data_row)

df = pd.DataFrame(data, columns=columns)
df.to_csv('download.csv', index=False)
