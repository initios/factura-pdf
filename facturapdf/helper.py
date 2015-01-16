from reportlab.lib import utils
from reportlab.lib.units import mm
from reportlab.platypus import Image


def get_image(path, width=1 * mm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)

    return Image(path, width=width, height=(width * aspect))


def chunks(collection, amount, fill_with=None):
    copy_collection = list(collection)
    chunk_list = []
    while len(copy_collection) > 0:
        total_items = amount
        chunk = []
        while total_items > 0 and len(copy_collection) > 0:
            chunk.append(copy_collection.pop(0))
            total_items -= 1

        if fill_with is not None:
            fill(chunk, amount, fill_with)

        chunk_list.append(chunk)

    return chunk_list


def fill(item, amount, fill_with):
    while len(item) < amount:
        item.append(fill_with)
