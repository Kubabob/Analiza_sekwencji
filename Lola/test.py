import requests
import time

with open('uniprot_id.txt', 'r') as file:
    uniprot_ids = file.read()
    uniprot_ids = uniprot_ids.split('\n')
    print(uniprot_ids)

def getDataFromKegg(operation, argument):
    url = f"https://rest.kegg.jp/{operation}/{argument}"

    resp = requests.get(
        url
    )

    if resp.ok:
        return resp.text

for uniprotid in uniprot_ids:
    ids = getDataFromKegg('conv', f'genes/uniprot:{uniprotid}').split()[1]
    print(f'Your KEGG ID for {uniprotid} is {ids}')
    
def getAminoSeq(uniprotid):
    kegg_id_data = getDataFromKegg(
        "conv", f"genes/uniprot:{uniprotid}"
    )

    kegg_id = kegg_id_data.strip().split("\t")[1]

    gene = getDataFromKegg(
        "get", f"{kegg_id}/aaseq"
    )

    return gene

with open('fastaFromKegg', 'w') as file:
    for uniprotid in uniprot_ids:
        file.write(getAminoSeq(uniprotid))

def runClustal(sequecnes_in_fasta):
    resp = requests.post(
        'https://www.ebi.ac.uk/Tools/services/rest/clustalo/run',
        data={
            "email": "k.klemenska.509@studms.ug.edu.pl",
            "sequence": sequecnes_in_fasta,
            "outfmt": "fa"
        }
    )
    jobid = resp.text

    return jobid


def getIdStatus(jobId):
    url = f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/status/{jobId}"
    
    resp = requests.get(
        url
    )

    return resp.text


def getResults(jobId):
    url = f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/{jobId}/fa"

    resp = requests.get(
        url
    )

    return resp.text

with open('fastaFromKegg', 'r') as file:
    sequencesFromFasta = file.read()

jobid = runClustal(sequencesFromFasta)

print(f"Your job ID is: {jobid}")

max_attempt = 20

for attept in range(max_attempt):
    status = getIdStatus(jobid)

    if status == "FINISHED":
        results = getResults(jobid)
        print(results)

        break

    time.sleep(1)
    
def GapsCount(result: str):
    resultsInLines = result.split('\n')
    countGaps = 0
    for cos in resultsInLines:
        if cos.startswith('>'):
            pass
        else:
            countGaps += cos.count('-')
    return countGaps

print(f'You have {GapsCount(results)} gaps in MSA')