import os
from celery import shared_task
import io
from google.cloud import vision
from google.cloud.vision import types
from sliply_project.settings import MEDIA_ROOT


@shared_task
def detect_text(filename):
    client = vision.ImageAnnotatorClient()

    with io.open(os.path.join(MEDIA_ROOT, filename), 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    # for text in texts:
    #     print('\n"{}"'.format(text.description))

    return [text.description for text in texts][0]

        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in text.bounding_poly.vertices])
        #
        # print('bounds: {}'.format(','.join(vertices)))
