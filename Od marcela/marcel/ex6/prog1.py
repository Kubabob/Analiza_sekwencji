import requests

def getDataFromKegg(operation, argument):
    url = f"https://rest.kegg.jp/{operation}/{argument}"

    resp = requests.get(
        url
    )

    if not resp.ok:
        return False
    
    return resp.text

if __name__ == "__main__":
    kegg_info = getDataFromKegg("conv", "genes/uniprot:P12345")

    print(kegg_info)
