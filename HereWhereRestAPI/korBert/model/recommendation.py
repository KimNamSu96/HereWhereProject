import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import random, os
from korBert.model.chatgpt import AssistantSingleton
from korBert.model.mbti_prediction import MBTIKorBERTSingleTone
class RecommendDestination():
    def __init__(self):
        # 현재 파일의 절대 경로를 기준으로 데이터 파일 경로 생성
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 임베딩 및 데이터 로드에 사용할 경로 수정
        travel_embeddings_path = os.path.join(current_dir, '..', 'datasets', 'embeddings', 'travel_embeddings.npy')
        mbti_embeddings_path = os.path.join(current_dir, '..', 'datasets', 'embeddings', 'mbti_embeddings.npy')
        travel_data_path = os.path.join(current_dir, '..', 'datasets', 'travel_data.csv')
        mbti_recommend_data_path = os.path.join(current_dir, '..', 'datasets', 'mbti_recommend_destination.csv')

        self.travel_embeddings = np.load(travel_embeddings_path)
        self.mbti_embeddings = np.load(mbti_embeddings_path)
        self.travel_data = pd.read_csv(travel_data_path, encoding='utf-8-sig')
        self.mbti_recommend_data = pd.read_csv(mbti_recommend_data_path, encoding='utf-8-sig')

        # 기타 클래스 초기화 코드...
        self.gpt=AssistantSingleton.get_instance()
        self.model=MBTIKorBERTSingleTone.get_instance()

    def recommend_destinations_by_mbti(self, mbti_type, top_n=5):
        mbti_type = mbti_type.upper().strip()
        mbti_idxs = np.where(self.mbti_recommend_data['mbti'].str.upper().str.strip() == mbti_type)[0]

        if len(mbti_idxs) == 0:
            print(f"MBTI 유형 '{mbti_type}'에 해당하는 데이터가 없습니다.")
            return None

        mbti_idx = mbti_idxs[0]
        mbti_embedding = self.mbti_embeddings[mbti_idx].reshape(1, -1)
        similarities = cosine_similarity(mbti_embedding, self.travel_embeddings)
        sorted_idx = np.argsort(similarities[0])[::-1][:30]  # 상위 15개 추출

        # 상위 15개 중 유니크한 여행지 선택
        unique_destinations = {}
        for idx in sorted_idx:
            destination = self.travel_data.iloc[idx]['destination']
            if destination not in unique_destinations:
                unique_destinations[destination] = similarities[0][idx]

        # 유니크한 여행지 중에서 랜덤으로 최대 5개 선택
        selected_destinations = random.sample(list(unique_destinations.keys()), k=min(len(unique_destinations), top_n))

        # 선택된 여행지 및 유사도 점수, 상세 정보 출력
        print(f"MBTI 유형 '{mbti_type}'에 대한 추천 여행지 및 상세 정보:")
        recommendations = []
        for destination in selected_destinations:
            idx = self.travel_data[self.travel_data['destination'] == destination].index[0]
            score = unique_destinations[destination] * 100  # 퍼센트로 변환
            description = self.travel_data.iloc[idx]['description']
            tag = self.travel_data.iloc[idx]['tag']
            image = self.travel_data.iloc[idx]['image']
            recommendation = {
                'destination': destination,
                'tag': tag,
                'description': description,
                'image': image,
                'score': f"{score:.2f}%"
            }
            recommendations.append(recommendation)
        return recommendations

    def recommend_destinations_by_search(self, search, top_n=5):
        # GPT를 통해 검색어에 대한 텍스트 생성
        generated_texts = self.gpt.send_message(search)

        # 생성된 텍스트의 임베딩을 얻음
        search_embedding = self.model.get_embedding(generated_texts).reshape(1, -1)

        # 여행지 임베딩과의 코사인 유사도 계산
        similarities = cosine_similarity(search_embedding, self.travel_embeddings)
        sorted_idx = np.argsort(similarities[0])[::-1]  # 유사도가 높은 순서로 정렬

        # 추천 여행지 선택 (중복 제거)
        unique_destinations = {}
        for idx in sorted_idx:
            destination = self.travel_data.iloc[idx]['destination']
            if destination not in unique_destinations:
                unique_destinations[destination] = similarities[0][idx]
            if len(unique_destinations) == top_n:
                break

        # 추천 여행지 및 상세 정보 출력
        print(f"검색어 '{search}'에 대한 추천 여행지 및 상세 정보:")
        recommendations = []
        for destination, score in unique_destinations.items():
            idx = self.travel_data[self.travel_data['destination'] == destination].index[0]
            score = score * 100  # 퍼센트로 변환
            description = self.travel_data.iloc[idx]['description']
            tag = self.travel_data.iloc[idx]['tag']
            image = self.travel_data.iloc[idx]['image']
            recommendation = {
                'destination': destination,
                'tag': tag,
                'description': description,
                'image': image,
                'score': f"{score:.2f}%"
            }
            recommendations.append(recommendation)
        return recommendations

class RecommendDestinationSingleton:
    _instance = None
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RecommendDestination()
        return cls._instance