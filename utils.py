import requests
import subprocess
import urllib
import os
# from urllib.parse import urlparse, parse_qs, urlencode

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



def filter_urls(urls):
    """
    Filters out urls that cannot be accessed.

    Parameters: 
    urls: a list of unfiltered urls
    
    Returns:
    videos: a list of filtered urls
    """ 
    filtered_urls = []
    invalid_urls = []
    for url in urls:
        if check_url(url):
            filtered_urls.append(url)
        else:
            invalid_urls.append(url)
               
    return filtered_urls, invalid_urls

def get_id(url):
    '''
    Takes an url and returns a string that is the video ID.

    Parameter:
    url: a string that is the YouTube url.

    Return:
    id: a string that is the video ID.
    '''
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)
    
    # Check if it's a standard YouTube URL with "v" parameter in the query
    if 'youtube.com' in parsed_url.netloc:
        query_params = urllib.parse.parse_qs(parsed_url.query)
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

    file_paths = []
    for url in urls:
        file_paths.append("./downloads/" + get_id(url) + ".mp3")

    # Run yt-dlp with the list-formatted args
    output = run_cmd(command, args)
    if output is not None:
        print("Program ran successfully.")
    else:
        print("Program encountered an error.")
    return file_paths

def generate_url(urls, timestamps):
    if len(urls) != len(timestamps):
        raise ValueError("The number of ids must match the number of timestamps.")

    # Base parameters for each video ID and timestamp
    params = []
    for url, ts in zip(urls, timestamps):
        params.append(('v', get_id(url)))
        params.append(('t', ts))

    # Add the mode parameter last
    params.append(('mode', 'solo'))

    # Construct the URL
    base_url = "http://viewsync.net/watch"
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def clean_up(file_paths):
    # Loop through the list and remove each file
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"Removed: {file_path}")
        except Exception as e:
            print(f"Error removing {file_path}: {e}")