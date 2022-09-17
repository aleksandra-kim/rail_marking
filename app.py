import tempfile

import cv2 as cv

from flask import Flask, request, render_template
from scripts.segmentation.test_one_image import interface

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def upload_file():
    image = request.files["image"]
    with tempfile.TemporaryFile() as fp:
        image.save(fp.name)
        img = cv.imread(fp.name)

        points = interface(img)
        print(points)

        return {
            "points": points,
        }
