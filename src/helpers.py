import re


def normalize_filename(filename):
    filename = re.sub(r"\s+", "_", filename)
    filename = re.sub(r"[^\w\.-]+", "", filename)
    return filename


def convert_bytes(num):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024.0:
            return f"{num:.2f} {unit}"
        num /= 1024.0
