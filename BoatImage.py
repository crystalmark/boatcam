from PIL import Image
import picamera
import time
import piexif
import io
from datetime import datetime


class CaptureError:
    def __init__(self, message):
        self.message = message


class BoatImage:
    def click(self, position):
        try:
            stream = io.BytesIO()
            with picamera.PiCamera() as camera:
                # camera.resolution = (1960, 1080)
                # camera.resolution = (1280, 720)
                camera.rotation = 180
                camera.start_preview()
                time.sleep(2)
                camera.capture(stream, format='jpeg')
            # "Rewind" the stream to the beginning so we can read its content
            stream.seek(0)
            image = Image.open(stream)
            if image is None:
                raise CaptureError("Unable to find position")

            if position.has_fix():
                exif_bytes = self.create_exif(image, position)
                return self.save(image, exif_bytes, position.timestamp)
            else:
                return self.save(image, None, datetime.today().isoformat())
        except Exception as e:
            print("Unable to capture image from camera")
            print(e)
            return None

    @staticmethod
    def create_exif(image, position):
        exif_dict = piexif.load(image.info["exif"])

        exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = position.latitude_ref()
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = position.abs_latitude()
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = position.longitude_ref()
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = position.abs_longitude()
        return piexif.dump(exif_dict)

    @staticmethod
    def save(image, exif_bytes, timestamp):
        new_file = "cam" + timestamp + ".jpg"
        if exif_bytes is not None:
            image.save(new_file, "jpeg", exif=exif_bytes)
        else:
            image.save(new_file, "jpeg")
        return new_file
