import requests
from ast import literal_eval
import sys

def get_history(access_token):
    history = []
    r = requests.get(f"https://graph.facebook.com/me/posts?access_token={access_token}")
    
    if r.status_code != 200:
        print('Invalid access_token or api url.')
        sys.exit(0)
    
    r_data = literal_eval(r.text)
    data = r_data['data']
    next = r_data['paging']['next'].replace('\\', '')
    previous = r_data['paging']['previous'].replace('\\', '')
    
    for d in data:
        history.append(d)
    
    #### Begin traversing
    ## Previous nodes iteration
    previous_r_data = literal_eval(requests.get(previous).text)
    
    # Last node flag (length data array = 0)
    not_last_node = len(previous_r_data['data'])
    
    while (not_last_node):
        for d in reversed(previous_r_data['data']):
            history.insert(0, d)
        
        previous = previous_r_data['paging']['previous'].replace('\\', '')
        previous_r_data = literal_eval(requests.get(previous).text)
    
        # Last node flag (length data array = 0)
        not_last_node = len(previous_r_data['data'])
    

    ## Next nodes iteration
    next_r_data = literal_eval(requests.get(next).text)
    
    # Last node flag (length data array = 0)
    not_last_node = len(next_r_data['data'])
    
    while (not_last_node):
        for d in next_r_data['data']:
            history.append(d)
        
        next = next_r_data['paging']['next'].replace('\\', '')
        next_r_data = literal_eval(requests.get(next).text)
    
        # Last node flag (length data array = 0)
        not_last_node = len(next_r_data['data'])
    
    return history

if __name__ ==  "__main__":
    history = []
    access_token = None
    if not access_token:
        access_token = input("Enter access_token: ")

    if access_token:
        history = get_history(access_token)
    
    # Download to file
    download = input("Download to file: Y or N? ")
    if download == 'Y' or download == 'y':
        f = open("posts_history.txt", "w")
        f.write(str(history))
        print("Downloaded to file posts_history.txt.")
        f.close()

    # uncomment to check database insertion
    # history = [{'message': 'Fake data for checking script', 'created_time': '2012-12-30T18:23:09+0000', 'id': '10000_0001'}, {'created_time': '2012-12-28T05:45:07+0000', 'message': 'fake huh? yup', 'id': '10000_0002'}, {'message': 'Lại là fake data ~~', 'created_time': '2012-12-27T05:37:28+0000', 'id': '10000_0003'}, {'message': 'Still fake', 'created_time': '2012-12-21T09:37:46+0000', 'id': '10000_0004'}]

    # Insert to mongodb database
    upload = input("Upload to database: Y or N? ")
    if upload == 'Y' or upload == 'y':
        from utils.utils import *
        for d in history:
            d['_id'] = d['id']
            del d['id']
        add_data(history)
        print("Inserted into mongodb database.")

    
