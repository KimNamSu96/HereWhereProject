#pip install CORS flask_restful Flask werkzeug requests amadeus selenium bs4 pillow aiohttp aiofiles google-cloud-vision google-cloud-translate PyPDF2 forex-python pandas uvicorn uvicorn flask_cors
# 설치 라이브러리
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from api.google_hotel_crawling_api import Hotel_Crawling
from api.google_hotel_api import Hotel
from api.google_restaurant_api import Restaurant
from api.google_attraction_api import Attraction
from api.SearchImage import SearchImage
from api.booking_api import Booking
from api.flight_api import Flight
from api.coolsms import Coolsms
from api.images_gpt import Images
from api.kakao import Kakao
from api.youtube_api import Youtube
from api.currency_api import CurrencyApi
from api.image_ocr import ImageOcr
from api.imageDetection_api import ImageDetection
from api.is_ocr_image import isOcrImage
from api.flight_booking_api import FlightBooking
from api.weather_api import Weather
from api.news_api import News
from api.overseas_popular_api import Overseas
from api.korea_popular_api import Korea
from api.assistant_api import AssistantResource
from api.recommned_api import RecommendBySearch
from api.sentiment_analysis import SentimentAnalysis
from api.predict_mbti_api import PredictAPI

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(SearchImage,'/searchImage')
api.add_resource(Hotel,'/hotel')
api.add_resource(Hotel_Crawling,'/hotel_crawling')
api.add_resource(Restaurant,'/restaurant')
api.add_resource(Attraction,'/attraction')
api.add_resource(Booking,'/booking')
api.add_resource(Flight,'/flights_list')
api.add_resource(Coolsms, '/coolsms')
api.add_resource(Images, '/images_gpt')
api.add_resource(Kakao,'/kakao')
api.add_resource(Youtube,'/youtube')
api.add_resource(CurrencyApi,'/currency_list','/current_currency')
api.add_resource(ImageOcr,'/imageOcr')
api.add_resource(ImageDetection,'/image_detecton')
api.add_resource(isOcrImage,'/is_ocr_image')
api.add_resource(FlightBooking,'/airports_list','/searchFlight')
api.add_resource(Weather,'/weather')
api.add_resource(News,'/news')
api.add_resource(Overseas,'/overseas')
api.add_resource(Korea,'/korea')
api.add_resource(AssistantResource,'/assistant')
api.add_resource(RecommendBySearch, '/recommend_by_search', endpoint='recommend_by_search')
api.add_resource(RecommendBySearch, '/recommend_by_mbti', endpoint='recommend_by_mbti')
api.add_resource(SentimentAnalysis, '/sentiment_analysis')
api.add_resource(PredictAPI, '/predict_mbti')



if __name__ == '__main__':
    app.run(debug=True)