import pygame as pg
from text import *


class Texts(Text):
    def __init__(self, screen, texts_end_func=None, font_kind="arial", font_size=30, line_pad=10, font_color="white", box_pad=10, box_color="black", box=None, text_time=100, text_align="left"):
        super().__init__(screen, text_align=text_align, font_kind=font_kind, font_size=font_size, line_pad=line_pad, font_color=font_color, box_pad=box_pad, box_color=box_color, box=box, text_time=text_time)
        self.texts = []
        self.texts_pro = 0
        self.texts_end_func = texts_end_func

    def update(self):
        super().update()

    def update_texts(self):
        if not self.texts_end:
            self.texts_pro += 1
            self.change_text(self.texts[self.texts_pro])
        else:
            if self.texts:
                self.end()
                if self.texts_end_func is not None:
                    self.texts_end_func()
                    self.texts_end_func = None

    def end(self):
        self.texts = []
        self.text = ""
        self.texts_pro = 0
        self.text_words = []

    @property
    def texts_end(self):
        return self.texts_pro >= len(self.texts) - 1

    def change_texts(self, texts=None, texts_end_func=None):
        if texts is None:
            texts = []
        self.texts = texts
        self.texts_pro = 0
        if self.texts:
            self.change_text(self.texts[self.texts_pro])
        self.texts_end_func = texts_end_func
