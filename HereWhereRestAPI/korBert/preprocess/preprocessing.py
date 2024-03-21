import re

#텍스트 전처리
def preprocess_text(text):
    # HTML 태그 제거
    text = re.sub(r'<.*?>', '', text)
    # 대괄호 및 중괄호 내용 제거
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\{.*?\}', '', text)
    # 특수 문자 제거
    re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", text)
    # 연속된 공백 제거
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', ' ', text)
    return text.strip()