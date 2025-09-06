"""
A subclass of PIL.ImageDraw that can draw anti-alias polygons to an existing PIL.Image as a drop-in replacement using aggdraw
by @t-wy (2025)
"""

from PIL import Image, ImageDraw, ImageColor
from typing import *

class ImageDraw(ImageDraw.ImageDraw):
    def __init__(self, im: Image.Image) -> None:
        super().__init__(im)

    def polygon(self, xy: Union[List[float], List[Tuple[float, float]]], fill = None, outline = None, width: int = 1):
        import aggdraw
        from math import ceil
        if len(xy) == 0:
            return
        if isinstance(xy[0], tuple):
            # flatten to (x, y, x, y, ...)
            xy = tuple(c for pt in xy for c in pt)
        xs = xy[0::2]
        ys = xy[1::2]
        min_x = int(min(xs)) - 1
        min_y = int(min(ys)) - 1
        max_x = ceil(max(xs)) + 1
        max_y = ceil(max(ys)) + 1
        xy = tuple(c for x, y in zip(xs, ys) for c in (x - min_x, y - min_y))
        base_image: Image.Image = self._image
        base = base_image.crop((min_x, min_y, max_x, max_y)) # left, upper, right, and lower
        patch_size = (max_x - min_x, max_y - min_y)
        base_alpha = base.getchannel("A")
        patch = aggdraw.Draw("RGBA", patch_size)
        patch.frombytes(base.tobytes())
        patch_alpha = aggdraw.Draw("L", patch_size)
        patch_alpha.frombytes(base_alpha.tobytes())
        brush, brush_alpha = None, None
        if fill is not None:
            color = ImageColor.getrgb(fill) if isinstance(fill, str) else fill
            alpha = color[3] if len(color) == 4 else 255
            brush = aggdraw.Brush(color)
            brush_alpha = aggdraw.Brush(alpha)
        pen, pen_alpha = None, None
        if outline is not None:
            color = ImageColor.getrgb(outline) if isinstance(outline, str) else outline
            alpha = color[3] if len(color) == 4 else 255
            pen = aggdraw.Pen(color, width)
            pen_alpha = aggdraw.Pen(alpha, width)
        patch.polygon(xy, pen, brush)
        patch_alpha.polygon(xy, pen_alpha, brush_alpha)
        img = Image.frombytes("RGBA", (max_x - min_x, max_y - min_y), patch.tobytes())
        a2 = Image.frombytes("L", (max_x - min_x, max_y - min_y), patch_alpha.tobytes())
        r, g, b, a = img.split()
        merged_image = Image.merge("RGBA", (r, g, b, a2))
        base_image.paste(merged_image, (min_x, min_y))


def Draw(im: Image.Image) -> ImageDraw:
    return ImageDraw(im)