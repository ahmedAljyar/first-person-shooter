from text import *


class Instructions(Text):
    def __init__(self, screen, font_kind="arial", font_size=30, font_color="white", line_pad=5, height=50, text_time=100):
        super().__init__(screen, font_kind=font_kind, font_size=font_size, font_color=font_color, box_color=None, box=pg.Rect(0, height, screen.get_width(), 0), line_pad=line_pad, box_pad=0, text_time=text_time, text_align="center")
        self.instructions_time = 0
        self.prev_instructions_time = 0

    def update(self):
        super().update()
        self.instruction_end()

    def instruction_end(self):
        now = pg.time.get_ticks()
        if self.prev_instructions_time and self.prev_instructions_time + self.instructions_time < now:
            self.prev_instructions_time = 0
            self.change_text()
            self.instructions_time = 0

    def change_instruction(self, text, time):
        self.change_text(text, self.start_timer)
        self.prev_instructions_time = 0
        self.instructions_time = time

    def start_timer(self):
        self.prev_instructions_time = pg.time.get_ticks()
