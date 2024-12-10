import requests
from urllib.parse import urljoin
from time import sleep
from ultralytics import YOLO

def koordinatYaz(box_coordinates, i):
    top_left_x = box_coordinates[i][0]
    top_left_y = box_coordinates[i][1]
    bottom_right_x = box_coordinates[i][2]
    bottom_right_y = box_coordinates[i][3]

    result = {
        "top_left_x": float("{:.2f}".format(top_left_x)),
        "top_left_y": float("{:.2f}".format(top_left_y)),
        "bottom_right_x": float("{:.2f}".format(bottom_right_x)),
        "bottom_right_y": float("{:.2f}".format(bottom_right_y))
    }
    return result

def box_contains(box1, box2):
    return (box1[0] <= box2[0] <= box1[2] and box1[1] <= box2[1] <= box1[3] and
            box1[0] <= box2[2] <= box1[2] and box1[1] <= box2[3] <= box1[3])

def get_artin():
    url = 'http://127.0.0.1:5000/artin'
    data = {"id": -1}

    while True:
        response = requests.post(url, json=data)
        re = response.json()
        print("Sunucudan gelen yanıt:", re)

        if not re:
            print("Sunucudan boş cevap alındı. Tekrar deneniyor...")
            sleep(1)
            continue

        frame = re['url']
        img_url = f"/static/images/{re['image_url']}"
        img_path = urljoin(url, img_url)

        model = YOLO("1.pt")
        results = model.predict(source=img_path)
        class_idss = results[0].boxes.cls.tolist()
        box_coordinates = results[0].boxes.xyxy.tolist()

        output_data = []
        for i, class_id in enumerate(class_idss):
            obj = {}
            if class_id in [0.0, 1.0]:
                obj["landing_status"] = "-1"
            elif class_id in [2.0, 3.0]:
                obj["landing_status"] = "1"
                for j, other_class_id in enumerate(class_idss):
                    if i != j and box_contains(box_coordinates[i], box_coordinates[j]):
                        obj["landing_status"] = "0"
                        break

            obj["class_idss"] = class_id
            coordinates = koordinatYaz(box_coordinates, i)
            obj.update(coordinates)
            output_data.append(obj)

        for obj in output_data:
            print("cls:", obj["class_idss"])
            print("landing_status:", obj["landing_status"])
            print("top_left_x:", obj["top_left_x"])
            print("top_left_y:", obj["top_left_y"])
            print("bottom_right_x:", obj["bottom_right_x"])
            print("bottom_right_y:", obj["bottom_right_y"])
            print()

        data = {
            "id": 232,
            "user": "http://localhost/users/4/",
            "frame": frame,
            "detected_objects": output_data,
            "detected_translations": [
                {
                    "translation_x": 0.02,
                    "translation_y": 0.01
                }
            ]
        }

        post_response = requests.post(url, json=data)
        print("Status Code:", post_response.status_code)
        print("Response JSON:", post_response.json())
        sleep(1)

result = get_artin()
print(result)
