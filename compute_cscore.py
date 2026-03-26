import requests
import math

# Coefficients from c-score.py
COEFFS = {
    "NC": 0.08810111,
    "H": 0.21621749,
    "Hm": 0.25977242,
    "NCS": 0.10252264,
    "NCSF": 0.09185340,
    "NCSFL": 0.09075539,
}

def compute_cscore(papers):
    nc_total = sum(p['citations'] for p in papers)
    citations_list = sorted([p['citations'] for p in papers], reverse=True)
    h_index = 0
    for i, c in enumerate(citations_list):
        if c >= i + 1:
            h_index = i + 1
        else:
            break
    fractional = []
    for p in papers:
        n_auth = p['num_authors']
        fractional.append(p['citations'] / n_auth if n_auth > 0 else 0)
    fractional.sort(reverse=True)
    hm_index = 0
    for i, f in enumerate(fractional):
        if f >= i + 1:
            hm_index = i + 1
        else:
            break
    ncs_total = sum(p['citations'] for p in papers if p['role'] == 'single')
    ncsf_total = sum(p['citations'] for p in papers if p['role'] in ('single', 'first'))
    ncsfl_total = sum(p['citations'] for p in papers if p['role'] in ('single', 'first', 'last'))
    score = (
        COEFFS['NC'] * math.log(nc_total + 1) +
        COEFFS['H'] * math.log(h_index + 1) +
        COEFFS['Hm'] * math.log(hm_index + 1) +
        COEFFS['NCS'] * math.log(ncs_total + 1) +
        COEFFS['NCSF'] * math.log(ncsf_total + 1) +
        COEFFS['NCSFL'] * math.log(ncsfl_total + 1)
    )
    return score, {
        'NC': nc_total,
        'H': h_index,
        'Hm': hm_index,
        'NCS': ncs_total,
        'NCSF': ncsf_total,
        'NCSFL': ncsfl_total
    }

def main():
    r = requests.get('http://localhost:8000/api/papers')
    papers = r.json()
    print(f'Loaded {len(papers)} papers')
    score, metrics = compute_cscore(papers)
    print('C‑Score:', score)
    print('Metrics:', metrics)
    # Compare with original c-score.py output? We'll just show.

if __name__ == '__main__':
    main()
