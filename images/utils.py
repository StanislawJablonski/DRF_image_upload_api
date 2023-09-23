import os
import re
import time
import uuid




def sanitize_filename(filename):
    basename, ext = os.path.splitext(filename)
    basename = re.sub(r'[^\w\.]', '_', basename)
    filename = f"{basename}{ext}"
    return filename