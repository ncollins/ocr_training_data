# coding=UTF-8
# Generate training sets for text recognition

from __future__ import division
import Image, ImageDraw, ImageFont

text0 = u"Hello, world!"
text1 = u"您好，世界！"


fontsize = 256
fonts = {
    "song": ImageFont.truetype(u"/Library/Fonts/华文宋体.ttf",fontsize),
    "black": ImageFont.truetype(u"/Library/Fonts/华文细黑.ttf",fontsize),
    "arial": ImageFont.truetype(u"/Library/Fonts/Arial.ttf",fontsize),
    "georgia": ImageFont.truetype(u"/Library/Fonts/Georgia.ttf",fontsize),
    "verdana": ImageFont.truetype(u"/Library/Fonts/Verdana.ttf",fontsize),
}

def make_text_image(text, f):
    im = Image.new("L",(3000,300))
    draw = ImageDraw.Draw(im)
    draw.text((20, 20), text1, font=f, fill=255)
    im_resized = im.resize((1000,100), Image.ANTIALIAS)
    return im_resized


def glue_images_vertical(im0, im1):
    im_out = Image.new(im0.mode, (im0.size[0], 2*im0.size[1]))
    im_out.paste(im0,(0,0))
    im_out.paste(im1,(0,im0.size[1]))
    return im_out


def splice_images_vertical(im0, im1):
    im_tmp = glue_images_vertical(im0, im1)
    w, h = im_tmp.size
    top, bottom = h // 4, h * 3 // 4
    return im_tmp.crop((0,top,w,bottom))


def glue_images_horizontal(im0, im1):
    im_out = Image.new(im0.mode,(2*im0.size[0], im0.size[1]))
    im_out.paste(im0,(0,0))
    im_out.paste(im1,(im0.size[0],0))
    return im_out


def splice_images_horizontal(im0, im1):
    im_tmp = glue_images_horizontal(im0, im1)
    w, h = im_tmp.size
    left, right = w // 4, w * 3 // 4
    return im_tmp.crop((left,0,right,h))
