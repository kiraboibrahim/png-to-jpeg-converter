import io
import base64
from PIL import Image

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileSize, FileField

from .config.config import Config


class PngToJpegConverterForm(FlaskForm):
    png_image = FileField("Image", validators=[FileRequired(), FileAllowed(["png"], "Only png images"),
                                               FileSize(Config.MAX_FILE_UPLOAD_SIZE)])

    def convert(self) -> str:
        """Convert the png_image to jpeg in memory
        Should only be invoked when the form is valid

        Returns:
            str: base64 representation of the jpeg image
        """
        png_image_file = self.png_image.data  # This is a werkzeug FileStorage object
        in_buffer = io.BytesIO(png_image_file.read())
        data_uri = "data:image/jpeg;base64,{data}"
        with io.BytesIO() as out_buffer:
            with Image.open(in_buffer) as in_image:
                if in_image.mode in ("RGBA", "P"):
                    in_image = in_image.convert("RGB")  # Convert to RGB mode
                in_image.save(out_buffer, format="jpeg")
            out_buffer.seek(0)  # Position file cursor back to beginning of file since saving image moves cursor to end
            data_uri = data_uri.format(data=base64.b64encode(out_buffer.read()).decode("utf-8"))
        
        png_image_file.close()
        return data_uri
