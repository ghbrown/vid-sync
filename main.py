import utils
import processor

def generate_playback(urls):
    error_msg = ""

    # Filter out invalid urls
    (filtered_urls, invalid_urls) = utils.filter_urls(urls)

    if not invalid_urls:
        error_msg += "Some of the URLs are not valid. They have been removed from the list."

    file_paths = utils.get_audio(filtered_urls)

    timestapms = processor.resolve_lags(file_paths)

    viewsync_url = utils.generate_url(urls, timestapms)


    



    return viewsync_url