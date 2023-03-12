from flask import Flask, render_template

from .config.config import Config
from .forms import PngToJpegConverterForm

app = Flask(__name__)
app.config.from_object(Config())


@app.route("/")
def index():
    png_to_jpeg_converter_form = PngToJpegConverterForm()
    return render_template("index.html", png_to_jpeg_form=png_to_jpeg_converter_form)


@app.route("/convert/png-to-jpeg", methods=("POST",))
def convert_png_to_jpeg():
    png_to_jpeg_converter_form = PngToJpegConverterForm()
    if png_to_jpeg_converter_form.validate_on_submit():
        out_image_uri = png_to_jpeg_converter_form.convert()
        return render_template("index.html", png_to_jpeg_form=png_to_jpeg_converter_form, out_image_uri=out_image_uri)
    return render_template("index.html", png_to_jpeg_form=png_to_jpeg_converter_form)


if __name__ == "__main__":
    app.run(debug=True)
