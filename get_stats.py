import requests
import argparse



def req(url):
    response = requests.get(url)

    if response.status_code == 200:
        print(response.text)
    else:
        print("Error:", response.text)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Username')
    parser.add_argument('--name', type=str, default="Fatih" , help='Database de aranacak isim ')
    args = parser.parse_args()
    username=args.name
    url = "http://localhost:5000/user_stats?username="+username
   
    req(url)
