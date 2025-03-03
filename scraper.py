# https://kciebiera.github.io/www-2425/lab1.html
# https://kciebiera.github.io/www-2425/
# https://aslotala.github.io/
# https://www.oldest.org/entertainment/board-games/

import requests

r = requests.get('https://www.oldest.org/entertainment/board-games/')

html_doc = r.text
pocz = 'wpb-content-wrapper'

html_doc.split(pocz)

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

# elements = soup.find_all(class_='col-md-8 content-holder')

from markdownify import markdownify as md
print(md('<b>Yay</b> <a href="http://github.com">GitHub</a>', convert=['b']))

