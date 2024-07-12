import requests
import pandas as pd

def makeKeggID(uniprot_id):
    url = f"https://rest.kegg.jp/conv/genes/uniprot:{uniprot_id}"

    resp = requests.get(
        url
    )

    if not resp.ok:
        return "ERROR"
    
    return resp.text.strip("\n").split("\t")[1]

def getGeneSequence(kegg_id):
    url = f"https://rest.kegg.jp/get/{kegg_id}/ntseq"

    resp = requests.get(
        url
    )

    if not resp.ok:
        return "ERROR"

    return ''.join(resp.text.split("\n")[1:])


def getGCContent(gene):
    g_count = gene.count("g")
    c_count = gene.count("c")

    gene_length = len(gene)

    gc_content = (g_count + c_count) / gene_length

    return round(gc_content*100, 2)

def getGCContentUgly(gene):
    return round(((gene.count("g")+gene.count("c"))/len(gene))*100 ,2)


df = pd.read_csv("./data")

df['kegg_id'] = df['uniprot_id'].apply(
    lambda uniprot_id: makeKeggID(uniprot_id)
)

df['gene_sequence'] = df['kegg_id'].apply(
    lambda kegg_id: getGeneSequence(kegg_id)
)

df['gene_length'] = df['gene_sequence'].apply(
    lambda gene: len(gene)
)

df['gc_content'] = df['gene_sequence'].apply(
    lambda gene: getGCContentUgly
    (gene)
)



print(df)