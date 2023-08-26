import subprocess
import shlex
import shutil
from pathlib import Path
import git
from dateutil.parser import parse
import time
from repo_list import list

Path('log-raw').mkdir(parents=True, exist_ok=True)
Path('caption').mkdir(parents=True, exist_ok=True)
Path('config').mkdir(parents=True, exist_ok=True)

# shutil.rmtree('../gource_temp', ignore_errors=True)

for name in list:
		
	# shutil.rmtree(Path('..', 'gource_temp', normalized_name), ignore_errors=True)

	normalized_name = name.replace('/', '__')

	subprocess.run(shlex.split(f'git clone https://github.com/{name} ../gource_temp/{normalized_name}'))

	subprocess.run(shlex.split(f'gource --output-custom-log log-raw/{normalized_name}.txt ../gource_temp/{normalized_name}'), shell=True)

	# shutil.rmtree(Path('..', 'gource_temp', normalized_name), ignore_errors=True)