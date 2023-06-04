from scholarly import scholarly, ProxyGenerator

from tqdm import tqdm

from anyascii import anyascii

def fname(s):
    return 'data/'+anyascii(s).replace(' ','_').replace('"','') + '.json'

authors = [
            '"Benjamin F. Maier"',
            'Jonas L. Juul',
            'Sune Lehmann',
            'Laura Alessandretti',
            "Louis Boucherie"',
            'Germans Savcisens',
            '"Anna Sapienza"',
            'Federico Delussu',
            'Josefine Bohr Brask',
            'Peter Edsberg Møllgaard'
            'Kelton Minor',
            'Lasse Mohr Mikkelsen',
            'Silvia De Sojo Caso',
            'Léo Meynent',
        ]


def get_pub_list_by_author(authorname):
    # Retrieve the author's data, fill-in, and print
    # Get an iterator for the author results
    search_query = scholarly.search_author(authorname)

    # Retrieve the first result from the iterator
    first_author_result = next(search_query)
    #scholarly.pprint(first_author_result.encode())

    # Retrieve all the details for the author
    author = scholarly.fill(first_author_result )
    #scholarly.pprint(author.encode())

    pubs = []
    # Take a closer look at the first publication
    for pub in tqdm(author['publications']):
        pub_filled = scholarly.fill(pub)
        pubs.append(pub_filled)

    return pubs




if __name__=="__main__":
    # Set up a ProxyGenerator object to use free proxies
    # This needs to be done only once per session
    #pg = ProxyGenerator()
    #pg.FreeProxies()
    #scholarly.use_proxy(pg)

    from rich import print
    import simplejson as json

    for i, author in enumerate(authors):
        print(i+1,'/',len(authors), author)

        pubs = get_pub_list_by_author(author)

        with open(fname(author),'w') as f:
            json.dump(pubs, f, indent='  ')
