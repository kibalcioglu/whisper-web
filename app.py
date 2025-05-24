from flask import Flask, request
import whisper
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        model = whisper.load_model("base")
        result = model.transcribe(filepath, language="tr")

        output_text = ""
        for segment in result["segments"]:
            start = int(segment["start"])
            minutes = start // 60
            seconds = start % 60
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            output_text += f"{timestamp} {segment['text'].strip()}\n"

        return f"<pre>{output_text}</pre>"

    return '''
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit">
        </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
