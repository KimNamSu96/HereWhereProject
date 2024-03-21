from flask_restful import Resource,reqparse
from model.imageCompare import annotate,report
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import jsonify
import os,requests
class SearchImage(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('image',type=FileStorage, location='files')
        args=parser.parse_args()
        image_file=args['image']

        if image_file:
            filename = secure_filename(image_file.filename)
            file_path = os.path.join('upload', filename)
            image_file.save(file_path)
            descriptions, urls = report(annotate(file_path))
            address = descriptions[0]
            api_key = os.getenv('api_key')
            url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
            res = requests.get(f"{url}?query={address}&inputtype=textquery&language=ko&key={api_key}")
            res.encoding = 'utf-8'
            res.headers = {'Content-Type': 'application/json'}
            response_data = res.json()
            response_data['descriptions'] = descriptions
            return jsonify(response_data)
        else:
            return None