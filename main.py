from flask import Flask, request, jsonify
import cv2
import numpy as np
from deepface import DeepFace
import tensorflow as tf
import sqlite3
import time

app = Flask(__name__)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
            tf.config.set_logical_device_configuration(gpu, [tf.config.LogicalDeviceConfiguration(memory_limit=4000)])
            logical_gpus = tf.config.list_logical_devices('GPU')
            #print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:

        print(e)


conn = sqlite3.connect("user_stats.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        model_output TEXT NOT NULL,
        execution_time REAL NOT NULL
    )
""")

conn.commit()
conn.close()

def save_model_output_to_db(username, model_output, execution_time):
            conn = sqlite3.connect("user_stats.db")
            cursor = conn.cursor()

            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                INSERT INTO user_stats (username, timestamp, model_output, execution_time)
                VALUES (?, ?, ?, ?)
            """, (username, timestamp, model_output, execution_time))

            conn.commit()
            conn.close()


@app.route('/inference', methods=['POST'])

def image_inference():
    start_time = time.time()
    try:
       
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        if 'username' not in request.files:
            return jsonify({"error": "No username provided"}), 400


        image_file = request.files['image']
        username_file = request.files['username']
        username=username_file.read().decode("utf-8")
    
        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        result= deep_face(image) #DeepFace
        end_time = time.time()
        execution_time = end_time - start_time
        save_model_output_to_db(username,result,str(execution_time))
        
        
        return jsonify({"result": "Succesfull"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/user_stats', methods=['GET'])
def get_user_stats():
    username = request.args.get('username')

    conn = sqlite3.connect("user_stats.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, model_output, execution_time
        FROM user_stats
        WHERE username=?
    """, (username,))

    result = cursor.fetchall()
    conn.close()

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

def deep_face(data):
    
    demography = DeepFace.analyze(data)
    # emotion = demography[0]['emotion']
    dominant_emotion = demography[0]['dominant_emotion']
    region = demography[0]['region']
    age = demography[0]['age']
    #gender = demography[0]['gender']
    dominant_gender = demography[0]['dominant_gender']
    # race = demography[0]['race']
    dominant_race = demography[0]['dominant_race']
    result = "Emotion =" + " " + str(dominant_emotion) + " "  + "Age =" + " "  + str(age) + " "  + "Dominant_Race =" + " "  + str(dominant_race) + " "  + 'Gender =' + " " + str(dominant_gender) 
    return result



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
