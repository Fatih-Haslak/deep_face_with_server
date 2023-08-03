from flask import Flask, request, jsonify
import cv2
import numpy as np
import sqlite3
import time
from utils.face_recognition import ClassDeepFace
from utils.database import ClassDataBase
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)


@app.route('/inference', methods=['POST'])
def image_inference():
    start_time = time.time()
    global face_recognition
    global db
    try:
        if 'image' and 'image_test' not in request.files:
            return jsonify({"error": "No images provided"}), 400

        if 'username' not in request.files:
            return jsonify({"error": "No username provided"}), 400


        image_file = request.files['image']
        image_file_test = request.files['image_test']
        username_file = request.files['username']
        username=username_file.read().decode("utf-8")
    
        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        image_test = cv2.imdecode(np.fromstring(image_file_test.read(), np.uint8), cv2.IMREAD_COLOR)
        result = face_recognition.run(image,image_test) #DeepFace

        end_time = time.time()
        execution_time = end_time - start_time

        db.save_model_output_to_db(username,str(result),str(execution_time)) #DataBase
        
        
        return jsonify({"result": "Succesfull"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/user_stats', methods=['GET'])
def get_user_stats():
    username = request.args.get('username')

    result=db.return_data_from_db(username=username)

    if not result:
        return jsonify(message="User not found"), 404

    stats = []
    for row in result:
        stats.append({
            "timestamp": row[0],
            "model_output": row[1],
            "execution_time": row[2]
        })

    return jsonify(stats)


if __name__ == '__main__':
    db = ClassDataBase() #DataBase
    face_recognition = ClassDeepFace() #DeepFace
    app.run(host='0.0.0.0', port=5000)
