from flask_restful import Resource, reqparse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import re
import json
from keras_preprocessing.text import tokenizer_from_json
from kiwipiepy import Kiwi

class SentimentAnalysis(Resource):
    def __init__(self):
        self.model = load_model('model/best_model.h5')
        self.tokenizer = self._load_tokenizer("model/tokenize.json")  # tokenizer를 저장한 json 파일을 로드. 만약에 파일명이 다르다면, 수정하세요.
        self.max_len = 75
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('sentence', type=str)

    def _load_tokenizer(self, filename):
        with open(filename, 'r') as f:
            json_data = json.load(f)
        tokenizer = tokenizer_from_json(json_data)
        return tokenizer

    def _tokenizing(self, sentence):
        kiwi = Kiwi()
        stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']
        words = [token[0] for token in kiwi.tokenize(sentence) if token[0] not in stopwords]
        return words

    def post(self):
        args = self.parser.parse_args()
        new_sentence = args['sentence']
        new_sentence = re.sub('r[^ㄱ-ㅎㅏ-ㅣ가-힣]', '', new_sentence)
        new_sentence = self._tokenizing(new_sentence)
        encoded = self.tokenizer.texts_to_sequences([new_sentence])
        pad_new = pad_sequences(encoded, maxlen = self.max_len)
        score = float(self.model.predict(pad_new))
        neg = (1 - score) * 100  # 부정 확률 계산

        if score > 0.5:
            if score > 0.8:
                result = 5
            elif score > 0.6:
                result = 4
            else:
                result = 3
            return {"result": result, "probability": round(score*100, 2) ,"sentiment": "긍정"}
        else:
            if neg > 90:
                result = 1
            elif neg > 80:
                result = 2
            else:
                result = 3
            return {"result": result, "probability": round(neg, 2) ,"sentiment":"부정"}