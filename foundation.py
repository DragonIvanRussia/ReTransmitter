import inspect
import math
import ctypes
import os
import sys
import pygame



def ColorDelta(color, delta, variation: str, *args):
    """linear: add value
sine: varies between original color and current color"""
    result = []
    if variation == 'linear':
        for i in range(0, 3):
            buffer = color[i] + delta[i]
            if buffer > 255:
                buffer = 255
            if buffer < 0:
                buffer = 0
            result.append(buffer)
    if variation == 'sine':
        duration = args[0]
        ceil = args[1]
        orig = args[2]
        if duration is None or ceil is None:
            raise ValueError("duration not filled in. check duration or ceil")
        elif type(duration) != int or type(ceil) != int:
            raise TypeError("value not int. check duration or ceil")
        for i in range(0, 3):
            buffer = 0
            if orig[i] and delta[i] != 0:
                preset = delta[i] - orig[i]
                buffer = preset / 2 * math.sin((duration * math.pi) / (ceil * 2)) + preset / 2 + orig[i]
            if buffer > 255:
                buffer = 255
            if buffer < orig[i]:
                buffer = orig[i]
            result.append(int(buffer))
    return tuple(result)

def MoveDelta(origin, offset, variation: str, *args):
    result = list(origin)
    if variation == 'linear':
        for i in range(0, 2):
            result[i] += offset[i]
    elif variation == 'accelerate':
        for i in range(0, 2):
            result[i] += offset[i] * args[0]
    else:
        duration = args[0]
        ceil = args[1]
        if variation == 'sine':
            for i in range(0, 2):
                preset = offset[i] - origin[i]
                result[i] = -1 *(math.cos(math.pi * duration / ceil) - 1) / 2 * preset + origin[i]
        elif variation == 'quad':
            for i in range(0, 2):
                preset = offset[i] - origin[i]
                x = duration / ceil
                if x > 1:
                    x -= 1
                if x < 0.5:
                    result[i] = 2 * x * x * preset + origin[i]
                else:
                    result[i] = (1 - math.pow((-2 * x + 2), 2) / 2) * preset + origin[i]
        if variation == 'out_quad':
            for i in range(0, 2):
                preset = offset[i] - origin[i]
                x = duration / ceil
                result[i] = (1 - (1 - x) * (1 - x)) * preset + origin[i]
        elif variation == 'expo':
            for i in range(0, 2):
                result = 1
        elif variation == 'custom':  
            handle_bottom = args[2][0]
            handle_top = args[2][1]
    return tuple(result)

class BGColor():
    def __init__(self, orig, delta, variation='linear', *args):
        global bg_color
        self.delta = delta
        self.variation = variation
        self.args = args
        self.original = orig
        if self.variation == 'sine' and len(self.args) == 1:
            self.args = (0, self.args[0])

    def __call__(self):
        bg_color = ColorDelta(self.original, self.delta, self.variation, *self.args, self.original)
        if self.variation == 'sine':
            self.args = (self.args[0] + 1, self.args[1])
        return bg_color

def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image
