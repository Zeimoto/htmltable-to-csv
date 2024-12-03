import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import sys

url = sys.argv[1]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")
#print(f"SOUP: {soup}")

table = soup.find("table")

columns = []
data = []

rows = table.find_all("tr")

for index, row in enumerate(rows):
    #cols = row.find_all("p")

    data_row = []

    for col in row:
    
#        print(col, type(col))
        col_text = col.get_text().replace("\n", "").strip()

        if index == 0:
            #print(f"column: {col_text}")
            columns.append(col_text)

        else:
            data_row.append(col_text)

    if index != 0:
        data.append(data_row)

#Let's clean empty columns and rows
#first add the columns array on top of the data matrix
data_copy = list()
data.insert(0, columns)
data_copy = data
print(f"Data_copy: {data_copy}")

data_copy = np.array(data_copy)

#check for empty columns and rows
empty_columns = np.all(data_copy == '', axis=0)
empty_rows = np.all(data_copy == '', axis=1)

#filtered out the empty columns and rows from the matrix
data_copy = data_copy[:, ~empty_columns]
data_copy = data_copy[~empty_rows]

#now that the matrix empty columns where removed, reset the columns and data in seperate varibles
columns = data_copy[0, :]
data = data_copy[1:, :]

print(f"Columns: {columns}")
print(f"Data:{data}")

df = pd.DataFrame(data, columns=columns)
df.to_csv('download.csv', index=False)

 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python test.py {sys.argv[1]}")
        sys.exit(0)
