import sys
sys.path.insert(0, '.')
from backend import Paper, update_bib_files

papers = [
    Paper(
        title="Fabrication of surface microstructures by mask electrolyte jet machining",
        year=2020,
        authors="Wu, M and Liu, J and He, J and Chen, X and Guo*, Z",
        role="first",
        citations=3,  # original value
        num_authors=5,
        source_file="MyPaper.bib"
    )
]

update_bib_files(papers)
print("Reverted to citation = 3")
