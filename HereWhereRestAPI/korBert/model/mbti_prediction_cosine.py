import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from mbti_prediction import MBTI_korBert

class MBTIPredictor:
    def __init__(self, model, base_embeddings_path='../datasets/embeddings/word_base_mbti_embeddings.npy'):
        # 모델과 기본 MBTI 임베딩 로드
        self.model = model
        self.base_embeddings = np.load(base_embeddings_path)
        # MBTI 유형 데이터 로드 및 인덱스 재설정
        self.mbti_data = pd.read_csv('../datasets/word_base_mbti_datasets.csv')
        self.mbti_data.reset_index(drop=True, inplace=True)  # 인덱스 재설정

    def predict(self, input_text):
        # 입력 텍스트의 임베딩 생성
        input_embedding = self.model.get_embedding(input_text)
        # 코사인 유사도 계산
        similarities = cosine_similarity(input_embedding, self.base_embeddings).flatten()
        # 가장 유사도가 높은 MBTI 유형 찾기
        max_similarity_index = np.argmax(similarities)
        predicted_mbti = self.mbti_data['mbti'].iloc[max_similarity_index]  # 수정된 접근 방식
        similarity_score = similarities[max_similarity_index]

        return predicted_mbti, similarity_score

# 예시 사용
model = MBTI_korBert() # MBTI_korBert 인스턴스 생성
predictor = MBTIPredictor(model)
input_text = '''
사람
수
유형
이
행동
것
사업가
중
가장
때
성격
일
등
때문
변화
능력
생각
현실
자신
경우
'''
predicted_mbti, similarity_score = predictor.predict(input_text)
print(f"Predicted MBTI: {predicted_mbti}, Similarity Score: {similarity_score}")
