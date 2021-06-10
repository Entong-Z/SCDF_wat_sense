import sys
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

authenticator = IAMAuthenticator(APIKEY)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator)

natural_language_understanding.set_service_url(URL)

f = open(sys.argv[1], "r")

response = natural_language_understanding.analyze(
    text=f.read(),
    features=Features(
        # entities=EntitiesOptions(emotion=True, sentiment=True, limit=10),
        keywords=KeywordsOptions(limit=10))).get_result()

keywordList = []
for i in response["keywords"]:
    # print(i["text"])
    keywordList.append(i["text"])

print(keywordList)
