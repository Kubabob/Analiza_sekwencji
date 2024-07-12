import requests
import pandas as pd

def getStructureLength(pdb_id):
    url = f"https://files.rcsb.org/view/{pdb_id}.pdb"

    resp = requests.get(
        url
    )

    if resp.ok:
        data = resp.text
        data_as_list = data.split('\n')

        for line in data_as_list:
            if line.startswith('SEQRES'):
                sequence_length = line[13:17]

                return sequence_length.strip()

    return "Error"


def getHelixNumber(pdb_id):
    url = f"https://files.rcsb.org/view/{pdb_id}.pdb"

    resp = requests.get(
        url
    )

    if resp.ok:
        data = resp.text
        data_as_list = data.split('\n')

        helix = 0
        for line in data_as_list:
            if line.startswith('HELIX'):
                helix += 1

        return helix

    return "Error"

def getSheetNumber(pdb_id):
    url = f"https://files.rcsb.org/view/{pdb_id}.pdb"

    resp = requests.get(
        url
    )

    if resp.ok:
        data = resp.text
        data_as_list = data.split('\n')

        sheet = 0
        for line in data_as_list:
            if line.startswith('SHEET'):
                sheet += 1

        return sheet

    return "Error"


def calculateRatio(helix, sheet):
    if sheet == 0:
        return 0
    
    return helix / sheet


if __name__ == "__main__":
    df = pd.read_csv("./input_pdbids")

    df['sequence_length'] = df['pdb id'].apply(
        lambda pdb_id: getStructureLength(pdb_id)
    )

    df['helix'] = df['pdb id'].apply(
        lambda pdb_id: getHelixNumber(pdb_id)
    )

    df['sheet'] = df['pdb id'].apply(
        lambda pdb_id: getSheetNumber(pdb_id)
    )

    df['ratio'] = df[['helix', 'sheet']].apply(
        lambda x: calculateRatio(x[0], x[1]), axis=1
    )



    print(df)
