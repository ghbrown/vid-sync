import requests
import json
import subprocess

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



def run_cmd(cmd, args):
    """
    Runs a command-line program with the specified arguments.
    
    Parameters:
    cmd (str): The command to run (e.g., "some_program")
    args (list): A list of arguments to pass to the command.
    
    Returns:
    str: The output from the command execution.
    """
    try:
        # Run a and capture its output
        result = subprocess.run([cmd] + args, capture_output=True, text=True, check=True)
        print("Command output:", result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e.stderr}")
        return None
    
def get_audio(urls, quality=0):
    """
    Obtains a list of YouTube video links and downloads the best available quality audio tracks.

    Parameters:
    urls: a list of strings of YouTube links.
    quality: specifies the quality of the audio track. Default is 0 (highest).

    Returns:
    str: The output from the command execution.
    """
    command = 'yt-dlp'

    # Build args as a list for subprocess.run()
    args = ["-x", "--audio-format", "mp3", "--audio-quality", str(quality), "--postprocessor-args", "ffmpeg:-t 3600", "-o", "./downloads/%(id)s.%(ext)s"]

    # Add URLs to the end of the args list
    args.extend(urls)

    # Run yt-dlp with the list-formatted args
    output = run_cmd(command, args)
    if output is not None:
        print("Program ran successfully.")
    else:
        print("Program encountered an error.")
    return output

    

