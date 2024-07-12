import requests

def getDataFromPDB(pdb_id):
    url = f"https://files.rcsb.org/view/{pdb_id}.pdb"

    resp = requests.get(url)

    if resp.ok:
        return resp.text
    
    return

def writeToFile(pdb_id, data):
    with open(f"./{pdb_id}.pdb", "w") as f:
        f.write(data)


if __name__ == "__main__":
    pdb_id = "1LKX"
    data = getDataFromPDB(pdb_id)
    writeToFile(pdb_id, data)
