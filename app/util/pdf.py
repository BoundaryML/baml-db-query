import base64, json
from io import BytesIO
from pdf2image import convert_from_bytes
from fastapi import UploadFile


def pdf_to_images(pdf_file):
    images = convert_from_bytes(pdf_file, dpi=300)
    return images


def image_to_base64(image):
    output = BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return base64.b64encode(output.getvalue()).decode("utf-8")


def pdf_to_image_base64(pdf_file: UploadFile):
    images = pdf_to_images(pdf_file.file.read())
    base64_strings = [image_to_base64(image) for image in images]

    # free memory
    for image in images:
        image.close()

    return base64_strings
