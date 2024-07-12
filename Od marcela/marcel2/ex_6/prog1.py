import requests
import pandas as pd


def getDataFromKegg(operation, argument):
    resp = requests.get(
        f"https://rest.kegg.jp/{operation}/{argument}"
    )

    if resp.ok:
        return resp.text

# conv , genes/uniprot:P12345
def getGeneLength(uniprot_id):
    kegg_id_data = getDataFromKegg(
        "conv",
        f"genes/uniprot:{uniprot_id}"
    )

    kegg_id = kegg_id_data.strip().split("\t")[1]

    sequence_data = getDataFromKegg(
        "get", f"{kegg_id}/ntseq"
    )

    sequence = "".join(
        sequence_data.split("\n")[1:]
    )

    return len(sequence)

def getGC(uniprot_id):
    kegg_id_data = getDataFromKegg(
        "conv",
        f"genes/uniprot:{uniprot_id}"
    )

    kegg_id = kegg_id_data.strip().split("\t")[1]

    sequence_data = getDataFromKegg(
        "get", f"{kegg_id}/ntseq"
    )

    sequence = "".join(
        sequence_data.split("\n")[1:]
    )

    sequence_length = len(sequence)

    g_count = sequence.count("g")
    c_count = sequence.count("c")

    return (g_count + c_count) / sequence_length


if __name__ == "__main__":
    df = pd.read_csv("./input_data")
    
    df['gene_lenght'] = df['uniprot_id'].apply(
        lambda x: getGeneLength(x)
    )

    df['gc_content'] = df['uniprot_id'].apply(
        lambda x: getGC(x)
    )

    print(df)