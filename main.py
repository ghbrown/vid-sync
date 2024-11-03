import utils
import processor

def generate_playback(urls, keep=False):
    error_msg = ""

    # Filter out invalid urls
    (filtered_urls, invalid_urls) = utils.filter_urls(urls)

    if not invalid_urls:
        error_msg += "Some of the URLs are not valid. They have been removed from the list."

    # Obtain downloaded file paths
    file_paths = utils.get_audio(filtered_urls)

    # Obtain timestamps
    timestamps = processor.resolve_lags(file_paths,1000)

    # Generate url compatible with ViewSync website
    viewsync_url = utils.generate_url(urls, timestamps)

    # Clean up files if not keeping
    if not keep:
        utils.clean_up(file_paths)

    return viewsync_url