import re
import requests


def getDataFromNCBI():
    query = "escherichia+coli[orgn]+AND+biomol+mrna[prop]"

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    url += f"esearch.fcgi?db=nucleotide&term={query}&usehistory=y"

    resp = requests.get(url)

    return resp.text


def getQueryKey(ncbiResp):
    rgx = re.compile('<QueryKey>(.+)</QueryKey>')
    search = re.search(rgx, ncbiResp)

    query_key = search.group(1)

    return query_key

def getWebEnv(ncbiResp):
    rgx = re.compile('<WebEnv>(.+)</WebEnv>')
    search = re.search(rgx, ncbiResp)

    web_env = search.group(1)

    return web_env


def getRecordFromNCBI(query_key, web_env):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    url += f"efetch.fcgi?db=nucleotide&WebEnv={web_env}"
    url += f"&query_key={query_key}&retstart=1&retmax=1"
    url += f"&rettype=gb&retmode=text"

    resp = requests.get(url)

    return resp.text

def getHeader(record):
    for line in record.split("\n"):
        if line.startswith("LOCUS"):
            return line


def getSequence(record):
    sequence = record.split("ORIGIN")[1]

    final_sequence = ""

    for line in sequence.split("\n"):
        line = line.strip()
        
        if not line:
            continue
        
        if line == "//":
            break
        
        data = line.split()[1:]
        data = "".join(data)
        data = data.upper()

        final_sequence += data


    return final_sequence


if __name__ == "__main__":
    ncbiResp = getDataFromNCBI()

    query_key = getQueryKey(ncbiResp)
    web_env = getWebEnv(ncbiResp)

    record = getRecordFromNCBI(query_key, web_env)
    
    header = getHeader(record)
    sequence = getSequence(record)
    
    print(
        f">{header}",
        sequence,
        sep="\n"
    )