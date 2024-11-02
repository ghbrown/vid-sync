import requests
import json
import re
from urllib.parse import urlparse, parse_qs

def check_url(url):
    '''
    Checks if a given YouTube url is valid and accessible.

    Parameter: 
    url: a string that is the YouTube url.

    Returns:
    valid: a boolean that returns True if the url is valid.
    '''
    response = requests.get(url)
    # Check if the status code is 200
    if response.status_code == 200:
        print("The YouTube video is accessible.")
        valid = True
    elif response.status_code == 403:
        print("The video might be private or restricted.")
        valid = False
    elif response.status_code == 404:
        print("The video URL is invalid or the video has been removed.")
        valid = False
    else:
        print(f"Encountered an unexpected error. Status code: {response.status_code}")
        valid = False
    
    return valid



def extract_urls(file_name):
    """
    Extracts information of videos from a .json file.

    Parameters: 
    file_name: name of the .json file

    Returns:
    videos: a list of urls
    """ 
    videos = []
    with open(file_name, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        
        # Assuming 'urls' is an array of objects with 'url' property
        if 'videos' in json_data and isinstance(json_data['videos'], list):
            for item in json_data['videos']:
                if 'url' in item:
                    if check_url(item['url']):
                        videos.append(item['url'])
                    else: 
                        print("Invalid video url: " + item['url'])
               
    return videos

def get_id(url):
    '''
    Takes an url and returns a string that is the video ID.

    Parameter:
    url: a string that is the YouTube url.

    Return:
    id: a string that is the video ID.
    '''
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Check if it's a standard YouTube URL with "v" parameter in the query
    if 'youtube.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if 'v' in query_params:
            return query_params['v'][0]
    # Check for youtu.be short URL format
    elif 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.lstrip('/')
    
    # In case no video ID found
    return None