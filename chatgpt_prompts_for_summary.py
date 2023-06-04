import sys
import subprocess
import math

chunksize = 15000

if len(sys.argv) == 1:
    sys.stderr.write('No file given!')
    sys.exit(1)
if len(sys.argv) == 2:
    fn = sys.argv[1]
if len(sys.argv) > 2:
    fn = sys.argv[1]
    chunksize = int(sys.argv[2])

with open(fn,'r') as f:
    all_text = f.read()

    total_chunks = int(math.ceil(len(all_text)/chunksize))
    count = 0

    first_message = f"""I'm going to send you a long JSON file in {total_chunks} parts. Note that for each part, the end may be cut off. Please treat the parts as if they were one large file. The files contain abstracts and titles of research papers that have been written by a research group. After I send you the last part, please write a three-paragraph summary of what this group research is focused on."""
    subprocess.run("pbcopy", text=True, input=first_message)
    input(f"Copied 1st initial prompt to the clipboard, press enter to copy next part")

    for idx in range(0, len(all_text), chunksize):
        count += 1
        this_text = all_text[idx:idx+chunksize]
        subprocess.run("pbcopy", text=True, input=f"Here's part {count}/{total_chunks} of the file, note that it might cut off at the end. Don't generate an elaborate response, just acknowledge that you received this part of the file.\n\n"+this_text)
        input(f"Copied Part {count}/{total_chunks} to clipboard, press enter to copy next part")

    last_message = """Now you have the whole JSON file. The file contains abstracts and titles of research papers that have been written by a research group. Please write a three-paragraph summary of what this group's research is focused on."""
    subprocess.run("pbcopy", text=True, input=first_message)
    input(f"Copied final prompt to clipboard, exiting now...")
