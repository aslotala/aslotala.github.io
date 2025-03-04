# Useful links:
# Exercise -   https://kciebiera.github.io/www-2425/lab1.html
# My website - https://aslotala.github.io/
# My site -    https://www.oldest.org/entertainment/board-games/

import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

GITHUB_IMAGES_URL = "https://github.com/aslotala/aslotala.github.io/blob/main/photos/"

url = 'https://www.oldest.org/entertainment/board-games/'

r = requests.get(url)

start_marker = '<h3>8. Chess</h3>'
end_marker = '<p>Although historians aren&#8217;t quite sure how exactly the game was played, Timothy Kendall and R.C. Bell have made their own reconstructions of the game. Kendall and Bell&#8217;s rules are based on pieces of texts mentioning Senet and these rules have been adopted by modern senet players.</p>'

cut_html = r.text.split(start_marker)[1].split(end_marker)[0]

soup = BeautifulSoup(cut_html, 'html.parser')

img_folder = "photos"
os.makedirs(img_folder, exist_ok=True)


games = []
for h3 in soup.find_all('h3'):
    game_name = h3.get_text(strip=True)
    description = h3.find_next_sibling('p')
    image = h3.find_next('img')

    game_info = f"## {game_name}\n"
    if description:
        game_info += f"{description.get_text(strip=True)}\n"

    # Process images (but use GitHub instead of downloading)
    if image and 'src' in image.attrs:
        img_name = f"{game_name.lower().replace(' ', '_')}.jpg"
        img_url = f"{GITHUB_IMAGES_URL}{img_name}"  # Reference GitHub image

        # Add image reference to Markdown
        game_info += f"![{game_name}]({img_url})\n"

    games.append(game_info)

# Convert to Markdown
markdown_content = "# Oldest Board Games\n\n" + "\n\n".join(games)

# Save to README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write(markdown_content)

print("Scraped content saved to README.md with GitHub image references.")