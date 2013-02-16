# coding=UTF-8
# Generate training sets for text recognition

import Image, ImageDraw, ImageFont

fontsize = 64
fonts = {
    "song": ImageFont.truetype(u"/Library/Fonts/华文宋体.ttf",fontsize),
}

text = u"您好，世界！"

im = Image.new("L",(400, 100))

draw = ImageDraw.Draw(im)

draw.text((20, 20), text, font=fonts["song"], fill=255)

im_resized = im.resize((200,50), Image.ANTIALIAS)
