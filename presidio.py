from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

text_file = open("fraudLog.log", "r")
 
#read whole file to a string
data = text_file.read()

# Set up the engine, loads the NLP module (spaCy model by default) 
# and other PII recognizers
analyzer = AnalyzerEngine()

# Call analyzer to get results
results = analyzer.analyze(text=data,
                           entities=["EMAIL_ADDRESS", "PERSON"],
                           language='en')
print(results)

# Analyzer results are passed to the AnonymizerEngine for anonymization

anonymizer = AnonymizerEngine()

anonymized_text = anonymizer.anonymize(text=data,analyzer_results=results)

print(anonymized_text)
