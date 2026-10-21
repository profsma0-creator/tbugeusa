"""Consistency checks across the reconstructed chapters.

Checks heading sequence, table/figure numbering, citation-reference matching,
and a small set of British-style and typographic conventions. Prints a report;
exits non-zero if a hard check fails.
"""
from pathlib import Path
import json, re, sys

REFS = {}
for n in range(1, 21):
    name = 'manuscript/chapter01-verified-references.json' if n == 1 else f'manuscript/chapter{n:02d}-references.json'
    REFS[n] = json.loads(Path(name).read_text())

problems = []
report = []
US = {'behavior': 'behaviour', 'color': 'colour', 'organiz': 'organis', 'analyz': 'analys',
      'modeling': 'modelling', 'labeled': 'labelled', 'center': 'centre', 'defense': 'defence',
      'program ': 'programme ', 'fetus': 'fetus', 'pediatric': 'paediatric', 'estrogen': 'oestrogen',  # only when standalone; 'oestrogen' contains it
      'hemoglobin': 'haemoglobin', 'leukocyte': 'leucocyte'}

for n in range(1, 21):
    text = Path(f'manuscript/chapter{n:02d}.md').read_text()
    words = len(text.split())
    # heading numbering
    heads = re.findall(r'^## (\d+)\.(\d+) ', text, re.M)
    nums = [int(b) for a, b in heads]
    if nums and nums != list(range(1, len(nums) + 1)):
        problems.append(f'Ch{n}: section numbering {nums}')
    # table / figure numbering
    tabs = re.findall(r'^Table (\d+)\.(\d+)\.', text, re.M)
    if any(int(a) != n for a, b in tabs):
        problems.append(f'Ch{n}: table chapter prefix mismatch {tabs}')
    tnums = [int(b) for a, b in tabs]
    if tnums and tnums != list(range(1, len(tnums) + 1)):
        problems.append(f'Ch{n}: table numbering {tnums}')
    figs = re.findall(r'\[FIGURE:(\d+)\.(\d+)\]', text)
    if any(int(a) != n for a, b in figs):
        problems.append(f'Ch{n}: figure chapter prefix mismatch {figs}')
    # references present
    refs = REFS[n]
    if not refs:
        problems.append(f'Ch{n}: no references')
    refkeys = set()
    for r in refs:
        m = re.match(r'([^,(]+)', r)
        surname = m.group(1).strip() if m else ''
        y = re.search(r'\((\d{4})[a-z]?\)', r)
        refkeys.add((surname.split()[-1] if surname else '', y.group(1) if y else ''))
    # in-text citations
    cites = set()
    for m in re.finditer(r'\(([^()]{0,120}?(?:19|20)\d{2}[a-z]?)\)', text):
        for part in m.group(1).split(';'):
            y = re.search(r'((?:19|20)\d{2})', part)
            nm = re.match(r'\s*(?:e\.g\.,\s*|see\s+|cf\.\s*)?([A-Z][A-Za-zÀ-ÿ\'\-]+)', part)
            if y and nm:
                cites.add((nm.group(1), y.group(1)))
    for m in re.finditer(r'([A-Z][A-Za-zÀ-ÿ\'\-]+)(?:\s+(?:and|&)\s+[A-Z][A-Za-zÀ-ÿ\'\-]+)?\s+\(((?:19|20)\d{2})\)', text):
        cites.add((m.group(1), m.group(2)))
    refnames = {k[0] for k in refkeys}
    STOP = {'Table', 'Chapter', 'Figure', 'Since', 'During', 'In', 'The', 'This', 'Between', 'For', 'After', 'Karolinska'}
    for nm, y in sorted(cites):
        if nm in STOP:
            continue
        base = nm[:-2] if nm.endswith("'s") else nm
        if (nm, y) not in refkeys and nm not in refnames and base not in refnames:
            problems.append(f'Ch{n}: citation {nm} {y} has no matching reference')
    # style flags
    for bad, good in US.items():
        if bad.strip() and re.search(r'(?<![a-z])' + re.escape(bad.strip()) + r'(?![a-z])', text.lower()):
            report.append(f'Ch{n}: US spelling "{bad.strip()}" (prefer {good})')
    if re.search(r'[a-z]  [a-z]', text):
        report.append(f'Ch{n}: double space')
    if re.search(r'\s,', text):
        report.append(f'Ch{n}: space before comma')
    report.append(f'Ch{n}: {words} words, {len(refs)} references, {len(nums)} sections, {len(tnums)} tables, {len(figs)} figures')

print('\n'.join(report))
print('\n--- problems ---')
print('\n'.join(problems) if problems else 'none')
sys.exit(1 if problems else 0)
