import random
import string
import tempfile

import cv2 as cv

from flask import Flask, request, render_template, redirect
from scripts.segmentation.test_one_image import interface, image2image

app = Flask(__name__)


def random_filename():
    "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


@app.route("/detect", methods=["GET"])
def index():
    return render_template("detect.html", action="/detect")


@app.route("/detect", methods=["POST"])
def upload_file():
    image = request.files["image"]

    path = "uploads/" + random_filename()
    image.save(path)

    img = cv.imread(path)
    points = interface(img)
    print(points)

    return {
        "points": points,
    }


@app.route("/detect/preview", methods=["GET"])
def index():
    return render_template("detect.html", action="/detect/preview")


@app.route("/detect/preview", methods=["POST"])
def upload_file():
    image = request.files["image"]

    filename = random_filename()
    path = "uploads/" + filename
    image.save(path)

    img = cv.imread(path)
    img_out = image2image(img)

    path_out = "static/" + filename
    cv.imwrite(path_out, img_out)

    return redirect(path_out)
