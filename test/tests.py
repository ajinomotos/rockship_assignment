import pytest
import requests
from ast import literal_eval

from ..utils.utils import *


def test_status_code_200():
	r = requests.get("http://127.0.0.1:5000/posts/search?q=like")
	assert(r.status_code == 200)

def test_status_code_400():
	r = requests.get("http://127.0.0.1:5000/posts/search")
	assert(r.status_code == 400)

def test_add_data():
	errors = 0
	count = count_data()
	datum = {"message": "kappa",
			 "created_time": "2020-10-05T12:03:30+00:00"}

	inserted_id = add_datum(datum)
	datum["_id"] = inserted_id

	if not count_data() == (count+1):
		errors += 1
	if not (datum == find_datum({"_id": inserted_id})):
		errors += 1

	# Clean up
	clear_collection()

	assert errors == 0
	

def test_api_search_found():
	# Add data
	data = [{"message": "i like cats",
			 "created_time": "2010-10-05T12:03:30+00:00"},
			{"message": "i've taken a liking for cats",
			"created_time": "2011-10-06T12:03:30+00:00"},
			{"message": "i liked cats",
			"created_time": "2012-11-06T12:03:30+00:00"},
			{"message": "i dislike cats",
			"created_time": "2014-11-06T12:03:30+00:00"}]

	add_data(data)

	# Calling api
	q = "like"
	r = requests.get(f"http://127.0.0.1:5000/posts/search?q={q}")
	requests_data = literal_eval(r.text)['data']

	# Checking for erros
	errors = 0

	if not {"content": "i like cats"} in requests_data:
		errors += 1
	if not {"content": "i liked cats"} in requests_data:
		errors += 1
	if not {"content": "i dislike cats"} in requests_data:
		errors += 1

	# Clean up
	clear_collection()
	assert errors == 0

def test_api_search_exact_found():
		# Add data
	data = [{"message": "i like cats",
			 "created_time": "2010-10-05T12:03:30+00:00"},
			{"message": "i've taken a liking for cats",
			"created_time": "2011-10-06T12:03:30+00:00"},
			{"message": "i liked cats",
			"created_time": "2012-11-06T12:03:30+00:00"},
			{"message": "i dislike cats",
			"created_time": "2014-11-06T12:03:30+00:00"}]

	add_data(data)

	# Calling api
	q = "like"
	r = requests.get(f"http://127.0.0.1:5000/posts/search?q={q}&exact_match=True")
	requests_data = literal_eval(r.text)['data']

	# Checking for erros
	errors = 0

	if not {"content": "i like cats"} in requests_data:
		errors += 1
	if {"content": "i liked cats"} in requests_data:
		errors += 1
	if {"content": "i dislike cats"} in requests_data:
		errors += 1

	# Clean up
	clear_collection()
	assert errors == 0

def test_api_search_not_found():
	# Add data
	data = [{"message": "i like cats",
			 "created_time": "2010-10-05T12:03:30+00:00"},
			{"message": "i've taken a liking for cats",
			"created_time": "2011-10-06T12:03:30+00:00"},
			{"message": "i liked cats",
			"created_time": "2012-11-06T12:03:30+00:00"},
			{"message": "i dislike cats",
			"created_time": "2014-11-06T12:03:30+00:00"}]

	add_data(data)

	# Calling api
	q = "dogs"
	r = requests.get(f"http://127.0.0.1:5000/posts/search?q={q}")
	requests_data = literal_eval(r.text)['data']

	# Clean up
	clear_collection()

	# Checking for erros
	assert len(requests_data) == 0