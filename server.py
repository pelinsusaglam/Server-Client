from flask import Flask, jsonify, request
import random

app = Flask(__name__)

images = 1
toggle = True  

@app.route('/artin', methods=['POST'])
def artin():
    global images, toggle
    
    data = request.get_json()
    
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    image_url = f"{images:08d}.jpg"  
    hs = random.choice([0,1])
    if hs == 0:
        ts_x = None
        ts_y = None
    else:
        ts_x = round(random.uniform(0.01,0.05),2)
        ts_y = round(random.uniform(0.01,0.05),2)
    response_data = {
        "url": "/Users/pelinsusaglam/Desktop/deneme/images/",
        "image_url": image_url,
        "video_name": "ljfgpemcvkmuadhxabwn_V2_1",
        "session": "http://localhost/session/2/",
        "translation_x": ts_x,
        "translation_y": ts_y,
        "health_status": hs
    }
    
    if toggle:
        images += 1
        print(data)  
    toggle = not toggle  
    

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

