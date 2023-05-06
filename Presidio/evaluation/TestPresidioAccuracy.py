
import csv
import math
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# COLUMN INDEXES in groundtruth.csv:
# 1: sentence
# 2: PERSON
# 3: CREDIT_CARD
# 4: STREET_ADDRESS
# 5: US_SSN

# Set up the engine, loads the NLP module (spaCy model by default)
# and other PII recognizers
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

entities = ['PERSON','CREDIT_CARD','STREET_ADDRESS','US_SSN']
# initialize results
TP = [0] * len(entities)
FP = [0] * len(entities)
TN = [0] * len(entities)
FN = [0] * len(entities)

# loop of reading line by line
with open('groundTruth.csv') as csv_file:
    reader = csv.DictReader(csv_file, delimiter=',')
    for row in reader:
        sentence = row['Sentence']
        # apply presidio to the line (with appropriate entities)
        result = analyzer.analyze(text=sentence, entities=entities,language='en')
        # apply anonymizer
        anonymized_text = anonymizer.anonymize(text=sentence, analyzer_results=result)
        anonymized_text = str(anonymized_text)

        # counts of PII
        counts_experimental = [anonymized_text.count(PII) for PII in entities]
        counts_truth = [int(row[entity]) for entity in entities]

        # TP, FP, TN, FN for each category of PII
        for i in range(len(entities)):
            if counts_experimental[i] == 0 and counts_truth[i] == 0:
                TN[i] += 1
            elif counts_experimental[i] == counts_truth[i]:
                TP[i] += counts_experimental[i]
            elif counts_experimental[i] < counts_truth[i]:
                TP[i] += counts_experimental[i]
                FN[i] += counts_truth[i] - counts_experimental[i]
            elif counts_experimental[i] > counts_truth[i]:
                TP[i] += counts_truth[i]
                FP[i] += counts_experimental[i] - counts_truth[i]

# print results
print('TP, TN, FP, FN')
for i in range(len(entities)):
    print("%s : %d, %d, %d, %d" % (entities[i], TP[i], TN[i], FP[i], FN[i]))

print('')

for i in range(len(entities)):
    accuracy = (TP[i] + TN[i]) / (TP[i] + TN[i] + FP[i] + FN[i])
    precision = TP[i]/(TP[i]+FP[i]) if TP[i]+FP[i] != 0 else math.nan
    recall = TP[i]/(TP[i]+FN[i]) if TP[i]+FN[i] != 0 else math.nan
    f1_score = 2*precision*recall/(precision+recall) if not math.isnan(precision) and not math.isnan(recall) else math.nan
    print("%s accuracy: %.4f" %(entities[i], accuracy))
    print("%s precision: %.4f" %(entities[i], precision))
    print("%s recall: %.4f" %(entities[i], recall))
    print("%s f1_score: %.4f" %(entities[i], f1_score))
    print('')

print('')

# relevant?
TP_all, TN_all, FP_all, FN_all = sum(TP), sum(TN), sum(FP), sum(FN)
accuracy = (TP_all + TN_all) / (TP_all + TN_all + FP_all + FN_all)
precision = TP_all/(TP_all+FP_all)
recall = TP_all/(TP_all+FN_all)
f1_score = 2*precision*recall/(precision+recall)
print("overall accuracy: %.4f" % accuracy)
print("overall precision: %.4f" % precision)
print("overall recall: %.4f" % recall)
print("overall f1_score: %.4f" % f1_score)


