
Run script:  

>> python download_fb_posts.py  

Check data in database:  

>> python  
>> from utils.utils import *  
>> show_data()  



Running flask instance:

>> export FLASK_APP = api.py  
>> flask run  

Sample requests:  
GET http://127.0.0.1:5000/posts/search?q=<search_term>	: none exact match  
GET http://127.0.0.1:5000/posts/search?q=<search_term>&exact_match=True   : exact match