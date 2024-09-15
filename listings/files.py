import os
import uuid
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile


def handle_images(uploaded_file):
    image = Image.open(uploaded_file)
    image = image.resize((800, 800), Image.Resampling.LANCZOS)

    ext = os.path.splitext(uploaded_file.name)[1]
    file_name = f'{str(uuid.uuid4())[:13]}{ext}'

    image_io = BytesIO()

    image_format = image.format if image.format else 'PNG'
    image.save(image_io, format=image_format)

    return ContentFile(image_io.getvalue(), name=file_name)


def handle_pdfs(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1]
    file_name = f'{str(uuid.uuid4())[:13]}{ext}'

    uploaded_file.name = file_name
    return uploaded_file
