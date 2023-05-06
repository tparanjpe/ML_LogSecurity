'''
Iterate through macieResults.json

'''
import json
import csv
import pandas as pd

with open('macieResults.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

frequencies = {}
# layout of array = [ 'PERSON', 'CREDIT_CARD', 'STREET_ADDRESS', 'US_SSN']

# print(data["classificationDetails"]["result"]["sensitiveData"]["occurrences"])
# print(data["classificationDetails"]["result"]["sensitiveData"])
for body in data["classificationDetails"]["result"]["sensitiveData"]:
    for occurence in body["detections"]:
        type = occurence["type"]
        print(type)
        for line in occurence["occurrences"]["lineRanges"]:
            sentenceIndex = line["start"]
            # print(sentenceIndex)
            if sentenceIndex in frequencies:
                currentSetup = frequencies[sentenceIndex]
            else: 
                currentSetup = [0, 0, 0, 0]
            if type == 'NAME':
                updatedValue = currentSetup[0] + 1
                currentSetup[0] = updatedValue
            elif type == "CREDIT_CARD_NUMBER":
                updatedValue = currentSetup[1] + 1
                currentSetup[1] = updatedValue
            elif type == "ADDRESS":
                updatedValue = currentSetup[2] + 1
                currentSetup[2] = updatedValue
            elif type == "USA_SOCIAL_SECURITY_NUMBER":
                updatedValue = currentSetup[3] + 1
                currentSetup[3] = updatedValue
            frequencies[sentenceIndex] = currentSetup
            # print(line)
            
print(frequencies)
df = pd.DataFrame.from_dict(frequencies, orient ='index') 
df.to_csv('macieResults.csv', header=False)

print(df)
