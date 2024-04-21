from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/matrix_image", methods=["GET"])
def matrix_colors():
    with open("files/matrix_image.txt", "r") as f:
        img_len = int(f.readline())
        delay = int(f.readline())
        images = []
        for i in range(img_len):
            images.append(f.readline().replace('\n', '').split(", "))
        return render_template("matrix.html", image_len=img_len, delay=delay, images=images)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
