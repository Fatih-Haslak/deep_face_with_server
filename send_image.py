import requests
import argparse
import cv2


def run(url,file_path,username):
    
    #files = {'image': ('image.png', file_path), 'username': username}
    files = {'image': open(file_path, 'rb'),'username': username}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        
        result = response.json()
        print("Result:", result["result"])
        exit()
    else:
        print("Error:", response.json())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='İsme göre selam veren betik')
    parser.add_argument('--name', type=str, default="Fatih" , help='Merhaba denilecek isim')
    args = parser.parse_args()
    url = "http://localhost:5000/inference"
    
    #file_path = ".\image1.png"
    username=args.name
    cap = cv2.VideoCapture(0)

    while True:
        # Kameradan bir kare alalım
        ret, frame = cap.read()

        # Kameradan başarılı bir şekilde kare alındıysa, bunu gönderelim
        if ret:
            cv2.imwrite(username+".jpg", frame)
            run(url, username+".jpg", username)

        # Çıkış için q tuşuna basın
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kamerayı kapat
    cap.release()
    cv2.destroyAllWindows()
    
