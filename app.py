from flask import Flask, jsonify, request
from datetime import datetime
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "This is Home Page. Please Search Query with 'search/' for different filters."

@app.route('/search',methods=["GET"])
def get_filter():
    query_param = request.args

    search_author = query_param.get('search_author')
    at_from = query_param.get('at_from')
    at_to = query_param.get('at_to')
    like_from = query_param.get('like_from')
    like_to = query_param.get('like_to')
    reply_from = query_param.get('reply_from')
    reply_to = query_param.get('reply_to')
    search_text = query_param.get('search_text')
    
    api_url = 'https://app.ylytic.com/ylytic/test'
    response = requests.get(api_url)
    data = response.json()['comments']
    return_array = []
    for i in data:
        d1 = datetime.strptime(i['at'], "%a, %d %b %Y %H:%M:%S GMT")
        if (search_author and search_author not in i['author']) or (like_from and int(like_from)>i['like']) or (like_to and int(like_to)<=i['like']) or (reply_from and int(reply_from)>i['reply']) or  (reply_to and int(reply_to)<=i['reply']) or (search_text and search_text not in i['text']) or (at_from and datetime.strptime(at_from, "%d-%m-%Y") > d1) or (at_to and datetime.strptime(at_to, "%d-%m-%Y") < d1):
            continue
        return_array.append(i)
    return jsonify(data=return_array)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)