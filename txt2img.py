from PIL import Image, ImageFont, ImageDraw
import pipeline

def converter(string):
    string = string.replace(" ", "")
    lent = len(string)
    chars = list(string)


    def getBound(txt, typ):
        testImg = Image.new('RGB', (1, 1))
        testDraw = ImageDraw.Draw(testImg)
        # print(testDraw.textsize(txt, typ))
        return testDraw.textsize(txt, typ)


    fontface = "typefaces/bpdots.squaresedit-Bold.otf"
    fontsize = 500
    bgColor = "white"
    color="black"

    typeface = ImageFont.truetype(fontface, fontsize)


    width, height = getBound(string, typeface)
    image = Image.new('RGB', (width, height+30), bgColor)
    draw = ImageDraw.Draw(image)
    draw.text((0, 15), string, font=typeface, fill=color, size=fontsize)
    image.show()
    return pipeline.imgPipe([image, lent], chars)
    # image.save("./test/output.jpg")

    # return string
