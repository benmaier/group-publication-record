import simplejson as json
from pathlib import Path
from datetime import date

from rich import print

from itertools import groupby

import re
import tldextract

MAX_AUTHOR = 10
USE_TITLE_AS_LINK_TO_PAPER = True


def extract_domain(url):
    extracted = tldextract.extract(url)
    domain = extracted.domain + '.' + extracted.suffix
    return domain



def get_id(pub):
    return pub['title'] + ' ' + ','.join(pub['author'])

files = Path('./clean_data/').glob('*.json')

pubs = []
for file in files:
    with open(file,'r') as f:
        these_pubs = json.load(f)
    pubs.extend(these_pubs)


for pub in pubs:
    #if pub['journal'] is None and pub['conference'] is None and (pub['citation']=='' or pub['citation'] is None):
    #    print(pub)
    if pub['journal'] is None and pub['conference'] is None and (pub['citation']=='' or pub['citation'] is None) and pub['pub_url'] is not None:
        if 'researchsquare' in pub['pub_url']:
            pub['journal'] = 'Research Square'
            pub['citation'] = 'Preprint (Research Square)'
        elif 'scholar.google' not in pub['pub_url']:
            pub['citation'] = extract_domain(pub['pub_url'])
        #print(pub)

pubs = list(filter(lambda p: not (p['conference'] is None and p['journal'] is None and (p['citation']=='' or p['citation'] is None)) and p['pub_year'] is not None, pubs))



# this block for filtering titles that end on preprint
titles = set([ pub['title'] for pub in pubs])
newpubs = []
for pub in pubs:
    title = pub['title']
    if title.endswith('(preprint)') or title.endswith('(Preprint)'):
        if title.endswith('(preprint)'):
            title = title.split('(preprint)')[0]
        if title.endswith('(Preprint)'):
            title = title.split('(Preprint)')[0]
        cleantitle = title.rstrip(' ')
        #print(title, cleantitle)
        if cleantitle not in titles:
            newpubs.append(pub)
    else:
        newpubs.append(pub)

pubs = newpubs
print(len(pubs))
print(len(newpubs))


counted_pubs = set()
newpubs = []
for pub in pubs:
    thisid = get_id(pub)
    if thisid not in counted_pubs:
        newpubs.append(pub)
    counted_pubs.add(thisid)

print("Length of list of publications =",len(pubs))
print("Length of list of unique publications =",len(newpubs))



def construct_entry(pub):

    citation = pub['citation']
    suffix = ', '+str(pub['pub_year'])

    if citation.endswith(suffix):
        citation = citation.split(suffix)[:-1]
        citation = ''.join(citation)

    if 'pub_url' in pub and not USE_TITLE_AS_LINK_TO_PAPER:
        citation = f"[{citation}]({pub['pub_url']})"

    title = pub['title']

    if 'pub_url' in pub and USE_TITLE_AS_LINK_TO_PAPER:
        title_decorator = ""
        title = f"[{title}]({pub['pub_url']})"
    else:
        title_decorator = "**"

    if len(pub['author']) > MAX_AUTHOR:
        pub['author'] = pub['author'][:MAX_AUTHOR-1] + ['...'] + [pub['author'][-1]]

    #The two spaces at the end of the lines are necessary
    #to get Markdown to render a non-paragraph line break
    entry = f"""
- {title_decorator}{title}{title_decorator}  
  {', '.join(pub['author'])}  
  {citation}"""

    if pub['num_citations'] > 0:
        entry += f", cited by: {pub['num_citations']}"

    return entry

def compute_hirsch_index(numbers):
    n = len(numbers)
    numbers.sort(reverse=True)  # Sort the list in descending order

    h_index = 0
    for i in range(n):
        if numbers[i] >= i + 1:
            h_index = i + 1
        else:
            break

    return h_index

newpubs = sorted(newpubs,key=lambda pub: -pub['pub_year'])

citations = [ pub['num_citations'] for pub in newpubs]
hindex = compute_hirsch_index(citations)
print(f"{hindex=}")
print(f"{sum(citations)=}")

title_abstract_file = ""


markdown_header_start_level = '###'
md = markdown_header_start_level + " Publications\n\n"
md += f"This is a combined list of publications that we authored or co-authored. If you're into numbers like that, our work has accumulated {sum(citations)} citations with an h-index of {hindex} over the years (as of {date.today()}, data by Google Scholar).\n\n"

for year, group in groupby(newpubs, lambda pub: pub['pub_year']):

    md +=  markdown_header_start_level + "# " + str(year) + '\n\n'
    group = list(group)
    group = sorted(group, key=lambda x: -x['num_citations'])

    entry = ""
    for pub in group:
        entry += construct_entry(pub)
    entry += "\n\n"

    md += entry


with open('output/publications.md','w') as f:
    f.write(md)

