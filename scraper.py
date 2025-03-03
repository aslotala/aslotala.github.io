# Useful links:
# Exercise -   https://kciebiera.github.io/www-2425/lab1.html
# My website - https://aslotala.github.io/
# My site -    https://www.oldest.org/entertainment/board-games/

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

r = requests.get('https://www.oldest.org/entertainment/board-games/')
start = '<h3>8. Chess</h3>'
end = '<p>Although historians aren&#8217;t quite sure how exactly the game was played, Timothy Kendall and R.C. Bell have made their own reconstructions of the game. Kendall and Bell&#8217;s rules are based on pieces of texts mentioning Senet and these rules have been adopted by modern senet players.</p>'

html = r.text
cut_html = r.text.split(start)[1].split(end)[0]

soup = BeautifulSoup(cut_html, 'html.parser')

# Extract game titles, descriptions, and images
games = []
for h3 in soup.find_all('h3'):
    game_name = h3.get_text(strip=True)
    description = h3.find_next_sibling('p')
    image = h3.find_next('img')

    game_info = f"## {game_name}\n"
    if description:
        game_info += f"{description.get_text(strip=True)}\n"
    if image:
        img_url = image['src']
        game_info += f"![{game_name}]({img_url})\n"

    games.append(game_info)

# Convert to Markdown
markdown_content = "# Oldest Board Games\n\n" + "\n\n".join(games)

# Save to README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write(markdown_content)

print("Scraped content saved to README.md")
