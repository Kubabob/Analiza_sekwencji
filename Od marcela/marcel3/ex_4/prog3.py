import requests

def getDataFromPDB(pdb_id):
    url = f"https://files.rcsb.org/view/{pdb_id}.pdb"

    resp = requests.get(url)

    if resp.ok:
        return resp.text
    
    return False

def writeDataToFile(pdb_id, data):
    with open(f"{pdb_id}.pdb", 'w') as f:
        f.write(data)


if __name__ == "__main__":
    pdb_id = '3RGK'
    data = getDataFromPDB(pdb_id)

    writeDataToFile(pdb_id, data)