import re
import numpy as np
import os

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
# List all variations of your name as they might appear in the bib file.
# The script will check if ANY of these match an author in the entry.
TARGET_ALIASES = ["Wu, M", "M. Wu", "Wu, M.", "Wu, M*", "M. Wu*", "Ming Wu"]
FILENAME = ["MyPaper.bib", "MyConference.bib"]
PREDICT = True

# The specific field in your bib file containing the citation count for the target year
CITATION_FIELD = "citationthisyear"
THRESHOLD = 2.0000 # Minimum from dataset
SCENARIOS = [5, 10, 20, 50, 100] # Avg Citations
TeamSize = 7

COEFFS = {
    "NC": 0.08810111,
    "H": 0.21621749,
    "Hm": 0.25977242,
    "NCS": 0.10252264,
    "NCSF": 0.09185340,
    "NCSFL": 0.09075539,
}


# -----------------------------------------------------------------------------
# 1. METRIC CALCULATIONS
# -----------------------------------------------------------------------------
def calculate_engineering_c_score(papers):
    nc_total = 0
    ncs_total = 0
    ncsf_total = 0
    ncsfl_total = 0
    
    citations_list = []
    fractional_citations_list = []
    
    # List to store per-paper metrics for reporting
    paper_reports = []

    for p in papers:
        cites = p['citations']
        n_auth = p['num_authors']
        role = p['role'] 
        title = p['title']
        
        # --- Metrics Accumulation ---
        nc_total += cites
        citations_list.append(cites)
        
        if n_auth > 0:
            fractional_citations_list.append(cites / n_auth)
        else:
            fractional_citations_list.append(0)

        # Apply Nested Authorship Logic
        is_single = (role == 'single')
        is_first = (role == 'first')
        is_last = (role == 'last')

        # Calculate contributions for this specific paper
        p_ncs = cites if is_single else 0
        p_ncsf = cites if (is_single or is_first) else 0
        p_ncsfl = cites if (is_single or is_first or is_last) else 0

        # Update totals
        ncs_total += p_ncs
        ncsf_total += p_ncsf
        ncsfl_total += p_ncsfl
        
        # Store for report
        paper_reports.append({
            'title': title,
            'NCS': p_ncs,
            'NCSF': p_ncsf,
            'NCSFL': p_ncsfl,
            'cites': cites # stored for sorting
        })

    # --- Index Calculations ---
    citations_list.sort(reverse=True)
    h_index = max([i + 1 for i, c in enumerate(citations_list) if c >= i + 1], default=0)
            
    fractional_citations_list.sort(reverse=True)
    hm_index = max([i + 1 for i, c in enumerate(fractional_citations_list) if c >= i + 1], default=0)

    # --- Final Log-Transformed Sum ---
    score = (
        COEFFS['NC'] * np.log(nc_total + 1) +
        COEFFS['H'] * np.log(h_index + 1) +
        COEFFS['Hm'] * np.log(hm_index + 1) +
        COEFFS['NCS'] * np.log(ncs_total + 1) +
        COEFFS['NCSF'] * np.log(ncsf_total + 1) +
        COEFFS['NCSFL'] * np.log(ncsfl_total + 1)
    )

    return score, {
        "NC": nc_total, "H": h_index, "Hm": hm_index,
        "NCS": ncs_total, "NCSF": ncsf_total, "NCSFL": ncsfl_total
    }, paper_reports


# -----------------------------------------------------------------------------
# 2. HELPER: NAME NORMALIZATION
# -----------------------------------------------------------------------------
def normalize_name(name):
    """
    Standardizes author names: removes asterisks, periods, and sets to lowercase.
    """
    return name.replace("*", "").replace(".", "").lower().strip()


