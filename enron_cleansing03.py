import pandas as pd
import re

df = pd.read_csv('/home/mhmmd/Documents/emails.csv')
df.drop(columns=['file'], inplace=True)


def prepare(in_text: str):
    txt = in_text.split('\n')
    txt = [i.strip() for i in txt if len(i) > 0]

    out = []
    index = None

    for i in txt:
        if (i[:3] == 'To:') and (i[-4:] == '.com'):
            out.append(i)
        elif (i[:5] == 'From:') and (i[-9:] == 'enron.com'):
            out.append(i)
        elif i[:11] == 'X-FileName:':
            index = txt.index(i)
    if index:
        txt = txt[index + 1:]
        txt = '\n'.join(txt)
        txt = re.sub(r'\s\s', ' ', txt)
        out.append(txt)
    return out


data = pd.DataFrame()
data['raw'] = df['message'].apply(lambda x: prepare(x))
data['len'] = data['raw'].apply(lambda x: len(x))
data['targets'] = data['raw'].apply(lambda x: [i for i in x if i[:3] == 'To:'])
data['sources'] = data['raw'].apply(lambda x: [i for i in x if i[:5] == 'From:'])
data['message'] = data['raw'].apply(lambda x: [i for i in x if ((i[:3] != 'To:') & (i[:5] != 'From:'))])
data['len_tar'] = data['targets'].apply(lambda x: len(x))
data['len_src'] = data['sources'].apply(lambda x: len(x))
data = data[data['len_tar'] != 0]
data = data[data['len_src'] != 0]
data['message'] = data['message'].apply(lambda x: str(x[0]) if len(x) > 0 else x)
data.reset_index(inplace=True)
data.drop(columns=['index'], inplace=True)
data = data.explode('targets')
data = data.explode('sources')

data.reset_index(inplace=True)
data.drop(columns=['index', 'len_tar', 'len_src', 'len'], inplace=True)

data.to_csv('enron_edge_list_00.csv')