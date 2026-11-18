"""
A subclass of PIL.ImageDraw that can draw anti-alias polygons to an existing PIL.Image as a drop-in replacement using aggdraw
by @t-wy (2025)
"""

from PIL import Image, ImageDraw as _ImageDraw, ImageColor, ImageFont
from typing import *

if TYPE_CHECKING:
    from PIL._typing import _Ink

def _to_rgba(color: Any) -> Tuple[int, int, int, int]:
    """Normalize a Pillow ink value to an RGBA tuple."""
    if isinstance(color, str):
        color = ImageColor.getrgb(color)
    if isinstance(color, int):
        return color, color, color, 255
    color = tuple(color)
    if len(color) == 1:
        return color[0], color[0], color[0], 255
    if len(color) == 2:
        return color[0], color[0], color[0], color[1]
    if len(color) == 3:
        return *color, 255
    if len(color) == 4:
        return color
    raise ValueError(f"Invalid color: {color}")

class ImageDraw(_ImageDraw.ImageDraw):
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
        has_alpha = "A" in base_image.mode
        image_mode = self._image.mode
        patch = aggdraw.Draw("RGBA", patch_size)
        if base_image.mode == "RGBA":
            # avoid copy
            patch.frombytes(base.tobytes())
        else:
            patch.frombytes(base.convert("RGBA").tobytes())
        patch_alpha = None
        if has_alpha:
            base_alpha = base.getchannel("A")
            patch_alpha = aggdraw.Draw("L", patch_size)
            patch_alpha.frombytes(base_alpha.tobytes())
        brush, brush_alpha = None, None
        if fill is not None:
            color = _to_rgba(fill)
            brush = aggdraw.Brush(color)
            brush_alpha = aggdraw.Brush(color[3])
        pen, pen_alpha = None, None
        if outline is not None:
            color = _to_rgba(outline)
            pen = aggdraw.Pen(color, width)
            pen_alpha = aggdraw.Pen(color[3], width)
        patch.polygon(xy, pen, brush)
        img = Image.frombytes(
            "RGBA",
            patch_size,
            patch.tobytes()
        )
        if patch_alpha is not None:
            patch_alpha.polygon(xy, pen_alpha, brush_alpha)
            a2 = Image.frombytes("L", patch_size, patch_alpha.tobytes())
            *color, a = img.split()
            merged_image = Image.merge(image_mode, (*color, a2))
            base_image.paste(merged_image, (min_x, min_y))
        elif base_image.mode == "RGBA":
            base_image.paste(img, (min_x, min_y))
        else:
            base_image.paste(
                img.convert(base_image.mode),
                (min_x, min_y)
            )

    def text(
        self,
        xy: tuple[float, float],
        text: str,
        fill: Optional["_Ink"] = None,
        font: Optional[ImageFont.ImageFont] = None,
        anchor: Optional[str] = None,
        spacing: float = 4,
        align: str = "left",
        direction: Optional[str] = None,
        features: Optional[list[str]] = None,
        language: Optional[str] = None,
        stroke_width: float = 0,
        stroke_fill: Optional["_Ink"] = None,
        embedded_color: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        zoom = 4
        font2 = font.font_variant(size = font.size * zoom)
        spacing2 = spacing * zoom
        stroke_width2 = stroke_width * zoom
        left, top, right, bottom = self.textbbox(
            (0, 0),
            text,
            font=font2,
            anchor=anchor,
            spacing=spacing2,
            align=align,
            direction=direction,
            features=features,
            language=language,
            stroke_width=stroke_width2,
            *args,
            **kwargs,
        )
        # make sure all coordinates are multiples
        left = int(left / zoom) * zoom
        top = int(top / zoom) * zoom
        right = (int(right / zoom) + 2) * zoom # 1 for inclusive, 1 for fraction coord part
        bottom = (int(bottom / zoom) + 2) * zoom
        mode = self._image.mode
        if "A" not in mode:
            mode = "RGBA"
        
        # patch size
        image_width = int((right - left) / zoom) + 1
        image_height = int((bottom - top) / zoom) + 1
        
        # now address for the decimal part of the result coordinates
        x_offset = (xy[0] % 1) * zoom
        y_offset = (xy[1] % 1) * zoom
        x_trunc = int(xy[0])
        y_trunc = int(xy[1])
        tmp = Image.new(
            mode,
            (image_width * zoom, image_height * zoom),
            (0, 0, 0, 0)
        )
        draw = _ImageDraw.Draw(tmp)
        draw.text(
            (
                x_offset - left,
                y_offset - top
            ),
            # notice that xy2 + offset is the actual text position zoomed, left and top (multiple of zoom) gives the offset such that the text is rendered within the image
            text,
            fill=fill,
            font=font2,
            anchor=anchor,
            spacing=spacing2,
            align=align,
            direction=direction,
            features=features,
            language=language,
            stroke_width=stroke_width2,
            stroke_fill=stroke_fill,
            embedded_color=embedded_color,
            *args,
            **kwargs,
        )
        tmp = tmp.resize(
            (image_width, image_height),
            Image.Resampling.LANCZOS,
        )
        dest_x = x_trunc + left // zoom # compensate for the offset
        dest_y = y_trunc + top // zoom
        self._image.paste(tmp, (dest_x, dest_y), mask = tmp)


def Draw(im: Image.Image) -> ImageDraw:
    return ImageDraw(im)