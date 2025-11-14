# import Libraries
import requests  # To help to download the image form internet(Github)
from io import BytesIO   # treat Downloaded bytes as a file
from PIL import Image, ImageDraw, ImageFont # To load Image, To Draw text on image and last one set font size and font
import qrcode

IMAGE_URL = "https://raw.githubusercontent.com/AshwiniSuryakar09/Invite_Maker-Python/main/couple.jpg.jpeg"
VIDEO_URL = "https://www.youtube.com/shorts/zBxFseL62gE"   # replace with your video link

OUTPUT_FILE = "final_wedding_card.png"   # Final Output

def load_image_from_url(url):
    response = requests.get(url)   # Download the image from internet
    return Image.open(BytesIO(response.content)).convert("RGB")  # Stored in memory and loaded as jpg

base_image = load_image_from_url(IMAGE_URL)

qr = qrcode.QRCode(box_size=10, border=2)   # Create QR code and fix its size
qr.add_data(VIDEO_URL)
qr.make(fit=True)   # Fit properly

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")  
qr_img = qr_img.resize((230, 230))

draw = ImageDraw.Draw(base_image)   # TO draw Initials on the image

# Initials font name and font size
try:
    font = ImageFont.truetype("arial.ttf", 120) # Used font name = arial and size =120
except:
    font = ImageFont.load_default()  # if not available above fot and then use default one

initials_text = "A  &  R"

# Pillow and Initials position
bbox = draw.textbbox((0, 0), initials_text, font=font)    # Size =[left(0),Top(1),Right(2),Bottom(3)] 
text_width = bbox[2] - bbox[0]             # (size = 0,0,350,120)
text_height = bbox[3] - bbox[1]

image_width, image_height = base_image.size

# Centered and placed the Initials
text_x = (image_width - text_width) // 2    # To put your initals horizontally
text_y = 50  # place text 50 pixels from top edge

draw.text((text_x, text_y), initials_text, fill="white", font=font)

# QR 
qr_x = image_width - qr_img.width - 40
qr_y = image_height - qr_img.height - 40

base_image.paste(qr_img, (qr_x, qr_y))

# save Image
base_image.save(OUTPUT_FILE)

print("Wedding card created successfully:", OUTPUT_FILE)

