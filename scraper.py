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

soup = BeautifulSoup(cut_html, 'html.parser')

img_folder = "photos"
os.makedirs(img_folder, exist_ok=True)

# Extract game titles, descriptions, and images
games = []
for h3 in soup.find_all('h3'):
    game_name = h3.get_text(strip=True)
    
    # Find the info section (date created, country of origin, etc.)
    info_section = h3.find_next('div', class_="wpb_text_column wpb_content_element")
    
    # If no div with class found, attempt a broader search (e.g., first <div> following the <h3>)
    if not info_section:
        info_section = h3.find_next('div')

    # If we found the info section, convert it to markdown
    game_info = f"## {game_name}\n\n"
    
    if info_section:
        info_text = markdownify(str(info_section))
        game_info += info_text + "\n\n"
    
    # Find the description of the game
    description_section = h3.find_next('p')  # Description typically comes right after the info section
    if description_section:
        game_info += f"{description_section.get_text(strip=True)}\n\n"
    
    # Process images (download them and save to the local folder)
    image = h3.find_next('img')
    if image and 'src' in image.attrs:
        img_url = image.attrs['src']
        
        # Check if the image URL is a full URL or needs to be prefixed
        if not img_url.startswith('http'):
            img_url = 'https://www.oldest.org' + img_url
        
        img_name = f"{game_name.lower().replace(' ', '_')}.jpg"
        img_path = os.path.join(img_folder, img_name)
        
        # Download the image and save it locally
        try:
            img_data = requests.get(img_url).content
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
            # Add image to Markdown
            game_info += f"![{game_name}]({img_folder}/{img_name})\n\n"
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image for {game_name}: {e}")

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