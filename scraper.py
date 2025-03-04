# Useful links:
# Exercise -   https://kciebiera.github.io/www-2425/lab1.html
# My website - https://aslotala.github.io/
# My site -    https://www.oldest.org/entertainment/board-games/

import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from duckduckgo_search import DDGS
from duckduckgo_search import ddg_search

url = 'https://www.oldest.org/entertainment/board-games/'
output_folder = "games_pages"

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
    # Create a query to search for game information
    query = f"Tell me something about {game_name} board game"
    
    # Perform the DuckDuckGo search using the chat() method
    search_results = DDGS().chat(query)  # Make sure chat returns relevant data
    
    # Initialize the Markdown section
    search_section = f"## Additional Information about {game_name}\n\n"
    
    # Loop through the search results and format them
    for i, result in enumerate(search_results[:5]):  # Limit to 5 results
        search_section += f"{i + 1}. [Link {i + 1}]({result['href']})\n"
        search_section += f"    - **Title**: {result['title']}\n"
        search_section += f"    - **Description**: {result['body']}\n\n"
    
    return search_section


print("Tworzenie podstron...")
for game in games:
    game_filename = f"{game.lower().replace(' ', '_')}.md"  # Zmieniamy na odpowiednią nazwę pliku
    game_filepath = os.path.join(output_folder, game_filename)
    
    additional_info = search_game_info(game)

    # Zapisanie pliku
    with open(game_filepath, 'w', encoding='utf-8') as f:
        f.write(additional_info)

print("Podstrony zostały utworzone.")




# Zalinkowanie stron w README.md
# Zaktualizowanie pliku README.md
readme_path = "README.md"

# Nagłówek
readme_content = "# Lista Najstarszych Gier Planszowych\n\n"

# Tworzenie linków do każdej gry
for game in games:
    # Zmieniamy nazwę gry na odpowiednią nazwę pliku
    game_filename = f"{game.lower().replace(' ', '_')}.md"
    
    # Sprawdzamy, czy plik dla tej gry istnieje
    game_url = os.path.join(output_folder, game_filename)
    
    # Tworzymy link w formacie Markdown
    readme_content += f"- [{game}]({game_url})\n"

# Zapisanie pliku README.md
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("README.md zostało zaktualizowane.")