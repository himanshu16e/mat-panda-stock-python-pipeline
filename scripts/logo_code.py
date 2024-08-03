from PIL import Image, ImageDraw, ImageFont
import os

width, height = 400, 200
image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)

font_size = 60

try:
    font = ImageFont.truetype("arial.ttf", font_size)
except IOError:
    font = ImageFont.load_default()


text = "Frank's stock"
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
text_position = ((width - text_width) // 2, (height - text_height) // 2)


offset = 5
shadow_color = "gray"


for i in range(offset):
    draw.text((text_position[0] + i, text_position[1] + i), text, font=font, fill=shadow_color)


text_color = "blue"
draw.text(text_position, text, font=font, fill=text_color)


os.makedirs('assets', exist_ok=True)
image.save('assets/company_logo.png')
print("3D logo saved as company_logo.png in the assets folder.")