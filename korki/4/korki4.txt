#1. z pliku uniprot_id wypisz wszystkie id. Przekonwertuj je do keggID.

#2. wykonaj MSA dla podanych sekwencji. Zapisz odpowiedz w formacie fasta do pliku MSA_analysis

#3. Przefiltruj sekwencje. Wypisz te ktore posiadaja w nazwie HLA.
import requests
import time
with open("uniprot_id", "r") as f:
    uniprotids = f.read().split("\n")  
    for uniprotid in uniprotids:
        print(uniprotid)
    

def fromunitokegg(uniprotid):
    
    url = f"https://rest.kegg.jp/conv/genes/uniprot:{uniprotid}"
    response = requests.get(url).text
    
    return(response)
for uniprotid in uniprotids:    
    print(fromunitokegg(uniprotid))
def getfastafromuniprot(uniprotid):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprotid}.fasta"
    respo = requests.get(url).text
    
    return respo

seq = []

for uniprotid in uniprotids:
    sekwencjefast = getfastafromuniprot(uniprotid)
    seq.append(getfastafromuniprot(uniprotid))
sequences_as_str = ''.join(seq)
"""
def runClustal(sequecnes_in_fasta):
    resp = requests.post(
        'https://www.ebi.ac.uk/Tools/services/rest/clustalo/run',
        data={
            "email": "marcel.thiel@ug.edu.pl",
            "sequence": sequecnes_in_fasta,
            "outfmt": "fa"
        }
    )
    jobid = resp.text

    return jobid
print(runClustal(sequences_as_str))

def getStatus(jobId):
    url = f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/status/{jobId}"
    
    resp = requests.get(
        url
    )

    return resp.text
jobid = runClustal(sequences_as_str)

print(f"JOB ID IS: {jobid}")


def getResults(jobId):
    url = f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/{jobId}/fa"

    resp = requests.get(
        url
    )

    return resp.text
''max_attempt = 20

for attept in range(max_attempt):
    status = getStatus(jobid)

    if status == "FINISHED":
        results = getResults(jobid)
        print(results)

        break
    
    time.sleep(1)       
with open("MSA.fasta","w") as g:
    g.write(results)
with open("MSA.fasta","r") as h:
    MSAwynik = h.readlines()
    print(MSAwynik)''"""
for x in seq:
    if "HLA" in x:
        print(x)




