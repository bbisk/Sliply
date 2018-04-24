import os
import io

from celery import shared_task
from google.cloud import vision
from google.cloud.vision import types

from .parser import get_receipt_date, get_total_amount, get_seller_name, get_payment_method, get_items, get_item_content
from .models import Slip, Item
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
    if slip_text:
        parse_text(slip_text, pk)
        return "Sent to parser"
    else:
        return None

@shared_task
def parse_text(slip_text, pk, get_action=None):
    slip_to_update = Slip.objects.get(pk=pk)

    if get_action != 'rescan':
        if slip_text:
            slip_to_update.raw_text = slip_text
            slip_to_update.seller_name = get_seller_name(slip_text)
            slip_to_update.purchase_date = get_receipt_date(slip_text)
            slip_to_update.total_amount = get_total_amount(slip_text)
            slip_to_update.payment_type = get_payment_method(slip_text)
            slip_to_update.save()

    items_to_save = get_items(slip_text)
    items_raw_only = get_item_content(slip_text)

    if items_to_save:
        if get_action == 'rescan':
            items_to_overwrite = Item.objects.filter(slip=slip_to_update)
            items_to_overwrite.delete()

        for item in items_to_save:
            if len(item) == 4:
                Item.objects.create(
                    owner=slip_to_update.owner,
                    slip=slip_to_update,
                    raw_text=item[1],
                    item_name=item[0],
                    quantity = float(item[2]),
                    price = float(item[3])
                )
            elif len(item) == 3:
                Item.objects.create(
                    owner=slip_to_update.owner,
                    slip=slip_to_update,
                    raw_text=item[1],
                    item_name=item[0],
                    price=float(item[2])
                )
    else:
        if items_raw_only:
            items_raw_list = items_raw_only.strip().split("\n")
            for item_raw in items_raw_list:
                Item.objects.create(
                    owner=slip_to_update.owner,
                    slip=slip_to_update,
                    raw_text=item_raw,
                    item_name=item_raw,
                )
        else:
            return None

