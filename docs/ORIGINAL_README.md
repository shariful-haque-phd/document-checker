# Accessible Document Checker

A static accessibility checker for HTML files.

## Checks
- images missing `alt`
- skipped heading levels
- empty links
- vague link labels
- form controls without accessible labels
- missing page language
- missing document title

## Usage
```bash
pip install -r requirements.txt
python src/check_accessibility.py sample/page.html
```

This is a screening tool, not a substitute for manual accessibility testing or assistive-technology testing.
