'''Algorithm R Implementation
(*S has items to sample, R will contain the result*)

ReservoirSample(S[1..n], R[1..k])
  // fill the reservoir array
  for i = 1 to k
      R[i] := S[i]

  // replace elements with gradually decreasing probability
  for i = k+1 to n
    j := random(1, i)   // important: inclusive range
    if j <= k
        R[j] := S[i]
'''

import subprocess
import os
import time
import random 
import json
import csv

path = 'data_cleaned/'
jsons = [jsonfile for jsonfile in os.listdir(path) if jsonfile.endswith('.json')]

count = 0
reservoir = []
times = {}

def get_interval(datestring):
    ddhhmm = datestring[8:19].replace(' ', '').replace(':', '')
    if int(ddhhmm[-2:]) >= 30:
        ddhhmm = ddhhmm[:-2] + '30'
    else:
        ddhhmm = ddhhmm[:-2] + '00'
    return ddhhmm

r_size = 300000

for jsonfile in jsons:
  with open(path + jsonfile, encoding='utf-8') as f:
    for item in f:
        r = json.loads(item)
        try:
            # get frequency of tweets in 30 minute intervals
            interval = get_interval(r["created_at"])
            if interval not in times:
                times[interval] = 1
            else:
                times[interval] += 1  

            # Reservoir sampling
            if count < r_size:
                reservoir.append(r)
            else:
                j = random.randint(1, count)
                if j < r_size:
                    
                    if count % 100000 == 0: # print progress 
                        print('went through ' + str(count) + ' items')
                        #print('replacing index ' + str(j) + ' with item')
                        
                    reservoir[j] = r

            count += 1  

        except:
            continue

print('DONE. Went through ' + str(count) + ' items total.')

# save reservoir to new json file 
with open('tweet_sample.json', 'w') as f:
    json.dump(reservoir, f)

# save times to csv
with open('times_data.csv', 'w') as f:  
    w = csv.DictWriter(f, times.keys())
    w.writeheader()
    w.writerow(times)
