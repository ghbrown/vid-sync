import subprocess

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

    

