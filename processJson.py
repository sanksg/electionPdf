import json, pickle

#from pprint import pprint

data = []
i=0
with open('finalVoterList.txt') as data_file:    
    for line in data_file:
      jsonD = json.loads(line)
      for voter in jsonD['aaData']:
        data.append(voter)
      i+=1
#      if i>110:
#        break
        
    print(len(data))
    print(data[0])

with open('voterRecords.pcl', 'wb') as pickleFile:
  pickle.dump(data, pickleFile)