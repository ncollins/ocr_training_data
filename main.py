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

def text_image_single(text, font, size):
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


def text_images(texts, fonts, size):
    """
    Parameters:
        texts - an iterable of text values
        fonts - an iterable of ImageFont objects
        size - a (width, height) tuple
    Output:
        A (lazy) generator of Image objects, each with one piece of text.
    """
    return (text_image_single(txt,f,size) for txt in texts 
                                        for f in fonts)


def images_transform_simple(images, transformations):
    """
    Parameters:
        images - an iterable of images
        transformations - transformations that operate on one image
    Output:
        a generator of the images with transformations applied
    """
    return (t(i) for i in images for t in transformations)


def images_transform_product(images, transformations):
    """
    Parameters:
        images - an iterable of images
        transformations - transformations that operate on two images
    Output:
        a generator of images formed by applying the tranformations to
        pairs of images
    """
    product = itertools.product(images, repeat=2)
    return (t(im1,im2) for t in transformations for im1, im2 in product)


def imerge(iter0, iter1):
    for i,j in itertools.izip(iter0, iter1):
        yield i
        yield j


def catagorized_image_transforms(images, preserving, non_preserving):
    """
    Parameters:
        images - an interable of images
        preserving - transformations that preserve the "text" nature of an image
        non_preserving - tranformation that break the "text" nature
    Output:
        a generator of (Image, bool) tuples where the bool indicates whether
        the images is a "text" image or not
    """
    images0, images1 = itertools.tee(images, 2)
    text = itertools.izip(images_transform_simple(images0, preserving),
                          itertools.repeat(True))
    #test = images_transform_product(images, non_preserving)
    non_text = itertools.izip(images_transform_product(images1, non_preserving),
                              itertools.repeat(False))
    return imerge(text, non_text)

if __name__ == '__main__':
    texts = ['hello, world!', 'the quick brown fox...', 'goodbye, world!', 'HaSch']
    fonts = [fonts['arial'], fonts['georgia'], fonts['verdana']]
    transforms = [splice_vertical, splice_horizontal]
    images = text_images(texts, fonts, (3000,300))
    catagorized = catagorized_image_transforms(images,
                                              [edentity, invert],
                                              [splice_horizontal, splice_vertical])
