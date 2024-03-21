from flask import request, jsonify
from flask_restful import Resource
import pandas as pd
import os
import logging
from korBert.model.mbti_prediction import MBTIKorBERTSingleTone
# 로거 설정
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

class PredictAPI(Resource):
    def __init__(self):
        self.model = MBTIKorBERTSingleTone.get_instance()
        # 현재 파일의 절대 경로
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 프로젝트 루트 경로 계산
        project_root = os.path.dirname(current_dir)
        # 프로젝트 루트를 기준으로 데이터셋 파일 경로 설정
        mbti_datasets_path = os.path.join(project_root, 'korBert', 'datasets', 'mbti_recommend_destination.csv')
        self.mbti_datasets = pd.read_csv(mbti_datasets_path, encoding='utf-8')

    def post(self):
        if not request.is_json:
            logger.error('json 데이터가 없거나 json 형식의 데이터가 아님')
            return {'error': 'json 데이터가 없거나 json 형식의 데이터가 아님'}, 400

        texts_query = request.json.get('answers', '')
        if not texts_query:
            logger.error('texts 필드가 필요함')
            return {'error': 'texts 필드가 필요함'}, 400
        logger.debug('texts_query: %s', texts_query)
        predict_data = self.model.predict_mbti(' '.join(texts_query))
        logger.debug('mbti: %s', predict_data)
        mbti=predict_data['mbti'].upper()
        filtered_data = self.mbti_datasets[self.mbti_datasets['mbti'] == mbti]
        if filtered_data.empty:
            logger.warning(f'{mbti}에 해당하는 데이터가 없습니다.')
            return {'message': f'{mbti}에 해당하는 데이터가 없습니다.'}, 404

        result = filtered_data.to_dict(orient='records')[0]
        result['probability']=predict_data['probability']
        logger.debug('result: %s', result)

        return jsonify(result)