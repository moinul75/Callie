from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def resize_and_crop_image(image, size=(700, 470)):
    with Image.open(image) as img:
        img = img.convert("RGBA")  # Ensure image is in RGBA mode for PNG
        
        # Resize image with high-quality resampling
        img.thumbnail(size, Image.Resampling.LANCZOS)
        width, height = img.size
        target_width, target_height = size
        
        # Calculate the cropping box
        left = (width - target_width) / 2
        top = (height - target_height) / 2
        right = (width + target_width) / 2
        bottom = (height + target_height) / 2
        
        img = img.crop((left, top, right, bottom))
        
        # Save image to a BytesIO object
        img_io = BytesIO()
        img.save(img_io, format='PNG', quality=100)  # Save as PNG
        img_file = ContentFile(img_io.getvalue(), image.name.replace('.jpg', '.png'))
        
        return img_file

