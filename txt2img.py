from PIL import Image, ImageFont, ImageDraw

image = Image.new('RGB', (25,25))
draw = ImageDraw.Draw(image)
typeface = ImageFont.truetype("typefaces/Grand9K Pixel.ttf")

draw.text((10, 25), "world", font=typeface)

image.save("s", 'jpg')

print("end")