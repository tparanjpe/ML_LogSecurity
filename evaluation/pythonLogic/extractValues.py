import json
import csv
import pandas as pd

with open('testing.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

sentenceNum = 1
for body in data:
    sentence = body["full_text"]
    frequencies = {'SentenceIndex': sentenceNum, 'Sentence': repr(sentence), 'PERSON': 0, 'CREDIT_CARD': 0, 'STREET_ADDRESS': 0, 'US_SSN': 0}

    for span in body["spans"]:
        type = span["entity_type"]
        if type in frequencies:
            frequencies[type] = frequencies[type] + 1

    new = pd.DataFrame.from_dict([frequencies])
    new.to_csv('groundTruth.csv', mode='a', index=False, header=False)
    sentenceNum +=1