from PIL import Image, ImageFont, ImageDraw
import pipeline

def converter(string):

    def getBound(txt, typ):
        testImg = Image.new('RGB', (1, 1))
        testDraw = ImageDraw.Draw(testImg)
        return testDraw.textsize(txt, typ)


    fontface = "typefaces/Grand9K Pixel.ttf"
    fontsize = 500
    bgColor = "white"
    color="black"

    typeface = ImageFont.truetype(fontface, fontsize)


    width, height = getBound(string, typeface)
    image = Image.new('RGB', ( int(width + (width/2)), int(height + (height/2))), bgColor)
    draw = ImageDraw.Draw(image)
    draw.text(((width/4), (height/4)), string, font=typeface, fill=color, size=fontsize)

    image.show()
    pipeline.imgPipe(image)
    # image.save("./test/output.jpg")

    # return string
