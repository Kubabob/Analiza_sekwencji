from sys import argv
import requests


def getFastaFromUniProt(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
    
    resp = requests.get(url)

    if resp.ok:
        print(resp.text)

        return
    
    print(f"UniProt ID {uniprot_id} not found")

if __name__ == "__main__":
    try:
        uniprot_id = argv[1]
        getFastaFromUniProt(uniprot_id)
    
    except IndexError:
        print("Hey! Please provide uniprot id")
