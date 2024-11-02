import requests
import json
import re

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
    videos: a dictionary with ids as keys and urls as values.
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