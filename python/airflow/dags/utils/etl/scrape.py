"""
Scrapes historical earthquake data at http://www.koeri.boun.edu.tr/sismo/zeqdb/default.asp
"""

import requests
import pandas as pd
import random


class KOERI:
    def __init__(self):
        self.headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
        }
        self.url = "http://www.koeri.boun.edu.tr/sismo/zeqdb/submitRecSearchT.asp"
        self.download_url = "http://koeri.boun.edu.tr/sismo/zeqdb/download.php?download_file={}"
        self.params = {
            "bYear": "2019", "bMont": "01", "bDay": "01",
            "eYear": "2019", "eMont": "12", "eDay": "31",
            "EnMin": "30.00", "EnMax": "47.00",
            "BoyMin": "21.00", "BoyMax": "50.00",
            "MAGMin": "0.01", "MAGMax": "10.0",
            "DerMin": "0", "DerMax": "1000",
            "Tip": "Hepsi"
        }
        self.columns = [
            "Deprem Kodu", "timestamp", "Enlem", "Boylam", "Der(km)",
            "xM", "MD", "ML", "Mw", "Ms",
            "Mb", "Tip", "Yer"
        ]

    def read_data(self, year):
        self.params["bYear"], self.params["eYear"] = year, year
        self.params["ofName"] = self._generate_file_name()
        request = requests.get(self.url, params=self.params, headers=self.headers)
        df = pd.read_csv(self.download_url.format(self.params["ofName"]), sep="\t", encoding="ISO-8859-1")
        for idx, row in df.iterrows():
            yield list(self._parse_row(row)[self.columns])

    @staticmethod
    def _parse_row(row):
        row["timestamp"] = f"{row['Olus tarihi']} {row['Olus zamani']}"
        row["Yer"] = row["Yer"]
        return row

    def _generate_file_name(self):
        b_date = f"{self.params['bYear']}{self.params['bMont']}{self.params['bDay']}"
        e_date = f"{self.params['eYear']}{self.params['eMont']}{self.params['eDay']}"
        mag = f"{self.params['MAGMin']}_{self.params['MAGMax']}"
        rand_num = f"{random.randint(10, 99)}_{random.randint(100, 999)}"
        return f"{b_date}_{e_date}_{mag}_{rand_num}.txt"
