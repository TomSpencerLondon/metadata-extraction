from io import BytesIO

import PIL.ExifTags
import PIL.Image
import boto3
from PIL import ExifTags

s3 = boto3.resource('s3')


def lambda_handler(event, null):
    image_object = s3.Object(event['bucket'], event['key'])
    img = PIL.Image.open(BytesIO(image_object.get()['Body'].read()))
    exif = {
        PIL.ExifTags.TAGS[k]: v for k, v in img.getexif().items() if k in PIL.ExifTags.TAGS
    }

    for k in ['UserComment', 'MakerNote']:
        if k in exif:
            del exif[k]
    gpsinfo = {}
    for key in exif['GPSInfo'].keys():
        decode = ExifTags.GPSTAGS.get(key)
        gpsinfo[decode] = exif['GPSInfo'][key]
    output = {'exif': exif, 'gpsinfo': gpsinfo}
    print(output)
    return output
