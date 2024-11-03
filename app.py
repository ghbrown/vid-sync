from flask import Flask, render_template, request, jsonify
import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_urls', methods=['POST'])
def process_data():
    urls = request.get_json()
    video_sync_url = main.generate_playback(urls)
    result = {"message": video_sync_url}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
