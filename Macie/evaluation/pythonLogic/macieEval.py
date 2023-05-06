'''
iterate through macieResults.csv
for each sentenceIndex, find the corresponding index in the groundTruth.csv
compare ground truth to macie results
calculate TN, TP, FN, FP

'''

import pandas as pd

groundTruth = pd.read_csv("groundTruth.csv")
macieResults = pd.read_csv("macieResults.csv")
# [tp, tn, fp, fn]
fieldResults = {
    "PERSON": [0, 0, 0, 0],
    "CREDIT_CARD": [0, 0, 0, 0],
    "STREET_ADDRESS": [0, 0, 0, 0],
    "US_SSN": [0, 0, 0, 0]
}


for index, row in groundTruth.iterrows():
    gtIndex = row["SentenceIndex"]
    numPersons = row["PERSON"]
    numCC = row["CREDIT_CARD"]
    numAddress = row["STREET_ADDRESS"]
    numSSN = row["US_SSN"]
    if gtIndex in macieResults['sentenceIndex'].values:
        results = macieResults.loc[macieResults['sentenceIndex'] == gtIndex].values.tolist()
        print(results)

        results[0].pop(0)
        results = results[0]
        print(results)
    else:
        print("no record")
        results = [0, 0, 0, 0]

    if numPersons == 0 and results[0] == 0:
        fieldResults["PERSON"][1] = fieldResults["PERSON"][1] + 1
    elif numPersons == results[0]:
        #update with tp value
        fieldResults["PERSON"][0] = fieldResults["PERSON"][0] + numPersons
    elif numPersons > results[0]:
        # tp = results[0]
        # fn = numPersons - results[0]
        fieldResults["PERSON"][0] = fieldResults["PERSON"][0] + results[0]
        fieldResults["PERSON"][3] = fieldResults["PERSON"][3] + (numPersons - results[0])
    else:
        fieldResults["PERSON"][0] = fieldResults["PERSON"][0] + numPersons
        fieldResults["PERSON"][2] = fieldResults["PERSON"][2] + (results[0] - numPersons)

    if numCC == 0 and results[1] == 0:
        fieldResults["CREDIT_CARD"][1] = fieldResults["CREDIT_CARD"][1] + 1
    elif numCC == results[1]:
        #update with tp value
        fieldResults["CREDIT_CARD"][0] = fieldResults["CREDIT_CARD"][0] + numCC
    elif numCC > results[1]:
        # tp = results[1]
        # fn = numCC - results[1]
        fieldResults["CREDIT_CARD"][0] = fieldResults["CREDIT_CARD"][0] + results[1]
        fieldResults["CREDIT_CARD"][3] = fieldResults["CREDIT_CARD"][3] + (numCC - results[1])
    else:
        fieldResults["CREDIT_CARD"][0] = fieldResults["CREDIT_CARD"][0] + numCC
        fieldResults["CREDIT_CARD"][2] = fieldResults["CREDIT_CARD"][2] + (results[1] - numCC)
    
    if numAddress == 0 and results[2] == 0:
        fieldResults["STREET_ADDRESS"][1] = fieldResults["STREET_ADDRESS"][1] + 1
    elif numAddress == results[2]:
        #update with tp value
        fieldResults["STREET_ADDRESS"][0] = fieldResults["STREET_ADDRESS"][0] + numAddress
    elif numAddress > results[2]:
        # tp = results[2]
        # fn = numCC - results[2]
        fieldResults["STREET_ADDRESS"][0] = fieldResults["STREET_ADDRESS"][0] + results[2]
        fieldResults["STREET_ADDRESS"][3] = fieldResults["STREET_ADDRESS"][3] + (numAddress - results[2])
    else: 
        fieldResults["STREET_ADDRESS"][0] = fieldResults["STREET_ADDRESS"][0] + numAddress
        fieldResults["STREET_ADDRESS"][2] = fieldResults["STREET_ADDRESS"][2] + (results[2] - numAddress)

    if numSSN == 0 and results[3] == 0:
        fieldResults["US_SSN"][1] = fieldResults["US_SSN"][1] + 1
    if numSSN == results[3]:
        #update with tp value
        fieldResults["US_SSN"][0] = fieldResults["US_SSN"][0] + numSSN
    elif numSSN > results[3]:
        # tp = results[3]
        # fn = numCC - results[3]
        fieldResults["US_SSN"][0] = fieldResults["US_SSN"][0] + results[3]
        fieldResults["US_SSN"][3] = fieldResults["US_SSN"][3] + (numSSN - results[3])
    else:
        fieldResults["US_SSN"][0] = fieldResults["US_SSN"][0] + numSSN
        fieldResults["US_SSN"][2] = fieldResults["US_SSN"][2] + (results[3] - numSSN)

print(fieldResults)
    # break

for value in fieldResults:
    results = fieldResults[value]
    print(value)
    tp = results[0]
    tn = results[1]
    fp = results[2]
    fn = results[3]
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    print("accuracy " + str(accuracy))
    precision = 0 if (tp + fp) == 0 else tp / (tp + fp)
    print("precision" + str(precision))
    recall = 0 if (tp + fn) == 0 else tp / (tp + fn)
    print("recall " + str(recall))
    if precision == 0 and recall == 0:
        f1 = 0  # or any other default value
    else:
        f1 = 2 * (precision * recall) / (precision + recall)
    print("f1-score " + str(f1))

#accuracy = (tp + tn) / (tp + tn + fp + fn)
#precision = tp / (tp + fp)
# recall = tp / (tp + fn)
#f1-score = 2* (precision * recall)/ (precision + recall)