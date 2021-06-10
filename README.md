# SCDF_wat_sense

## Technologies Used
IBM Speech to Text 

IBM Natural Language Understanding

## Installation
run the following commands in the terminal

````bash
pip install ibm_watson
````

## Usage
Create IBM cloud account.

Add Speech to Text and Natural Language Understanding services to resources

Open API_keys_URL.txt and replace the words with relevant API keys and URLs

Run the following commands to create a dataframe

````bash
python createdf.py
````

Run the following commands to add an audio file to the dataframe

````bash
python main.py API_KEY_URL.txt PATH_TO_AUDIO_FILE
````

## Description
Wat-Sense is a product to reduce the workload of operation centres in the event of multiple calls to the same emergency by identifying repeated calls.

When a call is received by the operation centre, it is recorded into an audio file.

The audio file will go through the IBM Speech to Text model and be transcribed into text. 

The text generated will then go through the IBM Natural Language Understanding model to identify a list of keywords in the call.

Using the list of keywords, Wat-Sense will run a Cosine-similarity check against previous calls to identify calls relating to the same emergency.

Similar calls will be grouped together under the same Event ID and be given a type of repeated.

Repeated calls may be automatically replied to to reduce the workload of operation centres.
