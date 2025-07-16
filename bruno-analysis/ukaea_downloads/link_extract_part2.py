import os
import re

# Regex to match any URL under opendata.ukaea.uk
ukaea_url_pattern = re.compile(r'https?://opendata\.ukaea\.uk/[^\s"\'<>]+')

found_urls = set()

# Loop through all numbered HTML files
for filename in os.listdir("."):
    if filename.isdigit():
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                matches = ukaea_url_pattern.findall(content)
                found_urls.update(match.strip() for match in matches)
                print(f"🔍 {filename}: {len(matches)} links")
        except Exception as e:
            print(f"❌ Error in {filename}: {e}")

# Save the list to a file
with open("ukaea_links.txt", "w") as out:
    for url in sorted(found_urls):
        out.write(url + "\n")

print(f"✅ Extracted {len(found_urls)} unique opendata.ukaea.uk links.")


useful_types = ('.csv', '.json', '.mat', '.nc')
useful_urls = [u for u in found_urls if u.lower().endswith(useful_types)]


print(f"✅ Extracted {len(found_urls)} total links.")
print(f"🎯 Of which {len(useful_urls)} are likely to be data files.")


with open("ukaea_datafiles.txt", "w") as data_out:
    for url in sorted(useful_urls):
        data_out.write(url + "\n")
