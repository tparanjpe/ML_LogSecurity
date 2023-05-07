import json
import numpy as np
from collections import defaultdict
import time
import google.cloud.dlp

def parse_val(expected, found):
    # TP TN FP FN
    if expected == 0:
        if found == 0:
            return [0,1,0,0]
        return [0,0,found,0]
    elif found >=expected:
        return [expected,0,found-expected,0]
    else:
        return [found,0,0,expected-found]

def calc_sent(expected, result):
    checkTypes = ['PERSON', 'CREDIT_CARD', 'STREET_ADDRESS','US_SSN']
    info_types = ["PERSON_NAME", "CREDIT_CARD_NUMBER", "STREET_ADDRESS",'US_SOCIAL_SECURITY_NUMBER']
    dictt = {}
    for check, info in zip(checkTypes, info_types):
        dictt[check] = parse_val(expected[check], result[info])
    return dictt


# Opening JSON file
f = open('synth_dataset_v2.json', encoding='utf-8')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
i = 0
for dictt in data:
    #print("keys: ", dictt.keys())
    for key in dictt.keys():
        #print(key, dictt[key], '\n')
        pass
    i+=1
    if i==5:
        break
print(len(data))
data = data

api_key_string="AIzaSyDpc-BqiuzjsHRnbyyM3BSTU2CU2WTAHDM"
quota_project_id="avid-elevator-385016"
dlp_client = google.cloud.dlp_v2.DlpServiceClient(client_options={"api_key": api_key_string, "quota_project_id": quota_project_id})


checkTypes = ['PERSON', 'CREDIT_CARD', 'STREET_ADDRESS','US_SSN']
info_types = [{"name": "PERSON_NAME"}, {"name":"CREDIT_CARD_NUMBER"}, {"name":"STREET_ADDRESS"},{"name":'US_SOCIAL_SECURITY_NUMBER'}]

min_likelihood = google.cloud.dlp_v2.Likelihood.LIKELIHOOD_UNSPECIFIED
max_findings = 0
include_quote = True

# Construct the configuration dictionary. Keys which are None may
# optionally be omitted entirely.
inspect_config = {
    "info_types": info_types,
    "min_likelihood": min_likelihood,
    "include_quote": include_quote,
    "limits": {"max_findings_per_request": max_findings},
}

project_id = "avid-elevator-385016"
parent = f"projects/{project_id}"


results = {}
for val in checkTypes:
    results[val] = np.array([0,0,0,0])

i = 0
for line in data:
    i = i+1
    expected = defaultdict(int)
    found = defaultdict(int)
    for span in line['spans']:
        if span["entity_type"] in checkTypes:
            expected[span["entity_type"]] = expected[span["entity_type"]] + 1
    content = line['full_text']
    #print(content.encode('ascii', errors='ignore').decode('ascii') + '\n')
    # Construct the item to inspect.
    item = {"value": content}
    response = dlp_client.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
    )
    if response.result.findings:
        for finding in response.result.findings:
            found[finding.info_type.name] = found[finding.info_type.name] + 1
    result = calc_sent(expected, found)
    for key in result.keys():
        results[key] = results[key] + np.array(result[key])
    #Limit on number of calls per minute
    if(i %50 == 0):
        time.sleep(90) 
        print(results)

print("FINAL")
print(results)
    

        

