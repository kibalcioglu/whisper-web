from flask import Flask, request
import whisper
import os

app = Flask(__name__)
model = whisper.load_model("tiny")
print("🎯 Yüklenen model boyutu:", os.path.getsize(model.model_path) / 1024 / 1024, "MB")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
