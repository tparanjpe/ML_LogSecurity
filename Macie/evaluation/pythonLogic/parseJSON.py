import json
import csv

with open('testing.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

sentence = []
for body in data:
    sentence.append(body['full_text'])
    
print(sentence)
 
# now we will open a file for writing
with open('data_file.txt', 'w', encoding='utf-8') as file:
    for line in sentence:
        file.write(repr(line) + "\n")

 
# # create the csv writer object
# csv_writer = csv.writer(data_file)

# # Counter variable used for writing
# # headers to the CSV file
# count = 0
 
# for sent in sentence:
#     if count == 0:
 
#         # Writing headers of CSV file
#         header = sent.keys()
#         csv_writer.writerow(header)
#         count += 1
 
#     # Writing data of CSV file
#     csv_writer.writerow(sent.values())
 
# data_file.close()