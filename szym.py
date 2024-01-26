import re
import requests
import json
from sys import argv, exit

def getMSAresults(x):

    resp = requests.post('https://www.ebi.ec.uk/Tools/services/rest/clustalo/run',
                         data = {
                             'email': 'marcel.thiel@ug.edu.pl',
                             'sequence': x,
                             'outfmt': 'fa'
                         })
    jobid = resp.text

    url = f'https://www.ebi.ec.uk/Tools/services/rest/clustalo/status/{jobid}'
    status = requests.get(url)

    return status.text


def keggStrip(keggID):
    keggIDret = ''
    for i in range(len(keggID)):
        if keggID[i] != ';':
            keggIDret += keggID[i]
        else:
            return keggIDret
    return 0

def getSeq(uniprotID):
    url = f'https://www.ebi.ac.uk/proteins/api/proteins/{uniprotID}'
    resp = requests.get(
        url,
        headers={'Accept': 'application/json'}
    )

    if resp.ok:
        data = json.loads(resp.text)
        return data['sequence']['sequence']

def zadanie1():
    path = 'file.txt'
    with open(path, 'w') as f:
        f.write('P10321\nP04439\nP01889\nP17693\nP13747')

    with open(path, 'r') as f:
        file = f.readlines()
        data = [uniprotID.rstrip('\n') for uniprotID in file]

    print(data)

    for idx in range(len(data)):
        uniprotID = data[idx]
        url = f'https://rest.uniprot.org/uniprotkb/{uniprotID}.txt'

        resp = requests.get(url)

        if resp.ok:
            txtData = resp.text
            for line in txtData.split('\n'):
                if line[5:9] == 'KEGG':
                    keggIDtemp = line[15:]
                    keggID = keggStrip(keggIDtemp)
                    data[idx] = [uniprotID, keggID]

    # data => [uniprotID, keggID]
    print(data)

    fastaSeqs = ''
    for i in range(len(data)):
        fastaSeqs += f'>uniprotID: {data[i][0]}\n{getSeq(data[i][0])}\n'
    with open('fastaFiles.txt', 'w') as file:
        file.write(fastaSeqs)


def main():
    zadanie1()
    with open('fastaFiles.txt', 'r') as f:
        file = f.read()
        print(file)
        '''for i in range(len(f)):
            getMSAresults(f)'''

if __name__ == '__main__':
    main()
