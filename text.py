import pygame as pg


class Text:
    def __init__(self, screen, text="", text_end_func=None, font_kind="arial", font_size=30, line_pad=10, font_color="white", box_pad=10, box_color="black", box=None, text_time=100, text_align="left"):
        self.screen = screen

        # style properties
        self.font_kind = font_kind
        self.font_size = font_size
        self.line_pad = line_pad
        self.font_color = font_color
        self.box_pad = box_pad
        self.box_color = box_color
        if box is None:
            box = pg.Rect(0, 0, 50, 50)
        self.box = box
        self.text_align = text_align

        self.font = pg.font.SysFont(font_kind, font_size)
        self.text = text
        self.text_time = text_time
        self.text_words = []
        self.prev_time = pg.time.get_ticks()
        self.text_end_func = text_end_func

    def update_text(self):
        if not self.text_end and self.text_trigger:
            if self.text_time:
                self.text_words.append(self.text.split(" ")[len(self.text_words)])
            else:
                self.text_words = self.text.split(" ")
        elif self.text_end:
            if self.text_end_func is not None:
                self.text_end_func()
                self.text_end_func = None

    def update(self):
        self.update_text()

    def draw_text(self):
        if self.text:
            if self.box_color:
                pg.draw.rect(self.screen, self.box_color, self.box)
            text = self.font.render(" ".join(self.text_words), True, self.font_color)
            if text.get_width() <= self.box.w - self.box_pad * 2 and "\n" not in "".join(self.text_words):
                if self.text_align == "right":
                    self.screen.blit(text, (self.box.x + self.box.w - text.get_width() - self.box_pad, self.box.y + self.box_pad))
                elif self.text_align == "center":
                    self.screen.blit(text, (self.box.x + (self.box.w - text.get_width()) / 2, self.box.y + self.box_pad))
                elif self.text_align == "left":
                    self.screen.blit(text, (self.box.x + self.box_pad, self.box.y + self.box_pad))
            else:
                texts = []
                line = ""
                for word in self.text_words:
                    if word == "\n":
                        text = self.font.render(line, True, self.font_color)
                        texts.append(text)
                        line = ""
                        continue
                    if line:
                        line += " " + word
                    else:
                        line += word
                    new_text = self.font.render(line, True, self.font_color)
                    if new_text.get_width() <= self.box.w - self.box_pad * 2:
                        text = new_text
                    else:
                        texts.append(text)
                        line = word
                text = self.font.render(line, True, self.font_color)
                texts.append(text)
                for i in range(len(texts)):
                    if self.text_align == "right":
                        self.screen.blit(texts[i], (self.box.x + self.box.w - texts[i].get_width() - self.box_pad, self.box.y + self.box_pad + i * (self.font_size + self.line_pad)))
                    elif self.text_align == "center":
                        self.screen.blit(texts[i], (self.box.x + (self.box.w - texts[i].get_width()) / 2, self.box.y + self.box_pad + i * (self.font_size + self.line_pad)))
                    elif self.text_align == "left":
                        self.screen.blit(texts[i], (self.box.x + self.box_pad, self.box.y + self.box_pad + i * (self.font_size + self.line_pad)))

    def draw(self):
        self.draw_text()

    def change_text(self, text="", text_end_func=None):
        self.text = text
        self.text_words = []
        self.text_end_func = text_end_func

    @property
    def text_end(self):
        return len(self.text_words) >= len(self.text.split(" "))

    @property
    def text_trigger(self):
        now = pg.time.get_ticks()
        if self.prev_time + self.text_time < now:
            self.prev_time = now
            return True
        return False
