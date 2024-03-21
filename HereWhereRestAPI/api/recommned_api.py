from flask_restful import Resource
from flask import request,jsonify, make_response
from korBert.model.recommendation import RecommendDestinationSingleton

class RecommendBySearch(Resource):
    def __init__(self):
        self.recommender = RecommendDestinationSingleton.get_instance()

    def post(self):
        if not request.is_json:
            return jsonify({'error': 'json 데이터가 없거나 json 형식의 데이터가 아님'}), 400

        search_query = request.json.get('search', '')
        if not search_query:
            return jsonify({'error': 'search 쿼리 필수 입력'}), 400
        print('search_query:', search_query)
        path = request.path
        if path.endswith('/recommend_by_search'):
            # 여행지 검색어에 대한 추천 실행
            recommendations = self.recommender.recommend_destinations_by_search(search_query, top_n=5)
            # 추천 결과 반환
        elif path.endswith('/recommend_by_mbti'):
            recommendations = self.recommender.recommend_destinations_by_mbti(search_query, top_n=10)
        else:
            return jsonify({'error': '잘못된 경로 요청'}), 400

        return make_response(jsonify(recommendations))