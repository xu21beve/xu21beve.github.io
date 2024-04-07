from flask import Flask, render_template, send_file, request
import soundfile as sf
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    audio_data = request.files['audio_data']
    audio_path = os.path.join(os.getcwd(), 'recorded_audio.wav')
    
    with open(audio_path, 'wb') as audio_file:
        audio_file.write(audio_data.read())

    # Convert to the correct format for Koala
    data, samplerate = sf.read(audio_path)
    sf.write(audio_path, data, samplerate, format='WAV', subtype='PCM_16')

    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

