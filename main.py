import sys

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

def main():
    #get the api keys and url
    f = open(sys.argv[1], "r")
    Lines = list(map(lambda line: line.strip(), f.readlines()))

    authenticator = IAMAuthenticator(Lines[0])
    speech_to_text = SpeechToTextV1(
        authenticator=authenticator
    )

    speech_to_text.set_service_url(Lines[1])

    authenticator = IAMAuthenticator(Lines[2])
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2020-08-01',
        authenticator=authenticator)

    natural_language_understanding.set_service_url(Lines[3])

    transcript = speechToText(sys.argv[2], speech_to_text)
    keywordList = textToKeywords(transcript, natural_language_understanding)
    print(keywordList)

if __name__ == "__main__":
    main()