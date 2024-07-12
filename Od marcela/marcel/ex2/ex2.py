import json
from sys import argv, exit

import requests


def downloadFromUniProt(uniprot_id):
    url = f"https://www.ebi.ac.uk/proteins/api/proteins/{uniprot_id}"

    response = requests.get(url, headers={
        "Accept":"application/json"
        }
    )

    if response.ok:
        return response.text

    print(f"UniProt ID {uniprot_id} does not exist in database")
    exit()


def stats(sequence):
    aminoacid_stats = {}

    for aminoacid in sequence:
        
        if aminoacid not in aminoacid_stats:
            aminoacid_stats[aminoacid] = 0

        aminoacid_stats[aminoacid] += 1

    
    for aminoacid, statistic in aminoacid_stats.items():
        print(
            f"{aminoacid} => {statistic}"
        )

if __name__ == "__main__":
    try:
        uniprot_id = argv[1]
    except IndexError:
        print("hey! please insert uniprot id")
        exit()

    data = downloadFromUniProt(uniprot_id)
    data_as_dict = json.loads(data)

    sequence = data_as_dict['sequence']['sequence']

    stats(sequence)