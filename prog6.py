import re
import requests


def getDataFromNCBI():
    query = "escherichia+coli[orgn]+AND+biomol+mrna[prop]"

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    url += f"esearch.fcgi?db=nucleotide&term={query}&usehistory=y"

    resp = requests.get(url)

    return resp.text


def getQueryKey(ncbiRecord):
    rgx = re.compile('<QueryKey>(.+)</QueryKey>')

    search = re.search(rgx, ncbiRecord)
    query_key = search.group(1)

    return query_key


def getWebEnv(ncbiRecord):
    rgx = re.compile('<WebEnv>(.+)</WebEnv>')

    search = re.search(rgx, ncbiRecord)
    web_env = search.group(1)

    return web_env


def getRecordFromNCBI(query_key, web_env):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    url += f"efetch.fcgi?db=nucleotide&WebEnv={web_env}"
    url += f"&query_key={query_key}&retstart=1&retmax=1"
    url += "&rettype=gb&retmode=txt"

    resp = requests.get(url)

    return resp.text

def getHeader(ncbiData):
    for line in ncbiData.split("\n"):
        if line.startswith("LOCUS"):
            return line


def getSequence(ncbiData):
    sequence = ncbiData.split("ORIGIN")[1]

    sequence_final = ""

    for line in sequence.split("\n"):
        line = line.strip()

        if not line:
            continue

        if line == "//":
            break
        
        data = line.split()[1:]
        data = "".join(data)
        data = data.upper()

        sequence_final += data

    return sequence_final

if __name__ == "__main__":
    ncbiResponse = getDataFromNCBI()

    query_key = getQueryKey(ncbiResponse)
    web_env = getWebEnv(ncbiResponse)

    record = getRecordFromNCBI(query_key, web_env)

    header = getHeader(record)
    sequence = getSequence(record)

    print(f">{header}")
    print(sequence)