from settings import *
from texts import *


class Conversation:
    def __init__(self, game, font_kind="arial", font_size=30, line_pad=10, box_pad=10, font_color="white", box_color="black", chat_time=100):
        self.game = game
        self.conversation = {"texts": [], "options": []}
        self.texts = Texts(game.screen, box=pg.Rect(10, height - 210, width - 20, 200))
        self.options = []
        self.show_options = False
        self.topics = {}
        self.current_topic = ""
        self.conv = False
        self.talker = None
        self.conv_end_func = None

    def update(self):
        if self.texts.texts:
            self.conv = True
            self.events()
            if self.texts.texts_end and self.options:
                self.show_options = True
            else:
                self.show_options = False
        else:
            self.conv = False
            self.show_options = False
        self.texts.update()
        for option in self.options:
            option.update()

    def draw_options(self):
        if self.options:
            [option.draw() for option in self.options]

    def change_conversation(self, texts, options=None, topic="", talker=None, conv_end_func=None):
        if options is None:
            options = []
        self.conversation = {"texts": texts, "options": options}
        self.texts.change_texts(texts)
        self.talker = talker
        self.current_topic = topic
        self.options = []
        for i in range(len(options)):
            self.options.append(Text(self.game.screen, text_align="center", font_size=20, text=options[i], box=pg.Rect(width / 2 - 200, self.texts.box.y + ((50 + 5) * -(i + 1)), 400, 50), text_time=0))
        self.conv_end_func = conv_end_func

    def draw(self):
        if self.texts.texts:
            self.texts.draw()
            if self.show_options:
                self.draw_options()

    def events(self):
        if pg.BUTTON_LEFT in self.game.mouse_up or pg.K_SPACE in self.game.key_up:
            if not self.show_options:
                end = 0
                if self.texts.texts:
                    end += 1
                self.texts.update_texts()
                if not self.texts.texts:
                    end += 1

                # conversation end
                if end == 2:
                    self.topics[self.current_topic] = ""
                    if self.talker is not None:
                        self.talker.topics[self.current_topic] = ""
                    self.current_topic = ""
                    if self.conv_end_func is not None:
                        self.conv_end_func("")
            else:
                if pg.BUTTON_LEFT in self.game.mouse_up:
                    mx, my = self.game.get_mouse_pos
                    for option in self.options:
                        # conversation end
                        if option.box.collidepoint(mx, my):
                            self.topics[self.current_topic] = option.text
                            if self.talker is not None:
                                self.talker.topics[self.current_topic] = option.text
                            self.texts.update_texts()
                            if self.conv_end_func is not None:
                                self.conv_end_func(option.text)
                            break

    def is_topic(self, topic):
        return topic in self.topics

    def get_topic(self, topic):
        if self.is_topic(topic):
            return self.topics[topic]

    def is_topic_result(self, topic, result):
        return self.is_topic(topic) and self.topics[topic] == result

    def topic_results(self, topic):
        if self.is_topic(topic):
            return self.topics[topic]
        else:
            return None
