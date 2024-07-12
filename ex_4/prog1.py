import requests
def getDataFromPDB(pdb_id):
    url = f'https://files.rcsb.org/view/{pdb_id}.pdb'
    resp = requests.get(
        url    
    )
    return resp.text

if __name__ == '__main__':
    pdb_id = '1LKX'
    data = getDataFromPDB(pdb_id)

    with open(f'{pdb_id}.pdb', 'w') as file:
        file.write(data)
    print(f'File {pdb_id}.pdb is ready to open.')
