from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import certifi
ca = certifi.where();

from pymongo import MongoClient # [POST] 2. 코드 붙여넣기
client = MongoClient('mongodb://test:ahhyeon@ac-n9ccs4r-shard-00-00.arcitzi.mongodb.net:27017,ac-n9ccs4r-shard-00-01.arcitzi.mongodb.net:27017,ac-n9ccs4r-shard-00-02.arcitzi.mongodb.net:27017/?ssl=true&replicaSet=atlas-8qe01r-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.dbtest

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']        # [post] 1. 변수 설정
    
    # [POST] 4. 버킷리스트 전체 불러와서 count에 순번 저장!
    count = len(list(db.bucket.find({},{'_id':False})))
    
    # [POST] 3. DB에 데이터 저장
    doc = {
       'num' : count, # 버킷리스트 순번
        'bucket' : bucket_receive,
        'done':0 # 완료(1), 미완료(0)
    }

    db.bucket.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done(): # 2[GET] 1. 변수 받아오고 업데이트
    num_receive = request.form['num_give']

    # 클라이언트에서 서버로 숫자를 넘겨줘도, 서버는 문자로 받음 >>> 따라서 따로 변환필요!
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '버킷 완료!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    # [GET] 1. 서버에서 모든 데이터 가져오기
    bucket_list = list(db.bucket.find({}, {'_id':False}))
    # [GET] 2. bucket_list 담아서 클라이언트로 내려주기, 이러면 서버 끝~!
    return jsonify({'buckets':bucket_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)