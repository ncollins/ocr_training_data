# coding=UTF-8
# Generate training sets for text recognition

import Image, ImageOps

# Single image transformations

def edentity(im):
    """
    Identity function for Image objects.
    """
    return im


def invert(im):
    """
    Just a wrapper around the ImageOps function,
    takes an image and returns it with colors inverted.
    """
    return ImageOps.invert(im)


def return_first(im0, im1):
    """
    Returns first argument.
    """
    return im0


def invert_first(im0, im1):
    """
    Applies ImageOps.invert() to the first argument
    and returns it.
    """
    return ImagesOps.invert(im0)


# Composite two-image transformations

def _glue_vertical(im0, im1):
    """
    Stacks two images vertically, does not preserve
    size.
    """
    im_out = Image.new(im0.mode, (im0.size[0], 2*im0.size[1]))
    im_out.paste(im0,(0,0))
    im_out.paste(im1,(0,im0.size[1]))
    return im_out


def _glue_horizontal(im0, im1):
    """
    Combines two images horizontally, the output
    has dimensions (2*width, height) where width and
    height are taken from the first argument.
    """
    im_out = Image.new(im0.mode,(2*im0.size[0], im0.size[1]))
    im_out.paste(im0,(0,0))
    im_out.paste(im1,(im0.size[0],0))
    return im_out


def splice_vertical(im0, im1):
    im_tmp = _glue_vertical(im0, im1)
    w, h = im_tmp.size
    top, bottom = h // 4, h * 3 // 4
    return im_tmp.crop((0,top,w,bottom))


def splice_horizontal(im0, im1):
    im_tmp = _glue_horizontal(im0, im1)
    w, h = im_tmp.size
    left, right = w // 4, w * 3 // 4
    return im_tmp.crop((left,0,right,h))
