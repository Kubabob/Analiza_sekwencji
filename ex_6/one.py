import requests as rq
import pandas as pd


def get_from_kegg(operation, *args):
    url = f'https://rest.kegg.jp/{operation}'
    for idx, arg in enumerate(args):
        if idx == 0:
            url += f'/{arg}'
        else:
            url += f'[/{arg}'
    else:
        url += f'{(len(args)-1)*"]"}'
    resp = rq.get(url)

    return resp.text

def get_nucl_seq(uniprot_id):
    kegg_id = get_from_kegg(
        'conv',
        f'genes/uniprot:{uniprot_id}'
    )

    kegg_id = kegg_id.split('\t')[1].strip('\n')

    nt_seq = get_from_kegg(
        'get',
        f'{kegg_id}/ntseq'
    )

    return nt_seq


def gc_content(nt_seq):
    amount = 0
    for item in nt_seq:
        if str(item).capitalize() == 'G' or str(item).capitalize() == 'C':
            amount += 1
    else:
        return amount/len(nt_seq)

if __name__ == '__main__':
    df = pd.read_csv('input_data')

    df['nt_seq'] = df['uniprot_id'].apply(
        lambda x: get_nucl_seq(x)
    )

    df['nt_seq_len'] = df['nt_seq'].apply(
        lambda x: len(x)
    )

    df['gc_content'] = df['nt_seq'].apply(
        lambda x: gc_content(x)
    )

    print(df)
