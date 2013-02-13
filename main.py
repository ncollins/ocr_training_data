# coding=UTF-8
# Generate training sets for text recognition

from __future__ import division
import Image, ImageDraw, ImageFont
import itertools

from transformations import splice_horizontal, splice_vertical

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

def make_text_image(text, font, size):
    """
    Parameters:
        text - a string
        font - an ImageFont object
        size - a (width, height) tuple
    Output:
        An Image displaying the text
    """
    im = Image.new("L",(3000,300))
    draw = ImageDraw.Draw(im)
    draw.text((20, 20), text, font=font, fill=255)
    im_resized = im.resize((1000,100), Image.ANTIALIAS)
    return im_resized


def make_text_images(texts, fonts, size):
    """
    Parameters:
        texts - an iterable of text values
        fonts - an iterable of ImageFont objects
        size - a (width, height) tuple
    Output:
        A (lazy) generator of Image objects, each with one piece of text.
    """
    return (make_text_image(txt,f,size) for txt in texts 
                                    for f in fonts)


def combine(images, preserving, non_preserving, depth=2):
    """
    Parameters:
        images - a iterable of Image objects, these are assumed to all
                    be valid "text" images
        preserving - a iterable of transformations (functions) that 
                    preserve the "text" nature of an image
        non_preserving - a iterable of transformations that do not preserve 
                    the "text" nature of the image
        depth - an integer specifying how many successive  
    Output:
        a (lazy) generator of (Image,Bool) tuples where True indicates that
        the images is still classified as "text" and False indicates otherwise
    """
    pres = ((fn,True) for fn in preserving)
    non_pres = ((fn,False) for fn in non_preserving)
    all_trans = itertools.chain(pres, non_pres)
    images_initial = ((im, True) for im in images)
    def recur(images_cat, depth):
        if depth == 0:
            return images_cat
        else:
            new_images = ((t(im), t_bool*im_bool) for im, im_bool in images_cat
                                                for t, t_bool in all_trans)
            return recur(new_images, depth - 1)
    return recur(images_initial, depth)
