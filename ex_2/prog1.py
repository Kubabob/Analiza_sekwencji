#1.1

'''from sys import argv
import requests


def download_uniprot(id):
    url = f'https://rest.uniprot.org/uniprotkb/{id}.fasta'
    print(requests.get(url).text)


if __name__ == '__main__':
    try:
        download_uniprot(argv[1])
    except IndexError:
        print('Ty pacanie')'''

#1.2

'''
from sys import argv
import requests
import json


def download_uniprot(id):
    url = f"https://www.ebi.ac.uk/proteins/api/proteins/{id}"
    resp = requests.get(
        url,
        headers= {"Accept": "application/json"}
    )

    if resp.ok:
        ret_json = json.loads(resp.text)
        return ret_json

    print(f'Uniprot id {id} does not exist')


if __name__ == '__main__':
    try:
        data = download_uniprot(argv[1])
        print(data.keys())
        print(data['organism']['names'][0]['value'])
        print(data['gene'][0]['name']['value'])
        print(data['sequence']['sequence'])
    except IndexError:
        print('Ty pacanie')
'''