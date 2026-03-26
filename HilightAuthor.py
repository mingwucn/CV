import re
import os
import json
import bibtexparser
from pathlib import Path
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding

input_file_1 = "MyPaper.bib"
output_file_1 = "MyPaper_modified.bib"

input_file_2 = "MyConference.bib"
output_file_2 = "MyConference_modified.bib"

input_file_3 = "MyPatent.bib"
output_file_3 = "MyPatent_modified.bib"

input_files = [input_file_1, input_file_2, input_file_3]
json_output = "publications.json"


def remove_abstract(lines):
    in_abstract = False
    for line in lines:
        stripped = line.lstrip().lower()
        if stripped.startswith('abstract'):
            in_abstract = True
            abstract_start = line.find('{') if '{' in line else line.find('"')
            if abstract_start != -1:
                delimiter = '}' if '{' in line else '"'
                end = line.find(delimiter, abstract_start + 1)
                if end != -1:
                    in_abstract = False
            continue
        if in_abstract:
            if '}' in line or '"' in line:  # Check for closing delimiter
                in_abstract = False
            continue
        yield line


def highlight_author(line, target_author="Wu, M", replace="M Wu"):
    if "author" in line:
        # line = re.sub(rf"\b({re.escape(target_author)}}\b", rf"\\hl{{\\textbf{{{replace}}}}}", line)
        line = re.sub(re.escape(target_author), rf"\\hl{{\\textbf{{{replace}}}}}", line)
        # line = re.sub(rf"\b({re.escape(target_author)})\b", rf"\\hl{{\\textbf{{{replace}}}}}", line)
    for pattern, replacement in [("Accept", "\\textbf{Accept}"), ("Under Review", "\\textbf{Under Review}")]:
        line = re.sub(rf"\{{{pattern}\}}", rf"{{{replacement}}}", line)
    return line


def process_file(in_file, out_file, target, replace):
    with open(in_file, 'r', encoding='utf-8') as infile, \
         open(out_file, 'w', encoding='utf-8') as outfile:
        filtered_lines = remove_abstract(infile)
        for line in filtered_lines:
            modified = highlight_author(line, target, replace)
            outfile.write(modified)



def export_json(input_files, json_file):
    all_entries = []
    for file in input_files:
        with open(file, 'r', encoding='utf-8') as f:
            parser = BibTexParser(common_strings=True)
            parser.customization = homogenize_latex_encoding
            db = bibtexparser.load(f, parser=parser)
            for entry in db.entries:
                filtered = {key: entry.get(key, '') for key in [
                    'ID', 'author', 'journal', 'title', 'year', 'abstract', 'comment']}
                all_entries.append(filtered)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_entries, f, indent=2, ensure_ascii=False)

def replace_mu_with_latex(file_path: str) -> None:
    """
    Reads a file and replaces all occurrences of the Unicode character 'μ'
    with the LaTeX command '\\textmu'.

    The file is modified in place. It is assumed to be UTF-8 encoded.

    Args:
        file_path: The absolute or relative path to the target file.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: For other file I/O errors.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file at path '{file_path}' was not found.")

    try:
        # Define the character and its LaTeX replacement
        unicode_char = 'μ'
        latex_command = r'mu'


        # Read the file content with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Perform the replacement
        modified_content = content.replace(unicode_char, latex_command)

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        print(f"Processing complete for: {file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def tag_bib_file(filename, keyword):
    path = Path(filename)
    if not path.exists():
        print(f"File not found: {filename}")
        return

    with path.open(encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    modified_count = 0
    for entry in bib_database.entries:
        entry['keywords'] = keyword  # overwrites or inserts
        modified_count += 1

    with path.open('w', encoding='utf-8') as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)

    print(f"Tagged {modified_count} entries in '{filename}' with keyword='{keyword}'.")

if __name__ == "__main__":

    def highlight_author_multiple(line, replacements):
        for target, replace in replacements:
            line = re.sub(re.escape(target), rf"\\hl{{\\textbf{{{replace}}}}}", line)
        for pattern, replacement in [("Accept", "\\textbf{Accept}"), ("Under Review", "\\textbf{Under Review}")]:
            line = re.sub(rf"\{{{pattern}\}}", rf"{{{replacement}}}", line)
        return line

    def process_file_v2(in_file, out_file, author_replacements):
        with open(in_file, 'r', encoding='utf-8') as infile, \
             open(out_file, 'w', encoding='utf-8') as outfile:
            filtered_lines = remove_abstract(infile)
            for line in filtered_lines:
                modified = highlight_author_multiple(line, author_replacements)
                outfile.write(modified)

    # Define the specific replacements for MyPaper.bib
    mypaper_replacements = [
        ("M. Wu", "M. Wu"),
        ("Wu, M", "M. Wu"),
        ("Wu*, M", "M. Wu*"),
        ("M. Wu*", "M. Wu*"),
    ]
    process_file_v2(input_file_1, output_file_1, mypaper_replacements)


    process_file(input_file_2, output_file_2, "Wu, M", "M, Wu")
    process_file(input_file_3, output_file_3, "Wu, Ming", "M. Wu")
    export_json(input_files, json_output)

    for bib_file_path in [output_file_1, output_file_2, output_file_3]:
        try:
            replace_mu_with_latex(bib_file_path)
        except FileNotFoundError as e:
            print(e)

    patent_bib = Path("MyPatent_modified.bib")
    text = patent_bib.read_text(encoding='utf-8')
    fixed_text = text.replace('@Patent', '@misc')
    patent_bib.write_text(fixed_text, encoding='utf-8')

    tag_bib_file('MyPaper_modified.bib', 'paper')
    tag_bib_file('MyConference_modified.bib', 'conference')
    tag_bib_file('MyPatent_modified.bib', 'patent')