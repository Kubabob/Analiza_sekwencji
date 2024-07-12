import time
import requests

def readListData(path_to_file):
    with open(path_to_file, 'rt') as f:
        for uniprot_id in f:
            uniprot_id = uniprot_id.strip()

            yield uniprot_id

def readFastaForUniprotId(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"

    resp = requests.get(url)

    return resp.text


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


def getStatus(jobId):
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


if __name__ == "__main__":
    sequences = []

    for uniprot_id in readListData("./data.list"):
        sequences.append(readFastaForUniprotId(uniprot_id))

    sequences_as_str = ''.join(sequences)
    
    jobid = runClustal(sequences_as_str)

    print(f"JOB ID IS: {jobid}")

    max_attempt = 20

    for attept in range(max_attempt):
        status = getStatus(jobid)

        if status == "FINISHED":
            results = getResults(jobid)
            print(results)

            break

        time.sleep(1)       
