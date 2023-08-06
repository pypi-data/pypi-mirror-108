import os
from bytesviewapi import BytesviewApiClient 
import unittest

class test_bytesviwapi(unittest.TestCase):
    def setUp(self):
        # your private API key.
        key = os.environ.get("PYTEST_TOKEN")
        self.api = BytesviewApiClient(key)

    def test_sentiment_api(self):
        response = self.api.sentiment_api(data = {"key1": "this is my favourite food"}, lang = "en")

        self.assertEqual(response['results']['key1']['label'], 2)

    def test_emotion_api(self):
        response = self.api.emotion_api(data = {"key1": "this is good"}, lang = "en")

        self.assertEqual(response['results']['key1']['label'], 2)

    def test_keywords_api(self):
        response = self.api.keywords_api(data = {"key1": "Apple hasn't announced anything"}, lang = "en")

        self.assertEqual(str(response['results']['key1']['tags'][0]), "Apple")

    def test_semantic_api(self):
        response = self.api.semantic_api(data = {"string1": "this is good", "string2": "this is good"}, lang = "en")
        
        self.assertEqual(response['results']['score'], 100)
        

    def test_name_gender_api(self):
        response = self.api.name_gender_api(data = {"key1": "ron"})
        
        self.assertEqual(str(response['results']['key1']['gender']), "M")

    def test_ner_api(self):
        response = self.api.ner_api(data = {"key1": "Mauritania and the IMF agreed Poverty Reduction arrangement"}, lang = "en")
        self.assertEqual(str(response['results']['key1']['name'][0]), 'Mauritania')
    
    def test_intent_api(self):
        response = self.api.intent_api(data = {"key1": "please subscribe to our channel"}, lang = "en")
        
        self.assertEqual(response['results']['key1']['label'], 2)

    def test_feature_api(self):
        response = self.api.feature_api(data = {"key1": "This is probably one of the funniest films of the 1980's. Eddie Murphy does a fine job as con man Billy Ray and Dan Ackroyd is great as Louis."}, lang = "en")
        
        self.assertEqual(response['results']['key1']['review'][0], "funniest")

    def test_topic_api(self):
        response = self.api.topic_api(data = {"key1": "Accounting"}, lang = "en")
        
        self.assertEqual(response['results']['key1']['label_key'], 0)