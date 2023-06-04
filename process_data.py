import simplejson as json
from pathlib import Path
from tqdm import tqdm

from rich import print

relevant_keys_bib = [
      "title",
      "pub_year",
      "citation",
      "author",
      "journal",
      "volume",
      "number",
      "pages",
      "conference",
    ]
relevant_keys_other = [
    "num_citations",
    "pub_url",
    ]

files = Path('./data/').glob('*.json')

title_abstract_set = set()

for file in files:
    with open(file,'r') as f:
        pubs = json.load(f)

    new_pubs = []
    for pub in tqdm(pubs):
        this_pub = {}
        for key in relevant_keys_bib:
            this_pub[key] = pub['bib'][key] if key in pub['bib'] else None
        this_pub['author'] = this_pub['author'].split(' and ')

        for key in relevant_keys_other:
            this_pub[key] = pub[key] if key in pub else None

        new_pubs.append(this_pub)

        bib = pub['bib']
        if 'title' in bib and 'abstract' in bib:
            title_abstract_set.add((bib['title'], bib['abstract']))

    fn = str(file).split('data/')[1]
    with open('clean_data/'+fn,'w') as f:
        json.dump(new_pubs, f, indent='  ')

with open('output/titles_and_abstracts.json','w') as f:
    d = [ {'title':title, 'abstract':abstract} for title, abstract in title_abstract_set ]
    json.dump(d, f, indent='  ')
