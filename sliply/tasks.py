import os
from celery import shared_task
import io
from google.cloud import vision
from google.cloud.vision import types

from .parser import get_receipt_date, get_total_amount, get_seller_name, get_payment_method, get_item
from .models import Slip
from sliply_project.settings import MEDIA_ROOT


@shared_task
def detect_text(filename, pk):
    client = vision.ImageAnnotatorClient()

    with io.open(os.path.join(MEDIA_ROOT, filename), 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    slip_text = [text.description for text in texts][0]

    slip_to_update = Slip.objects.get(pk=pk)
    slip_to_update.raw_text = slip_text
    slip_to_update.seller_name = get_seller_name(slip_text)
    slip_to_update.purchase_date = get_receipt_date(slip_text)
    slip_to_update.total_amount = get_total_amount(slip_text)
    slip_to_update.payment_type = get_payment_method(slip_text)
    slip_to_update.save()

    items_to_save = get_item(slip_text)


    return "OK"
