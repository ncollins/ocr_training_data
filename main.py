# coding=UTF-8
# Generate training sets for text recognition

import Image, ImageDraw, ImageFont

text0 = u"Hello, world!"
text1 = u"您好，世界！"


im = Image.new("L",(3000,300))
draw = ImageDraw.Draw(im)

fontsize = 256
fonts = {
    "song": ImageFont.truetype(u"/Library/Fonts/华文宋体.ttf",fontsize),
    "black": ImageFont.truetype(u"/Library/Fonts/华文细黑.ttf",fontsize),
    "arial": ImageFont.truetype(u"/Library/Fonts/Arial.ttf",fontsize),
    "georgia": ImageFont.truetype(u"/Library/Fonts/Georgia.ttf",fontsize),
    "verdana": ImageFont.truetype(u"/Library/Fonts/Verdana.ttf",fontsize),
}

draw.text((20, 20), text1, font=fonts["song"], fill=255)
im_resized = im.resize((1000,100), Image.ANTIALIAS)
