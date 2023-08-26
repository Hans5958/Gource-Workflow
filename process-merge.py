from pathlib import Path
import git
from dateutil.parser import parse
import time
import fileinput
import os
from repo_list import list, code

Path('log').mkdir(parents=True, exist_ok=True)
Path('caption').mkdir(parents=True, exist_ok=True)
Path('config').mkdir(parents=True, exist_ok=True)

# shutil.rmtree('../gource_temp', ignore_errors=True)

aliases = dict()
author_names = set()

if os.path.exists('aliases.txt'):
	with open('aliases.txt', 'r') as f:
		for line in f:
			if ':' not in line:
				continue
			alias, real = line.strip().split(':')
			aliases[alias] = real
	
log_lines = []
captions = []

for name in list:

	print(name)
	
	normalized_name = name.replace('/', '__')

	if not os.path.exists(f'log-raw/{normalized_name}.txt'):
		continue		
	
	# shutil.rmtree(Path('..', 'gource_temp', normalized_name), ignore_errors=True)
	
	# ==== Log ====

	# with open(f'log/{normalized_name}.txt', mode='r') as file:
	with open(f'log-raw/{normalized_name}.txt', 'r', encoding='utf-8') as file_raw:
		for line in file_raw:
			entry = line.strip().split('|')
			# print(entry)
			if entry[1] in aliases:
				# print(aliases[entry[1]])
				entry[1] = aliases[entry[1]]
			author_names.add(entry[1])
			entry[3] = '/' + name + entry[3]
			log_lines.append('|'.join(entry))

	# ==== Captions ====

	if os.path.exists(f'../gource_temp/{normalized_name}'):
		repo = git.Repo(f'../gource_temp/{normalized_name}')
		tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
		for tag in tags:
			unix = time.mktime(tag.commit.committed_datetime.timetuple())
			tag_name = tag.name
			captions.append(f'{unix}|{name}: {tag_name} released')

		#if os.path.exists(f'caption-additional/{normalized_name}.txt'):
		#	with open(f'caption-additional/{normalized_name}.txt', 'r') as f:
		#		for line in f:
		#			captions.append(line.strip())

# ==== Config ====

with open(f'config/merged_{code}.ini', 'w') as f:
	f.write(f"""[gource]
path=log/merged_{code}.txt
caption-file=caption/merged_{code}.txt
title={len(list)} repositories
auto-skip-seconds=0.01
seconds-per-day=0.1
caption-duration=2
bloom-multiplier=0.75
bloom-intensity=0.5
hide=filenames
background-colour=000000
user-image-dir=avatar/

# Render configuration
# Uncomment before rendering to use it

# caption-size=32
# font-scale=2
""")

log_lines.sort()

with open(f'log/merged_{code}.txt', 'w', encoding='utf-8') as f:
	for line in log_lines:
		f.write(f'{line}\n')
	pass

captions.sort()

with open(f'caption/merged_{code}.txt', 'w', encoding='utf-8') as f:
	for line in captions:
		f.write(f'{line}\n')
	# print(tags)
			
	# shutil.rmtree(Path('..', 'gource_temp', normalized_name), ignore_errors=True)

author_names = sorted(author_names)
with open(f'all-authors.txt', 'w', encoding='utf-8') as f:
	for line in author_names:
		f.write(line + '\n')
