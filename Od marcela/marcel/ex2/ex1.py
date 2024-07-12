from sys import argv, exit

import requests


def downloadFromUniProt(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"

    response = requests.get(url)

    if response.ok:
        print(response.text)
        return

    print(f"UniProt ID {uniprot_id} does not exist in database")

if __name__ == "__main__":
    try:
        uniprot_id = argv[1]
    except IndexError:
        print("hey! please insert uniprot id")
        exit()

    downloadFromUniProt(uniprot_id)