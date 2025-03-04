# Useful links:
# Exercise -   https://kciebiera.github.io/www-2425/lab1.html
# My website - https://aslotala.github.io/
# My site -    https://www.oldest.org/entertainment/board-games/

import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from duckduckgo_search import DDGS

url = 'https://www.oldest.org/entertainment/board-games/'
output_folder = "games_pages"
os.makedirs(output_folder, exist_ok=True)

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# Zbieranie wszystkich nazw gier
games = []
for h3 in soup.find_all('h3'):
    game_name = h3.get_text(strip=True)  # Nazwa gry
    games.append(game_name)
    print(game_name)

start_marker = '<p>Although the exact rules of these ancient games have been lost, historians have been able to piece together and reconstruct gameplay so people can play them today.</p>'
end_marker = '<p>Although historians aren&#8217;t quite sure how exactly the game was played, Timothy Kendall and R.C. Bell have made their own reconstructions of the game. Kendall and Bell&#8217;s rules are based on pieces of texts mentioning Senet and these rules have been adopted by modern senet players.</p>'

cut_html = r.text.split(start_marker)[1].split(end_marker)[0]

# Convert the entire HTML content to Markdown
markdown_content = markdownify(cut_html)

# Save the converted Markdown to a file
readme_path = "README.md"
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print("README.md saved successfully")
print("Games found: ", len(games))


def search_game_info(game_name):
    """Generates text about a board game using DuckDuckGo's chat function."""
    query = f"Tell me something about {game_name} board game"

    try:
        with DDGS() as ddgs:
            search_response = ddgs.chat(query)  # Returns a text response, not a list
        
        # If no response is received, provide a default message
        if not search_response:
            search_response = "No information found."
    
    except Exception as e:
        search_response = f"Error retrieving information: {str(e)}"

    # Format as Markdown
    search_section = f"## Additional Information about {game_name}\n\n{search_response}\n"
    
    return search_section


# print("Tworzenie podstron...")
# for game in games:
#     game_filename = f"{game.lower().replace(' ', '_')}.md"
#     game_filepath = os.path.join(output_folder, game_filename)
    
#     additional_info = search_game_info(game)

#     # Save the file
#     with open(game_filepath, 'w', encoding='utf-8') as f:
#         f.write(additional_info)

# print("Podstrony zostały utworzone.")


# Wczytaj zawartość README.md
with open(readme_path, 'r', encoding='utf-8') as f:
    readme_content = f.read()

# Zamiana nazw gier na linki
for game in games:
    game_filename = f"{game.lower().replace(' ', '_')}.md"
    game_url = os.path.join(output_folder, game_filename)
    
    # Podmieniamy nazwę gry na jej wersję z linkiem
    readme_content = readme_content.replace(game, f"[{game}]({game_url})")

# Zapisanie zaktualizowanego pliku README.md
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("README.md został zaktualizowany.")