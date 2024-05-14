from flask import Flask, render_template, request, send_file
import os
import json

app = Flask(__name__)

# Function to convert JSON subtitles to SRT format
def json_to_srt(subtitles):
    srt_content = ''
    count = 1
    for subtitle in subtitles:
        start_time = subtitle['timestamp'][0]
        end_time = subtitle['timestamp'][1]
        text = subtitle['text']
        srt_content += f"{count}\n"
        try:
            srt_content += f"{convert_to_srt_time(start_time)} --> {convert_to_srt_time(end_time)}\n"
        except:
            pass
        srt_content += f"{text}\n\n"
        count += 1
    return srt_content

# Function to convert time in seconds to SRT format (HH:MM:SS,mmm)
def convert_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_srt', methods=['POST'])
def generate_srt():
    # Get the Google Drive link from the form
    google_drive_link = request.form['google_drive_link']

    # Assuming the file is in JSON format
    try:
        # Download the JSON file from the Google Drive link (you need to implement this)
        # Here, I assume the JSON file is named 'audio_description.json'
        # Replace this with the code to download the file
        json_file_path = '/content/drive/MyDrive/WhisperVideo/TextFiles/audio_description.json'

        # Read JSON data from the file
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # Extract subtitles from JSON data
        subtitles = data["chunks"]

        # Convert subtitles to SRT format
        srt_content = json_to_srt(subtitles)

        # Save the SRT content to a temporary file
        srt_file_path = '/tmp/output.srt'
        with open(srt_file_path, 'w') as f:
            f.write(srt_content)

        # Return the SRT file for download
        return send_file(srt_file_path, as_attachment=True, attachment_filename='output.srt')
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
