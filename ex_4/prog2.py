import requests
import pandas as pd
import time

def getDataFromPDB(pdb_id):
    url = f'https://files.rcsb.org/view/{pdb_id}.pdb'
    resp = requests.get(
        url    
    )
    return resp.text



def getSequenceLength(pdb_id):
    length = 0
    chains = {}
    try:
        with open(f'pdb_files/{pdb_id}.pdb', 'r') as f:
            for line in f:
                if line.startswith('SEQRES'):
                    line = line.split()
                    if line[2] not in chains.keys():
                        chains[line[2]] = int(line[3])
                        length += int(line[3])

    except:
        data = getDataFromPDB(pdb_id)
        data = data.split('\n')
        for line in data:
            if line.startswith('SEQRES'):
                line = line.split()
                if line[2] not in chains.keys():
                    chains[line[2]] = int(line[3])
                    length += int(line[3])


    return length


def getHelixNumber(pdb_id):
    count = 0
    try:
        with open(f'pdb_files/{pdb_id}.pdb', 'r') as f:
            for line in f:
                if line.startswith('HELIX'):
                    count += 1
    except:
        data = getDataFromPDB(pdb_id)
        data = data.split('\n')
        for line in data:
                if line.startswith('HELIX'):
                    count += 1
    return count


if __name__ == '__main__':
    df = pd.read_csv('input_data')

    #pdb_id = '1LKX'

    df['sequence_length'] = df['pdb_id'].apply(
        lambda x: getSequenceLength(x)
    )

    df['helix_number'] = df['pdb_id'].apply(
        lambda x: getHelixNumber(x)
    )

    print(df)
