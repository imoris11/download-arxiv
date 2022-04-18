# download-arxiv
A simple command line tool for downloading arxiv (https://arxiv.org/) papers using the arxiv API. arxiv papers cover research in Physics, Mathematics, Computer Science, etc.

Update:

This also converts the PDFs to txt files. using tesseract

# Requirements

1. Python3
2. PIL
3. pytesseract
4. pdf2image

# Usage

1. python3 index.py <term> <limit>
  `python3 index.py vr 5` will download the top 5 matches for vr into the current directory.
