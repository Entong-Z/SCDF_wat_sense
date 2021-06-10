#######################
# TexttoKeyword part
#######################
# import sys
# import json
# from ibm_watson import NaturalLanguageUnderstandingV1
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

# authenticator = IAMAuthenticator(APIKEY)
# natural_language_understanding = NaturalLanguageUnderstandingV1(
#     version='2020-08-01',
#     authenticator=authenticator)

# natural_language_understanding.set_service_url(URL)

# f = open(sys.argv[1], "r")

# response = natural_language_understanding.analyze(
#     text=f.read(),
#     features=Features(
#         # entities=EntitiesOptions(emotion=True, sentiment=True, limit=10),
#         keywords=KeywordsOptions(limit=10))).get_result()

# keywordList = []
# for i in response["keywords"]:
#     # print(i["text"])
#     keywordList.append(i["text"])


##############
# Store in df
##############
import math
import pandas as pd
from collections import Counter

new_list = keywordsList

df = pd.read_pickle("df.pkl")

def counter_cosine_similarity(listA, listB):
    c1 = Counter(listA)
    c2 = Counter(listB)
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

event_type = "new"
# event_id = df[len(df)]["event_id"] + 1 #how?

if len(df) != 0:
    # compare each row
    for index, row in df.iterrows():
        if counter_cosine_similarity(new_list, row["keywords"]) > 0.7:
            event_type = "repeated"
            #event_id = row["event_id"]
            break

# append new row
row = [new_list, event_type]
df.loc[len(df)] = row       


print(df)
df.to_pickle("df.pkl")
