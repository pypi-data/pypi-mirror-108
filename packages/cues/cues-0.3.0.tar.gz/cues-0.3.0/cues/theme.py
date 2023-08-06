# -*- coding: utf-8 -*-

"""
cues.theme
==========

This module contains the Theme class.
"""


class Theme:
    themes = {
        'Vice': {
            'question': 'pink',
            'secondary': 'blue',
            'primary': 'purple'
        }
    }

    def __init__(self, theme=None):
        self.theme = theme or 'Vice'
