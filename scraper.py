# Useful links:
# Exercise -   https://kciebiera.github.io/www-2425/lab1.html
# My website - https://aslotala.github.io/
# My site -    https://www.oldest.org/entertainment/board-games/

import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

GITHUB_IMAGE_URL = "https://github.com/aslotala/aslotala.github.io/blob/main/photos/"

url = 'https://www.oldest.org/entertainment/board-games/'

r = requests.get(url)

start_marker = '<p>Although the exact rules of these ancient games have been lost, historians have been able to piece together and reconstruct gameplay so people can play them today.</p>'
end_marker = '<p>Although historians aren&#8217;t quite sure how exactly the game was played, Timothy Kendall and R.C. Bell have made their own reconstructions of the game. Kendall and Bell&#8217;s rules are based on pieces of texts mentioning Senet and these rules have been adopted by modern senet players.</p>'

cut_html = r.text.split(start_marker)[1].split(end_marker)[0]

LOCAL_IMAGE_FOLDER = "photos"
os.makedirs(LOCAL_IMAGE_FOLDER, exist_ok=True)

# Convert the entire HTML content to Markdown
markdown_content = markdownify(cut_html)

# Save the converted Markdown to a file
readme_path = "README.md"
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print("README.md has been updated with the converted Markdown content.")