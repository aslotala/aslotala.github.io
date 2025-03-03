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



print("end")

