from bs4 import BeautifulSoup
import re
import os

doi_links = set()

# Regular expressions
doi_regex = re.compile(r'https?://(?:www\.)?(?:dx\.)?doi\.org/\S+')
iop_regex = re.compile(r'https?://iopscience\.iop\.org/article/\S+')

for filename in os.listdir("."):
    if filename.isdigit():
        try:
            with open(filename, "r", encoding="utf-8") as f:
                html = f.read()
                soup = BeautifulSoup(html, "html.parser")

                # From anchor tags
                for tag in soup.find_all("a", href=True):
                    href = tag["href"]
                    if "doi.org" in href or "iopscience.iop.org" in href:
                        doi_links.add(href.strip())

                # From visible text
                for match in doi_regex.findall(html):
                    doi_links.add(match.strip())
                for match in iop_regex.findall(html):
                    doi_links.add(match.strip())

        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")

# Write results
with open("extracted_doi_links.txt", "w") as out:
    for link in sorted(doi_links):
        out.write(link + "\n")

print(f"✅ Extracted {len(doi_links)} unique DOI/IOP links.")
