# Generate research group publication list

Contains scripts that scrape a collection of researchers' publication output and build summaries.

## Install and usage

    pip install -r requirements.txt
    make prep
    make scrape
    make

The output will be two json files in `output`.

## Fine tuning

In the script `build_publication_list.py`, you can change the list of authors that
should be scraped. It may happen that your IP is blocked for bot usage. In that
case you need to manually adjust the author list, change IPs and restart the process.

## ChatGPT

You can ask ChatGPT to write a summary of the collective research. To that
end you need to feed titles and abstracts to it in chunks. Get the prompts
copied to your clibpoard one by one with

    make chatgpt


