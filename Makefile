
default: processdata md

prep:
	mkdir -p data
	mkdir -p cleaned_data
	mkdir -p output

scrape:
	python build_publication_list.py

processdata:
	python process_data.py

md:
	python make_md.py

all: prep scrape processdata md

cleandownloads:
	rm data/*.json

cleanprocessed:
	rm cleandata/*.json

chatgpt:
	python chatgpt_prompts_for_summary.py output/titles_and_abstracts.json
