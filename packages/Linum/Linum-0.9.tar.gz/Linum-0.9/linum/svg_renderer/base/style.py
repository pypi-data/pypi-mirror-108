from typing import List

from linum.color import Color


class Style(dict):
    attrib_to_fix_color = [
        "fill",
        "stroke"
    ]

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
        l = []
        for parent in self.parents:
            l.append(str(parent))
        s = " [ " + " : ".join(l) + ' ] '
        return "{} -> {}".format(s, self.debug_name)

    @classmethod
    def fix_colors(cls, style_dict: dict):
        """
        It fixes colors to use them with xlsxwriter lib.

        """
        for k, v in style_dict.items():
            if k in cls.attrib_to_fix_color:
                color = Color(v)
                style_dict.update({k: str(color)})
        return style_dict

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
        sub_style = Style(key)
        sub_style.parents = [self]
        return sub_style

    @property
    def all(self) -> dict:
        """
        Returns all style params including inherited.

        :return: dict
        """
        d = {}
        for parent in self.parents:
            d.update(parent.all)

        for k, v in self.items():
            if not isinstance(v, dict):
                d.update({k: v})

        for k, v in d.copy().items():
            if v is None:
                d.pop(k)

        return d

    def _get_element_style(self, attrib_list: List[str]):
        return {k: v for k, v in self.all.items() if k in attrib_list}
