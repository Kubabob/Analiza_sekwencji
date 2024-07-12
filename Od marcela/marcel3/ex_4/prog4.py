import requests
import pandas as pd

def getSequenceLength(pdb_id):
    # 1. GET DATA FROM PDB BASED ON PDB_ID
    # 2. FIND SEQURES LINE
    # 3. GET LENGTH OF THE STRUCTURE
    
    url = f"https://files.rcsb.org/view/{pdb_id}.pdb"

    resp = requests.get(url)

    if resp.ok:
        data = resp.text
        data_as_list = data.split("\n")

        chains = {}

        for line in data_as_list:
            if line.startswith("SEQRES"):
                chain = line[11]
                length = line[13:17]

                chains[chain] = int(length)

        count = 0
        for _, lenght in chains.items():
            count += lenght

        return count

    return "Error"


if __name__ == "__main__":
    df = pd.read_csv("./input_data")

    df['sequence_length'] = df['pdb_id'].apply(
        lambda x: getSequenceLength(x)
    )

    print(df)
