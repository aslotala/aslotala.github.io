# Useful links:
# Exercise -   https://kciebiera.github.io/www-2425/lab1.html
# My website - https://aslotala.github.io/
# My site -    https://www.oldest.org/entertainment/board-games/

import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

GITHUB_IMAGE_URL = "https://github.com/aslotala/aslotala.github.io/blob/main/photos/"

url = 'https://www.oldest.org/entertainment/board-games/'

r = requests.get(url)

start_marker = '<h3>8. Chess</h3>'
end_marker = '<p>Although historians aren&#8217;t quite sure how exactly the game was played, Timothy Kendall and R.C. Bell have made their own reconstructions of the game. Kendall and Bell&#8217;s rules are based on pieces of texts mentioning Senet and these rules have been adopted by modern senet players.</p>'

cut_html = r.text.split(start_marker)[1].split(end_marker)[0]

soup = BeautifulSoup(cut_html, 'html.parser')

img_folder = "photos"
os.makedirs(img_folder, exist_ok=True)


# Extract game titles, descriptions, and images
games = []
for h3 in soup.find_all('h3'):
    game_name = h3.get_text(strip=True)
    description = h3.find_next_sibling('p')
    image = h3.find_next('img')

    game_info = f"## {game_name}\n\n"
    
    if description:
        game_info += f"{description.get_text(strip=True)}\n\n"

    # Process images (but use GitHub instead of downloading)
    if image and 'src' in image.attrs:
        img_name = f"{game_name.lower().replace(' ', '_')}.jpg"
        img_url = f"{GITHUB_IMAGE_URL}{img_name}"  # Reference GitHub image
        img_source = image['src']  # Original image source

        # Add image and source to Markdown
        game_info += f"![{game_name}]({img_url})\n\n"
        game_info += f"<sub>Photo source: {img_source}</sub>\n\n"

    games.append(game_info)

# Convert to Markdown
markdown_content = "# Oldest Board Games\n\n" + "\n\n".join(games)

# Clear README.md before writing
readme_path = "README.md"
if os.path.exists(readme_path):
    open(readme_path, "w").close()  # Truncate file (delete content)

# Save to README.md
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print("README.md has been cleared and updated with new scraped content.")