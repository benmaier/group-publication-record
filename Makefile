
prep:
	mkdir data
	mkdir cleaned_data

scrape:
	python build_publication_list.py

processdata:
	python process_data.py

md:
	python make_md

all:
	prep
	scrape
	processdata
	md

default:
	processdata
	md

cleandownloads:
	rm data/*.json

cleanprocessed:
	rm cleandata/*.json

chatgpt:
	python chatgpt_prompts_for_summary.py output/titles_and_abstracts.json
