import requests
import pandas as pd


def getDataFromKegg(operation, argument):
    url = f"https://rest.kegg.jp/{operation}/{argument}"

    resp = requests.get(
        url
    )

    if resp.ok:
        return resp.text
    
def getNuclSeq(uniprot_id):
    kegg_id_data = getDataFromKegg(
        "conv", f"genes/uniprot:{uniprot_id}"
    )

    kegg_id = kegg_id_data.strip().split("\t")[1]

    gene = getDataFromKegg(
        "get", f"{kegg_id}/ntseq"
    )

    gene = "".join(gene.split("\n")[1:])

    return gene

def getGC(sequence):
    g_content = sequence.count("g")
    c_content = sequence.count("c")

    gc_content = g_content + c_content
    gc_content_perc = gc_content / len(sequence)

    return gc_content_perc

if __name__ == "__main__":
    df = pd.read_csv("./input_data")

    df['nt_seq'] = df['uniprot_id'].apply(
        lambda x: getNuclSeq(x)
    )

    df['nt_seq_len'] = df['nt_seq'].apply(
        lambda x: len(x)
    )

    df['gc_content'] = df['nt_seq'].apply(
        lambda x: getGC(x)
    )

    print(df)