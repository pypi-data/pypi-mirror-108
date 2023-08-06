from PIL import Image, ImageDraw, ImageFont
import numpy as np


def txt2crop(str, font, color):

    ascent, descent = font.getmetrics()

    ox = font.getmask(str).getbbox()[2]
    oy = font.getmask(str).getbbox()[3] + descent
    im = Image.new('RGBA', (ox, oy), (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)
    draw.text((0, 0),
              str, color, font=font)
    verticalpix = np.array(im)

    count = 0
    #  momal numpy vertical
    verticalpix = verticalpix.tolist()

    horizonpix = list(map(list, zip(*verticalpix)))

    for y, li1 in enumerate(verticalpix):

        if count == 1:
            break
        for x, li2 in enumerate(li1):
            if count == 1:
                break

            if not li2 == [255, 255, 255, 0]:
                y1 = y
                count = 1

    count = 0
    #  make a horizon line

    for x, li1 in enumerate(horizonpix):

        if count == 1:
            break
        for y, li2 in enumerate(li1):
            if count == 1:
                break
            if not li2 == [255, 255, 255, 0]:
                x1 = x
                count = 1

    count = 0
    reverseverticalpix = reversed(verticalpix)

    for y, li1 in enumerate(reverseverticalpix):
        li1 = reversed(li1)
        if count == 1:
            break
        for x, li2 in enumerate(li1):
            if count == 1:
                break

            if not li2 == [255, 255, 255, 0]:
                y2 = oy-y
                count = 1
    count = 0

    reversehorizonpix = reversed(horizonpix)

    for x, li1 in enumerate(reversehorizonpix):
        li1 = reversed(li1)
        if count == 1:
            break
        for y, li2 in enumerate(li1):
            if count == 1:
                break
            if not li2 == [255, 255, 255, 0]:
                x2 = ox-x
                count = 1
    im = im.crop((x1, y1, x2, y2))
    return im
