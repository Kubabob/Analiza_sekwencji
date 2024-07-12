import requests
import pandas as pd


def getDataFromKegg(operation, argument):
    url = f"https://rest.kegg.jp/{operation}/{argument}"

    resp = requests.get(
        url
    )

    if resp.ok:
        return resp.text
    
dane = pd.read_csv('uniprot_id')
print(dane)
