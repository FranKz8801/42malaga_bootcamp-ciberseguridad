import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS
def scorpion(*files):
    for file in files:
        try:
            with Image.open(file) as img:
                exif_data = img._getexif()
                if exif_data:
                    print(f"Datos de metadatos para el archivo: {file}")
                    for tag_id in exif_data:
                        tag_name = TAGS.get(tag_id, tag_id)
                        tag_value = exif_data.get(tag_id)
                        print(f"{tag_name}: {tag_value}")
                else:
                    print(f"No se encontraron datos de metadatos para el archivo: {file}")
        except (IOError, AttributeError):
            print(f"No se puede procesar el archivo: {file}")
            continue
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: scorpion FILE1 [FILE2 ...]")
        sys.exit(1)
    files = sys.argv[1:]
    scorpion(*files)
