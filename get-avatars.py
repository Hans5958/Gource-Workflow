from pathlib import Path
import urllib.request
import requests
from bs4 import BeautifulSoup
import os

Path('avatar').mkdir(parents=True, exist_ok=True)

# shutil.rmtree('../gource_temp', ignore_errors=True)

author_names = set()

for filename in os.listdir('log'):

	print(filename)
	
	with open(f'log/{filename}', 'r', encoding='utf-8') as f:
		for line in f:
			# print(line.split('|'))
			author_names.add(line.split('|')[1])

author_names = sorted(author_names)

for username in author_names:
	if ' ' in username:
		continue
	print(f'Getting {username}...')
	if username.endswith('[bot]'):
		app_username = username.replace('[bot]', '')
		response = requests.get(f'https://github.com/apps/{app_username}')
		soup = BeautifulSoup(response.content, 'html.parser')
		try:
			urllib.request.urlretrieve(soup.select_one('.CircleBadge img')['src'].split('?s')[0], f'avatar/{username}.png')
		except:
			pass
	else:
		try:
			urllib.request.urlretrieve(f'https://github.com/{username.replace("[bot]", "")}.png', f'avatar/{username}.png')
		except:
			pass

print('Done!')