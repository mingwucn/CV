import sys
sys.path.insert(0, '.')
from backend import Paper, update_bib_files

# Create a dummy paper list with a known title
papers = [
    Paper(
        title="Fabrication of surface microstructures by mask electrolyte jet machining",
        year=2020,
        authors="Wu, M and Liu, J and He, J and Chen, X and Guo*, Z",
        role="first",
        citations=999,  # new citation count
        num_authors=5,
        source_file="MyPaper.bib"
    )
]

print("Updating .bib file...")
update_bib_files(papers)
print("Check MyPaper.bib for citationthisyear = {999}")
