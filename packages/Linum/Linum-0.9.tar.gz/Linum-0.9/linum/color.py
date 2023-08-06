import colorsys
import random
import re
from copy import copy
from typing import Union, Tuple, Set, Dict

import wcag_contrast_ratio as contrast

from linum.styles import color_palettes


class Color:
    used_colors: Dict[str, Set[int]] = {}

    def __init__(self, rgb: Union[str, int, 'Color'] = 0x000000):
        if isinstance(rgb, int):
            self.r = (rgb & 0xFF0000) >> 16
            self.g = (rgb & 0x00FF00) >> 8
            self.b = rgb & 0x0000FF
        elif isinstance(rgb, str) and re.fullmatch("#[0-9a-fA-F]{6}", rgb):
            self.r = int(rgb[1:3], 16)
            self.g = int(rgb[3:5], 16)
            self.b = int(rgb[5:7], 16)
        elif isinstance(rgb, Color):
            self.r, self.g, self.b = rgb.r_g_b
        else:
            raise ValueError

    def __str__(self):
        return '#' + hex(self.rgb)[2:].zfill(6)

    def __copy__(self):
        return Color(self.rgb)

    def contrast(self, color: 'Color') -> float:
        return contrast.rgb(self.r_g_b_percents, color.r_g_b_percents)

    @property
    def rgb(self) -> int:
        r, g, b = self.r_g_b
        r = r << 16
        g = g << 8
        return r + g + b

    @property
    def r_g_b(self) -> Tuple[int, int, int]:
        return self.r, self.g, self.b

    @property
    def r_g_b_percents(self) -> Tuple[float, float, float]:
        r, g, b = self.r_g_b
        return r / 255, g / 255, b / 255

    @property
    def h_s_v_percents(self) -> Tuple[float, float, float]:
        """
        Converts color to hue, saturation and value parts in percents.

        :return: Tuple[float, float, float]
        """
        r, g, b = self.r_g_b_percents
        return colorsys.rgb_to_hsv(r, g, b)

    @staticmethod
    def from_h_s_v_percents(h: float, s: float, v: float) -> 'Color':
        """
        Converts hue, saturation and value parts in percents to rgb int value.

        :param h: hue part in percents
        :param s: saturation part in percents
        :param v: value part in percents
        :return: int
        """
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r, g, b, = int(r * 255), int(g * 255), int(b * 255)

        r = r << 16
        g = g << 8
        return Color(r + g + b)

    @staticmethod
    def get_random_rgb(palette: str = "material_design") -> int:
        colors = color_palettes.palettes[palette]
        palette_colors = set(colors.values())
        used_colors = Color.used_colors.setdefault(palette, set())
        difference = palette_colors.difference(used_colors)
        if not difference:
            Color.used_colors[palette] = set()
            difference = palette_colors
        color = random.choice(list(difference))
        Color.used_colors[palette].add(color)
        return color

    def apply_blackout(self, blackout_value: float):
        h, s, v = self.h_s_v_percents
        v = max(0.0, v - blackout_value)
        self.r, self.g, self.b = self.from_h_s_v_percents(h, s, v).r_g_b
        return Color(self.rgb)

    def get_contrast_font_color(self):
        white_color = Color(0xFFFFFF)

        dark_color = copy(self)
        dark_color.apply_blackout(0.87)

        # Calculating contrasts
        dark_color_contrast = self.contrast(dark_color)
        white_contrast = self.contrast(white_color)

        # Choosing color with greater contrast
        contrast_color = dark_color if dark_color_contrast > white_contrast else white_color
        return contrast_color
