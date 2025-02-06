from PIL import Image, ImageDraw, ImageFont

# Tạo ảnh vuông 256x256 pixels
img = Image.new('RGB', (256, 256), color='white')
d = ImageDraw.Draw(img)

try:
    # Cố gắng load font mặc định
    font = ImageFont.truetype("arial.ttf", 100)
except:
    # Nếu không có font arial, dùng font mặc định
    font = ImageFont.load_default()

# Vẽ chữ "T" ở giữa
text = "T"
# Tính toán vị trí để text nằm giữa
text_bbox = d.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
x = (256 - text_width) // 2
y = (256 - text_height) // 2

# Vẽ text
d.text((x, y), text, fill='black', font=font)

# Lưu dưới dạng .ico
img.save('icon.ico') 