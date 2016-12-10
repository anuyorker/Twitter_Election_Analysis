import subprocess
import os

path = 'data/'
jsons = [jsonfile for jsonfile in os.listdir(path) if jsonfile.endswith('.json')]

for jsonfile in jsons:
	outfile = jsonfile.split('.json')[0] + '_cleaned.json'
	subprocess.check_output(["cat", jsonfile, "|", "jq", "'.'", "-c", ">", outfile])
	

