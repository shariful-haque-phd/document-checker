import argparse,json,re
from bs4 import BeautifulSoup
from pathlib import Path

VAGUE={"click here","read more","more","link","here"}

def check(html):
    soup=BeautifulSoup(html,"html.parser");issues=[]
    if not soup.html or not soup.html.get("lang"):
        issues.append({"type":"missing_language","detail":"<html> has no lang attribute."})
    if not soup.title or not soup.title.get_text(strip=True):
        issues.append({"type":"missing_title","detail":"Document has no non-empty <title>."})
    for i,img in enumerate(soup.find_all("img"),1):
        if img.get("alt") is None:
            issues.append({"type":"missing_alt","detail":f"Image #{i} has no alt attribute."})
    last=0
    for h in soup.find_all(re.compile("^h[1-6]$")):
        level=int(h.name[1])
        if last and level>last+1:
            issues.append({"type":"heading_skip","detail":f"Heading level jumps from h{last} to h{level}: {h.get_text(' ',strip=True)[:80]}"})
        last=level
    for a in soup.find_all("a"):
        txt=a.get_text(" ",strip=True).lower()
        if not txt: issues.append({"type":"empty_link","detail":f"Empty link to {a.get('href','')}"})
        elif txt in VAGUE: issues.append({"type":"vague_link_text","detail":f'Link text "{txt}" lacks context.'})
    labels={x.get("for") for x in soup.find_all("label") if x.get("for")}
    for inp in soup.find_all(["input","select","textarea"]):
        if inp.get("type")=="hidden":continue
        ident=inp.get("id")
        if (not ident or ident not in labels) and not inp.get("aria-label") and not inp.get("aria-labelledby"):
            issues.append({"type":"unlabeled_control","detail":f"{inp.name} control may lack an accessible label."})
    return {"issue_count":len(issues),"issues":issues}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("html");a=ap.parse_args()
    print(json.dumps(check(Path(a.html).read_text(errors="replace")),indent=2))
if __name__=="__main__":main()
