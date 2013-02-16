# coding=UTF-8
# Generate training sets for text recognition

from __future__ import division
import Image, ImageDraw, ImageFont
import itertools

from transformations import edentity, invert 
from transformations import return_first, invert_first
from transformations import splice_horizontal, splice_vertical

fontsize = 64
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
    im = Image.new("L",(size[0]*2,size[1]*2))
    draw = ImageDraw.Draw(im)
    draw.text((20, 20), text, font=font, fill=255)
    im_resized = im.resize(size, Image.ANTIALIAS)
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


def ipair(iter0):
    i = None
    for j in iter0:
        if i == None:
            first = j
        else:
            yield (i,j)
        i = j
    yield (j, first)


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
    trans0 = [(lambda x, y: x, True)] + [(t, False) for t in non_preserving]
    trans1 = [lambda x: x] + [t for t in preserving]
    first = ((t(im0, im1), b) for im0, im1 in ipair(images) for t, b in trans0)
    second = ((t(im), b) for im, b in first for t in trans1)
    return second


if __name__ == '__main__':
    f = open('data/brown.txt', 'r')

    texts = (line for line in f)
    #texts = ['hello', 'goodbye', 'hacker school']
    print('texts = %s' % (str(texts)))

    fonts = [fonts['arial'], fonts['georgia'], fonts['verdana']]
    transforms = [splice_vertical, splice_horizontal]

    images = text_images(texts, fonts, (200,50))
    print('images = %s' % (str(images)))

    catagorized = catagorized_image_transforms(images,
                                              [invert],
                                              [splice_vertical])
    print('catagorized = %s' % (str(catagorized)))
    
    count = 0
    for im,b in catagorized:
        print(count)
        count += 1
    f.close()
    #cat = list(catagorized)
