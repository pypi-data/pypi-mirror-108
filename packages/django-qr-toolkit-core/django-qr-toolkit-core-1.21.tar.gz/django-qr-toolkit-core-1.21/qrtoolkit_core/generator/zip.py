import io
import zipfile
from django.utils.text import get_valid_filename
from django.conf import settings

from .qr import create_qr_code


def generate_qr_zip(codes, form):
    s = io.BytesIO()

    zf = zipfile.ZipFile(s, mode='w', compression=zipfile.ZIP_DEFLATED)

    for code in codes:
        code_buffer = create_qr_code(code, form)
        filename = create_filename(code, form)
        zf.writestr(filename, code_buffer)

    zf.close()

    return s.getvalue()


def create_filename(code, form):
    filename_setting = form.cleaned_data['filename']
    ext = form.cleaned_data["kind"]
    name = f'{code.title}.{ext}'
    if filename_setting == 'envtitle':
        name = f'{settings.ENVIRONMENT}-{code.title}.{ext}'
    if filename_setting == 'basic':
        subname = code.basic_info[:200].replace(':', '_')
        name = f'{subname}.{ext}'
    if filename_setting == 'envbasic':
        subname = code.basic_info[:200].replace(':', '_')
        name = f'{settings.ENVIRONMENT}-{subname}.{ext}'
    if filename_setting == 'uuid':
        name = f'{code.short_uuid}.{ext}'
    if filename_setting == 'envuuid':
        name = f'{settings.ENVIRONMENT}-{code.short_uuid}.{ext}'

    return get_valid_filename(name)
