import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import qrcode

# ---------------------------------------
# 🔧 ADD YOUR LINKS HERE
# ---------------------------------------

IMAGE_URL = "https://raw.githubusercontent.com/AshwiniSuryakar09/Invite_Maker-Python/main/couple.jpg.jpeg"
VIDEO_URL = "https://www.youtube.com/shorts/zBxFseL62gE"   # replace with your video link

OUTPUT_FILE = "final_wedding_card.png"

# ---------------------------------------
# 🔧 DOWNLOAD IMAGE FROM URL
# ---------------------------------------
def load_image_from_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGB")

base_image = load_image_from_url(IMAGE_URL)

# ---------------------------------------
# 🔧 GENERATE QR CODE
# ---------------------------------------
qr = qrcode.QRCode(box_size=10, border=2)
qr.add_data(VIDEO_URL)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
qr_img = qr_img.resize((230, 230))

# ---------------------------------------
# 🔧 ADD INITIALS WITH MODERN LOOK
# ---------------------------------------
draw = ImageDraw.Draw(base_image)

try:
    font = ImageFont.truetype("arial.ttf", 120)
except:
    font = ImageFont.load_default()

initials_text = "A  &  R"

# Pillow 10+ uses textbbox
bbox = draw.textbbox((0, 0), initials_text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

image_width, image_height = base_image.size

# Centered
text_x = (image_width - text_width) // 2
text_y = 50  # Adjust top space

draw.text((text_x, text_y), initials_text, fill="white", font=font)

# ---------------------------------------
# 🔧 ADD QR CODE BOTTOM-RIGHT
# ---------------------------------------
qr_x = image_width - qr_img.width - 40
qr_y = image_height - qr_img.height - 40

base_image.paste(qr_img, (qr_x, qr_y))

# ---------------------------------------
# 🔧 SAVE IMAGE
# ---------------------------------------
base_image.save(OUTPUT_FILE)

print("Wedding card created successfully:", OUTPUT_FILE)
