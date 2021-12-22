# %%
import pandas as pd
import numpy as np
import re

hwd = {'H': 'height', 'W':'width', 'D':'depth', 'L': 'depth'}

df = pd.read_json('./newegg_cases.json')

df = df.drop(['height', 'width', 'depth'], axis=1)

dim_cols = df.columns[df.columns.str.startswith('Dimension')]
result = []
for col in dim_cols:
    order = re.findall(r"\(([HWLD])\s*x\s*([HWLD])\s*x\s*([HWLD])", col)
    if order:
        dim_order = [hwd[i] for i in order[0]]
    else:
        dim_order = ['height', 'width', 'depth']

    regex = re.compile(r"""
    (?P<{0}>[\d\.]+)
    \s*(?P<toss1>\([LWHD]\))?
    \s*"?\s*x\s*
    (?P<{1}>[\d\.]+)
    \s*(?P<toss2>\([LWHD]\))?
    \s*"?\s*x\s*
    (?P<{2}>[\d\.]+)
    \s*(?P<toss3>\([LWHD]\))?
    \s*"?\s*
    (?P<unit>mm|in)?
    """.format(*dim_order), re.VERBOSE)

    extracted = df.loc[df[col].notnull(), col].str.extract(regex)
    extracted = extracted.astype({d: 'float' for d in dim_order})
    extracted = extracted.drop(['toss1', 'toss2', 'toss3'], axis=1, errors='ignore')

    if not extracted.empty:
        result.append(extracted)

result = pd.concat(result, ignore_index=False)

df2 = df.join(result, how='left').drop_duplicates().reset_index(drop=True)

# %%
df2['height'] = df2['height'].mask((df2['unit'] == 'mm'), df2['height'] / 25.4)
df2['width'] = df2['width'].mask((df2['unit'] == 'mm'), df2['width'] / 25.4)
df2['depth'] = df2['depth'].mask((df2['unit'] == 'mm'), df2['depth'] / 25.4)
df2['Max GPU Length'] = df2['Max GPU Length'].str.extract(r"(\d{3})\s*mm").astype("float")
df2['price'] = df2['price'].str.extract(r"([\d\.]+)").astype("float")

df2 = df2.sort_values('price').reset_index(drop=True)


# %%
for url in df2[(df2['width'] <= 8.25) & (df2['Max GPU Length'] >= 323)]['url'].tolist():
    print(url)