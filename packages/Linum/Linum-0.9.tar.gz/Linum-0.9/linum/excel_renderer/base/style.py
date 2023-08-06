from copy import copy
from typing import List

from xlsxwriter import Workbook
from xlsxwriter.format import Format

from linum.color import Color

WHITE_COLOR = 0xFFFFFF
BLACK_COLOR = 0x000000


class Style(dict):

    def __init__(self, debug_name="", **kwargs):
        """
        Container for styles settings.

        :param kwargs: styles settings
        """
        self.debug_name = debug_name
        self.parents: List[Style] = []
        super().__init__(**kwargs)

    def __bool__(self):
        result = bool(super())
        return result or bool(self.parents)

    def __repr__(self):
        return "<Style '{}'>".format(self.debug_name)

    def get(self, key, default=None):
        """
        Overridden method. Search key among self and parents styles.

        :param key: key to search
        :param default: default value to return
        :return:
        """
        value = super().get(key, None)
        if value is not None:
            return value
        else:
            if not self.parents:
                return default
            else:
                value = None
                for parent in self.parents:
                    v = parent.get(key)
                    value = v if v is not None else value
                return value if value is not None else default

    def get_sub_style(self, key) -> 'Style':
        """
        Return sub style if exist, else create new sub style.

        :param key: key for sub style
        :return: Style
        """
        if key in self and isinstance(self[key], Style):
            sub_style = self[key]
            sub_style.debug_name = key
            return sub_style
        sub_style = Style()
        sub_style.parents = [self]
        sub_style.debug_name = key
        return sub_style

    @property
    def all(self) -> dict:
        """
        Returns all style params including inherited.

        :return: dict
        """
        d = {}
        for k, v in self.items():
            if not isinstance(v, dict):
                d.update({k: v})

        d_ = {}
        for parent in self.parents:
            d_.update(parent.all)

        d_.update(d)
        return d_

    def get_xlsxwriter_format(self, workbook: Workbook) -> Format:
        """
        Gets xlsxwriter format object.

        :param workbook:
        :return:
        """
        style_params = self.all

        # Applying blackout
        if style_params.get("use_blackout", False):
            blackout_value = style_params.get("blackout_value", 0.12)
            style_params = self.apply_blackout(style_params, blackout_value)

        # Resolving font color
        if style_params.get("font_color", False) == "auto":
            style_params = self.get_font_color(style_params)

        # Resolving colors with "blackout" value
        style_params = self.resolve_blackout_colors(style_params)

        # Fixing colors
        style_params = self.fix_colors(style_params)

        format_ = workbook.add_format()
        for k, v in style_params.items():
            try:
                getattr(format_, "set_" + k)(v)
            except AttributeError:
                pass
        return format_

    @staticmethod
    def fix_colors(style_dict: dict):
        """
        It fixes colors to use them with xlsxwriter lib.

        """
        for k, v in style_dict.items():
            if k.find("color") > -1:
                color = Color(v)
                style_dict.update({k: str(color)})
        return style_dict

    @staticmethod
    def apply_blackout(style_dict: dict, blackout_value: float):
        """
        Applies blackout to all colors in style dict

        """
        bg_color = style_dict.setdefault('bg_color', WHITE_COLOR)
        for k, v in style_dict.items():
            if k in ["bg_color", "left_color", "right_color", "top_color", "bottom_color"] \
                    and v != "blackout":
                v = v or bg_color
                color = Color(v)
                style_dict[k] = color.apply_blackout(blackout_value).rgb
        return style_dict

    @staticmethod
    def get_font_color(style_params: dict):
        bg_color = Color(style_params.get("bg_color", WHITE_COLOR))

        # Calculating color as black with opacity 0.87 on background color
        dark_color = copy(bg_color)
        dark_color.apply_blackout(0.87)

        # Calculating contrasts
        dark_color_contrast = bg_color.contrast(dark_color)
        white_contrast = bg_color.contrast(Color(WHITE_COLOR))

        # Choosing color with greater contrast
        contrast_color = dark_color if dark_color_contrast > white_contrast else Color(WHITE_COLOR)
        style_params.update({"font_color": contrast_color.rgb})
        return style_params

    @staticmethod
    def resolve_blackout_colors(style_params: dict) -> dict:
        blackout_value = style_params.get("blackout_value", 0.12)
        for k, v in style_params.items():
            if v == "blackout":
                color = Color(style_params.get("bg_color", WHITE_COLOR))
                color.apply_blackout(blackout_value)
                style_params[k] = color.rgb
        return style_params
