# coding=UTF-8
# Generate training sets for text recognition

from __future__ import division
import Image, ImageDraw, ImageFont
import itertools

from transformations import edentity, invert 
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
    def inner():
        return (make_text_image(txt,f,size) for txt in texts 
                                        for f in fonts)
    return inner


def images_tranform_product(images, transformations):
    """
    Parameters:
        images - an iterable of images
        transformations - transformations that operate on two images
    Output:
        a generator of images formed by applying the tranformations to
        pairs of images
    """
    l = list(images)
    product = itertools.product(l,l)
    return (t(im1,im2) for t in transformations for im1, im2 in product)


if __name__ == '__main__':
    texts = ["hello, world!", "goodbye, world!", "the quick brown fox..."]
    fonts = [fonts["arial"], fonts["georgia"], fonts["verdana"]]
    transforms = [splice_vertical, splice_horizontal]
    images = make_text_images(texts, fonts, (3000,300))
    products = images_tranform_product(images(), transforms)
