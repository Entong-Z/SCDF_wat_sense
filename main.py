import sys
import math
import pandas as pd
from collections import Counter
import datetime

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions


def speechToText(audio_file, model):
    speech_recognition_results = model.recognize(
        audio=open(audio_file, "rb"),
        # content_type='audio/wav',
        # word_alternatives_threshold=0.9,
        # keywords=['colorado', 'tornado', 'tornadoes'],
        # keywords_threshold=0.5
    ).get_result()

    transcript = speech_recognition_results["results"][0]["alternatives"][0]["transcript"]
    return transcript

def textToKeywords(txt, model):
    response = model.analyze(
        text=txt,
        features=Features(
            keywords=KeywordsOptions(limit=10))
            ).get_result()

    keywordList = []
    for i in response["keywords"]:
        keywordList.append(i["text"])

    return keywordList

def getSTTmodel(apikey, url):
    authenticator = IAMAuthenticator(apikey)
    speech_to_text = SpeechToTextV1(
        authenticator=authenticator
    )

    speech_to_text.set_service_url(url)
    return speech_to_text

def getNLPmodel(apikey, url):
    authenticator = IAMAuthenticator(apikey)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2020-08-01',
        authenticator=authenticator)

    natural_language_understanding.set_service_url(url)
    return natural_language_understanding

def counter_cosine_similarity(listA, listB):
    c1 = Counter(listA)
    c2 = Counter(listB)
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

def main():
    #get the api keys and url
    f = open(sys.argv[1], "r")
    Lines = list(map(lambda line: line.strip(), f.readlines()))

    #get the dataframe from pickle file
    df = pd.read_pickle("df.pkl")

    #get current time
    time = datetime.datetime.now().strftime("%X")

    #get the models
    speech_to_text = getSTTmodel(Lines[0], Lines[1])
    natural_language_understanding = getNLPmodel(Lines[2], Lines[3])

    #extract keywords from audio file
    transcript = speechToText(sys.argv[2], speech_to_text)
    keywordList = textToKeywords(transcript, natural_language_understanding)

    #check if audio is new or repeated
    event_type = "new"
    event_id = len(df)
    if len(df) != 0:
        # compare each row
        for index, row in df.iterrows():
            if counter_cosine_similarity(keywordList, row["Keywords"]) > 0.6:
                event_type = "repeated"
                event_id = row["Event ID"]
                break

    # append new row
    row = [time, keywordList, event_type, event_id]
    df.loc[len(df)] = row       


    print(df)
    df.to_pickle("df.pkl")
    return

if __name__ == "__main__":
    main()