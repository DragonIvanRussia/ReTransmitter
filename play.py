import os
import sys
import essentials
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(name):
    with open(name, encoding="utf8") as f:
        text = f.readlines()
        level_event = []
        for i in text:
            a = tuple(i.rstrip().split(";"))
            level_event.append(a)
        return level_event


class Image(pygame.sprite.Sprite):

    def __init__(self, name, pos, *groups):
        super().__init__(*groups)
        self.image = load_image(name)
        self.rect = self.image.get_rect().move(pos)


class Player(pygame.sprite.Sprite):

    def __init__(self, inp, *groups):
        self.size = 20, 75
        super().__init__(*groups)
        self.image = pygame.transform.scale(load_image("placeholder2.png"), self.size)
        self.pos = (200, 375)
        self.rect = self.image.get_rect().move(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
        self.player_pos_record = inp

    def update(self, *args):
        i = pygame.key.get_pressed()
        delta_x = 75 if i[pygame.K_DOWN] else 25
        a, b = 1, 1
        if i[pygame.K_LEFT] and a:
            self.rect.x -= delta_x
            if self.rect.x < 50:
                self.rect.x += delta_x
            self.player_pos_record.append((pygame.time.get_ticks() - starting_point, self.rect.x))
            a = 0
        if i[pygame.K_RIGHT] and b:
            self.rect.x += delta_x
            if self.rect.x > 350 - self.size[0]:
                self.rect.x -= delta_x
            self.player_pos_record.append((pygame.time.get_ticks() - starting_point, self.rect.x))
            b = 0
        if i[pygame.K_LEFT] and b:
            a = 1
        if i[pygame.K_RIGHT] and a:
            b = 1


class Noise(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self.size = 300, 150
        super().__init__(*groups)
        self.image = load_image("noise.png")
        self.pos = (200, 375)
        self.alpha = 0
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect().move(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
        self.counter = 0

    def noise(self):
        self.alpha = 255
        self.image.set_alpha(self.alpha)

    def disappear(self):
        if self.alpha:
            self.alpha = (1 - (self.counter / (30000 / bpm_x))) ** 4 * 255 - 2
            if self.alpha < 0:
                self.alpha = 0
            self.counter += 1
        self.image.set_alpha(self.alpha)


class Wave(pygame.sprite.Sprite):
    def __init__(self, inp, *groups):
        self.size = 50, 125
        super().__init__(*groups)
        self.image = load_image("wave_hitbox.png")
        self.pos = (200, 375)
        self.rect = self.image.get_rect().move(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
        self.wave_pos_record = inp

    def update(self, *args):
        a = 0

    def event_move(self, event_move):
        if event_move == "dash_left":
            self.rect.x -= 75
        elif event_move == "left":
            self.rect.x -= 25
        elif event_move == "right":
            self.rect.x += 25
        elif event_move == "dash_right":
            self.rect.x += 75
        self.wave_pos_record.append((pygame.time.get_ticks() - starting_point, self.rect.x))


def converted_pos(x, t, wave_pos_record):
    return 400 + x, 50 + t / wave_pos_record[-1][0] * 500


def load_table(screen, player_pos_record, wave_pos_record):
    pygame.draw.rect(screen, (10, 5, 15), (450, 50, 300, 500))
    for time, pos_record in player_pos_record:
        pygame.draw.circle(screen, (255, 255, 255), converted_pos(pos_record, time, wave_pos_record), 3)


class RadioSignal(pygame.sprite.Sprite):
    def __init__(self, bpm, *groups):
        self.size = 50, 50
        super().__init__(*groups)
        self.image = pygame.transform.scale(load_image("radio_signal.png"), self.size)
        self.pos = (325, 253)
        self.alpha = 0
        self.time = 0
        self.bpm = bpm
        self.rect = self.image.get_rect().move(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)

    def blink(self):
        self.time = pygame.time.get_ticks()
        self.alpha = 255
        self.image.set_alpha(self.alpha)

    def blink_fade(self):
        if self.time and self.alpha:
            self.alpha = 255 - ((pygame.time.get_ticks() - self.time) / (30000 / bpm_x)) * 255
            if self.alpha < 0:
                self.alpha = 0
        self.image.set_alpha(self.alpha)


def init():
    global running, up_hit, bpm_x
    end_screen = 0
    all_sprite = pygame.sprite.Group()
    end_sprite = pygame.sprite.Group()

    running = True
    fps = 60
    up_hit = 0
    noise_reduction = 0
    cooldown = 0
    process_cd = 0

    acc = 1
    acc_ticks = 0
    total_ticks = 0

    level_events = load_level("test_level_1.txt")
    time_until_event = int(level_events[0][0])
    bpm = 120
    bpm_x = bpm

    player_pos_record = []
    wave_pos_record = []

    layout = Image("layout.png", (0, 0), all_sprite)
    wave = Wave(wave_pos_record, all_sprite)
    radio_signal = RadioSignal(bpm, all_sprite)
    noise = Noise(all_sprite)
    player = Player(player_pos_record, all_sprite)
    template = essentials.Image(load_image("stable.png"), (0, 0), (0, 0), all_sprite)

    return locals()