# -----------------------------------------------------------------------------
# 3. BIB PARSING LOGIC
# -----------------------------------------------------------------------------
def parse_bib_file(filepath, aliases, citation_key):
    papers = []
    target_aliases_clean = set(normalize_name(a) for a in aliases)
    
    field_pattern = re.compile(r'(\w+)\s*=\s*[\{"](.*?)(?<!\\)[\}"]', re.DOTALL | re.IGNORECASE)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        entries = re.split(r'@\w+\s*\{', content)
        
        for entry in entries:
            if not entry.strip(): continue
            
            fields = {}
            for match in field_pattern.finditer(entry):
                key = match.group(1).lower()
                val = match.group(2).replace('\n', ' ').strip()
                fields[key] = val
            
            if 'author' in fields:
                # 1. Get Title (Default to 'Unknown' if missing)
                title = fields.get('title', 'Unknown Title')
                # Clean title: remove newlines and extra spaces
                title = " ".join(title.split())
                
                # 2. Get Citations
                cites = 0
                if citation_key.lower() in fields:
                    try:
                        cites = int(fields[citation_key.lower()])
                    except ValueError:
                        cites = 0 
                
                # 3. Parse Authors
                raw_authors = fields['author']
                author_list = [a.strip() for a in re.split(r'\s+and\s+', raw_authors, flags=re.IGNORECASE)]
                num_authors = len(author_list)
                
                # 4. Find Author Position
                match_index = -1
                for idx, author_in_paper in enumerate(author_list):
                    clean_paper_author = normalize_name(author_in_paper)
                    if clean_paper_author in target_aliases_clean:
                        match_index = idx
                        break
                
                if match_index == -1:
                    continue 

                # 5. Determine Role
                if num_authors == 1:
                    role = 'single'
                elif match_index == 0:
                    role = 'first'
                elif match_index == num_authors - 1:
                    role = 'last'
                else:
                    role = 'middle'
                
                papers.append({
                    'title': title,
                    'citations': cites,
                    'num_authors': num_authors,
                    'role': role
                })
                
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return []
    except Exception as e:
        print(f"Parsing error: {e}")
        return []

    return papers


def predict_papers_needed(target_score=1.90, citations_per_paper=10, num_authors=4):
    """
    Calculates the number of First Author papers needed to meet a target C-score.
    
    Args:
        target_score (float): The C-score threshold (approx 1.90 for Engineering).
        citations_per_paper (int): Hypothetical citations each new paper receives.
        num_authors (int): Total authors on the paper (affects Hm-index).
        
    Returns:
        int: Number of papers required.
    """
    
    # Iterate to find minimum N papers
    for n in range(1, 1000):
        # Calculate Metrics for N papers
        nc = n * citations_per_paper
        
        # H-index: capped by number of papers or citation count
        h = min(n, citations_per_paper)
        
        # Hm-index (Schreiber): 
        # With identical papers, Hm is determined by fractional citation (Cites/Authors)
        # It is capped by N or floor(Cites/Authors)
        frac_cites = citations_per_paper / num_authors
        hm = min(n, int(frac_cites))
        
        # Authorship Categories (First Author)
        ncs = 0                # Not Single Author
        ncsf = nc              # Is First Author (Counted)
        ncsfl = nc             # Is First/Last (Counted)
        
        # Calculate Composite Score
        score = (
            COEFFS['NC'] * np.log(nc + 1) +
            COEFFS['H'] * np.log(h + 1) +
            COEFFS['Hm'] * np.log(hm + 1) +
            COEFFS['NCS'] * np.log(ncs + 1) +
            COEFFS['NCSF'] * np.log(ncsf + 1) +
            COEFFS['NCSFL'] * np.log(ncsfl + 1)
        )
        
        if score >= target_score:
            return n
            
    return -1 # Not reachable within 1000 papers

