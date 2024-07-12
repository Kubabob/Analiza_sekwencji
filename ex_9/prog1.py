import requests
import numpy as np
import re

def getDataFromNCBI():
    query = "escherichia+coli[orgn]+AND+biomol+mrna[prop]"

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    url += f"esearch.fcgi?db=nucleotide&term={query}&retmax=20&usehistory=y"

    resp = requests.get(url)

    if resp.ok:
        return resp.text
    else:
        return "Error, resp not ok"
    
def getDataFromData(data, searchedValue):
    for i in range(len(data)):
        if data[i:i+len(searchedValue)] == searchedValue:
            return data[i+len(searchedValue)+1:i+len(searchedValue)+3]
        

def getDataFromDataButRe(data, searchedValue):
    returnValue = re.search(f"<{searchedValue}>(.+)</{searchedValue}>", data)
    '''for idx, value in enumerate(returnValue):
        returnValue[idx] = str(value).strip('<')
        returnValue[idx] = str(returnValue[idx]).strip('>')
        returnValue[idx] = str(returnValue[idx]).strip(f'{searchedValue}')
        returnValue[idx] = str(returnValue[idx]).strip('/')
        returnValue[idx] = str(returnValue[idx]).strip('<')
        returnValue[idx] = str(returnValue[idx]).strip('>')'''
    
    #^ dziala ale jest lepszy sposob ;((
    return returnValue.group(1)

def getAllDataFromDataButRe(data, searchedValue):
    returnValue = re.findall(f"<{searchedValue}>(.+)</{searchedValue}>", data)
    return returnValue

def getRecordFromNBCI(query_key, web_env):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    url += f"efetch.fcgi?db=nucleotide&WebEnv={web_env}"
    url += f"&query_key={query_key}&retstart=1&retmax=1"
    url += f"&rettype=gb&retmode=txt"

    resp = requests.get(url)

    return resp.text

def gbToValue(data, query, end):
    new = str(data).split(query)
    if end:
        new2 = new[1].split(end)
        return new2[0]
    else:
        return new[1]

if __name__ == '__main__':
    data = getDataFromNCBI()
    #print(data)
    
    QueryKey = getDataFromDataButRe(data, 'QueryKey')

    #print(QueryKey)

    WebEnv = getDataFromDataButRe(data, "WebEnv")

    #print(WebEnv)

    Id = getAllDataFromDataButRe(data, "Id")

    #print(Id)

    Record1 = getRecordFromNBCI(QueryKey, WebEnv)

    #print(Record1)

    locus = gbToValue(Record1, r'LOCUS', "DEFINITION")

    print(f'> {locus}')

    translation = gbToValue(Record1, 'ORIGIN', end=0)

    #translation = str(translation).split(' ')

    translation = re.findall('\d+ (.+)', translation)

    for idx in range(len(translation)):
        translation[idx] = ''.join(translation[idx].split(' '))
        translation[idx] = str(translation[idx]).upper()


    print(''.join(translation))


    #print(translation)

    #val = gbToValue(Record1, r'/translation=')
    #print(val)

