import re
import requests

def getResposneFromNCBI(url):
    resp = requests.get(url)

    return resp.text

def getDataFromXML(xml_data):
    rgx_count    = re.compile('<Count>(.*)</Count>')
    rgx_webenv   = re.compile('<WebEnv>(.*)</WebEnv>')
    rgx_querykey = re.compile('<QueryKey>(.*)</QueryKey>')

    count_search    = re.search(rgx_count, xml_data)
    webenv_search   = re.search(rgx_webenv,xml_data)
    querykey_search = re.search(rgx_querykey, xml_data)

    count_value = count_search.group(1)
    webenv_value = webenv_search.group(1)
    querykey_value = querykey_search.group(1)

    return count_value, webenv_value, querykey_value


def getRecordFromNCBI(webenv, querykey):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    url = url + f"efetch.fcgi?db=nucleotide&WebEnv={webenv}"
    url = url + f"&query_key={querykey}&retstart=1"
    url = url + "&retmax=1&rettype=gb&retmode=text"

    resp = requests.get(url)

    return resp.text

def makeFastaFromGB(gb_data):
    fasta = ""
    
    header = ""
    sequence = ""

    for line in gb_data.split("\n"):
        if line.startswith("LOCUS"):
            header = line

            break

    fasta += f">{header}\n"

    sequence = gb_data.split("ORIGIN")[1]
    sequence = sequence.strip().rstrip("//")

    for s in sequence.split("\n"):
        s = s.strip()
        s = s.split()

        s = "".join(s[1:])
        s = s.upper()

        fasta += f"{s}\n"

    return fasta

if __name__ == "__main__":
    query = "escherichia+coli[orgn]+AND+biomol+mrna[prop]"

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    url = url + f"esearch.fcgi?db=nucleotide&term={query}"
    url = url + "&usehistory=y"

    response = getResposneFromNCBI(url)
    count_value, webenv_value, querykey_value = getDataFromXML(response)

    data = getRecordFromNCBI(webenv_value, querykey_value)
    fasta = makeFastaFromGB(data)

    print(fasta)