def predict_single_author_papers(target_score=1.90, citations_per_paper=10):
    """
    Calculates number of SINGLE AUTHOR papers needed to meet a target C-score.
    
    Args:
        target_score (float): The C-score threshold (approx 1.90 for Engineering).
        citations_per_paper (int): Hypothetical citations each new paper receives.
        
    Returns:
        int: Number of papers required.
    """
    
    for n in range(1, 1000):
        # 1. Total Citations
        nc = n * citations_per_paper
        
        # 2. H-index & Hm-index
        # For single author, fractional cites = raw cites, so Hm == H
        h = min(n, citations_per_paper)
        hm = h 
        
        # 3. Authorship Categories
        # Single author papers contribute to ALL categories
        ncs = nc
        ncsf = nc
        ncsfl = nc
        
        # Calculate Composite Score
        score = (
            COEFFS['NC'] * np.log(nc + 1) +
            COEFFS['H'] * np.log(h + 1) +
            COEFFS['Hm'] * np.log(hm + 1) +
            COEFFS['NCS'] * np.log(ncs + 1) +
            COEFFS['NCSF'] * np.log(ncsf + 1) +
            COEFFS['NCSFL'] * np.log(ncsfl + 1)
        )
        
        if score >= target_score:
            return n
            
    return -1

# -----------------------------------------------------------------------------
# 4. EXECUTION
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    for _FILENAME in FILENAME:
        if not os.path.exists(_FILENAME):
            print(f"Error: Could not find '{FILENAME}' in the current directory.")
    else:
        print(f"Reading '{FILENAME}'...")
        print(f"Looking for author aliases: {TARGET_ALIASES}")

        parsed_papers = []
        for _FILENAME in FILENAME:
            parsed_papers+=parse_bib_file(_FILENAME, TARGET_ALIASES, CITATION_FIELD)
        # print(parsed_papers)

        if parsed_papers:
            c_score, metrics,paper_reports = calculate_engineering_c_score(parsed_papers)
            positive_cited_papers = [p for p in parsed_papers if p['citations'] > 0]

            print("\n" + "=" * 40)
            print(f" FINAL C-SCORE: {c_score:.5f}")
            print("=" * 40)
            print("\nMetrics Breakdown:")
            print(f" - Papers Counted: {len(parsed_papers)}")
            print(f" - Papers with Positive Citations:  {len(positive_cited_papers)}")
            print("-" * 25)
            for k, v in metrics.items():
                print(f"{k:<20}: {v}")

            print("PAPER-WISE METRICS BREAKDOWN")
            print("="*80)
            # Header
            print(f"{'Title':<50} | {'Cites':<6} |{'NCS':<6} | {'NCSF':<6} | {'NCSFL':<6}")
            print("-" * 80)
            
            # Rows
            for p in paper_reports:
                if p['cites'] > 0:
                    # Truncate title if too long
                    t_display = (p['title'][:47] + '..') if len(p['title']) > 47 else p['title']
                    print(f"{t_display:<50} | {p['cites']:<6}| {p['NCS']:<6} | {p['NCSF']:<6} | {p['NCSFL']:<6}")
        else:
            print("No matching papers found (check author name or file content).")

    if PREDICT:
        print(f"\n--- STRATEGY REPORT: FIRST AUTHOR PAPERS ---")
        print(f"Target Score: {THRESHOLD:.4f}")
        print(f"Assumed Team Size: {TeamSize} Authors\n")
        print(f"{'Avg Citations':<15} | {'Papers Needed':<15} | {'Total Citations':<15}")
        print("-" * 50)

        for cites in SCENARIOS:
            n = predict_papers_needed(THRESHOLD, cites, num_authors=TeamSize)
            print(f"{cites:<15} | {n:<15} | {n*cites:<15}") 

        print(f"\n--- STRATEGY REPORT: SINGLE AUTHOR PAPERS ---")
        print(f"Target Score: {THRESHOLD:.4f}")
        print(f"Authorship: Single Author (Maximum Impact Factor)\n")
        print(f"{'Avg Citations':<15} | {'Papers Needed':<15} | {'Total Citations':<15}")
        print("-" * 50)
        
        for cites in SCENARIOS:
            n = predict_single_author_papers(THRESHOLD, cites)
            print(f"{cites:<15} | {n:<15} | {n*cites:<15}")
