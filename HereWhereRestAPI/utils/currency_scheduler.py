import pandas as pd
from datetime import datetime
import os
import requests
import logging
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(filename='error.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # 환경 변수 로드
    load_dotenv()
    # 데이터 파일 경로 설정
    filename = os.path.join('..', 'data', 'currency_dataset_date.csv')
    # DataFrame 로드
    currency_df = pd.read_csv(filename, encoding='utf-8-sig')
    # 현재 날짜 문자열 생성
    current_date_str = datetime.now().strftime('%Y.%m.%d')
    # current_date_str = '2024.02.23'

    API_KEY = os.getenv('RAPID_API_KEY')
    API_HOST = os.getenv('CURRENCY_LIST_RAPID_API_HOST')
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    params = {'base': 'KRW'}
    # 특정 날짜의 환율
    # url = 'https://currency-conversion-and-exchange-rates.p.rapidapi.com/2024-02-23'
    #가장 최근 환율
    url = 'https://currency-conversion-and-exchange-rates.p.rapidapi.com/latest'


    response = requests.get(url, headers=headers, params=params)

    # 로그 파일에 상태 코드와 응답 JSON 기록
    logging.info(f"Status Code: {response.status_code}")
    logging.info(f"Response JSON: {response.json()}")

    rates = response.json().get('rates', {})
    # 수집된 환율 데이터를 DataFrame에 추가
    rows = []
    for code, rate in rates.items():
        if code in currency_df['CURRENCY_CODE'].values:
            currency_df.loc[currency_df['CURRENCY_CODE'] == code, current_date_str] = 1 / float(rate)
        else:
            rows.append({'CURRENCY_CODE': code, current_date_str: 1 / float(rate)})

    if rows:
        new_df = pd.DataFrame(rows)
        currency_df = pd.concat([currency_df, new_df], ignore_index=True)

    # 수정된 DataFrame을 CSV 파일로 저장
    currency_df.to_csv(filename, index=False, encoding='utf-8-sig')
except Exception as e:
    logging.exception("Error occurred")
