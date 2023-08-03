import requests
import argparse
import os



def run(url:str,file_path:str,file_path_test:str,username:str):
    
    files = {'image': open(file_path, 'rb'),'image_test': open(file_path_test, 'rb'),'username': username}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        result = response.json()
        print("Result:", result["result"])

    else:
        print("Error:", response.json())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Username for DataBase')
    parser.add_argument('--name', type=str, default="Fatih" , help='UserName for Database')
    args = parser.parse_args()
    url = "http://localhost:5000/inference"

    current_dir = os.path.dirname(os.path.abspath(__file__)) #bir alt klasorun ısmı
    data_folder = os.path.abspath(os.path.join(current_dir, '..', 'data')) #data ekleyerke datalara ulas

    file_path = data_folder+"\image1.png" #arguman olarak alınacak
    file_path_test =data_folder+"\image2.png" #arguman olarak alınacak
    username=args.name
    run(url, file_path,file_path_test, username)
