import os
import sys
import essentials
import pygame
import random
from foundation import *

def load_level(name):
    global music_name, bpm
    with open(name, encoding="utf8") as f:
        text = f.readlines()
        level_event = []
        counter = 0
        for i in text:
            if not counter:
                music_name, bpm = i[:-1].split(";")
                bpm = int(bpm)
            else:
                a = tuple(i.rstrip().split(";"))
                level_event.append(a)
            counter += 1
        return level_event

class Animation(pygame.sprite.Sprite):
    def __init__(self, image_size, name, frames, tickrate, *groups):
        global level
        super().__init__(*groups)
        self.frame_count = frames
        self.name = name
        self.size = image_size
        self.image_list = []
        self.tickrate = tickrate
        self.time = pygame.time.get_ticks()
        self.current_frame = 0
        for i in range(frames):
            self.image_list.append(pygame.transform.scale(load_image(f"level-{level}/{name}_{i}.png"), self.size))
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()

    def update_frame(self):
        frame = (pygame.time.get_ticks() - self.time) // int(self.tickrate)
        self.image = self.image_list[frame % self.frame_count]
        self.rect = self.image.get_rect()

    def change_frame_list(self, name, frame_count):
        global level
        self.image_list = []
        self.frame_count = frame_count
        for i in range(self.frame_count):
            self.image_list.append(pygame.transform.scale(load_image(f"{name}_{i}.png"), self.size))
        self.time = pygame.time.get_ticks()
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()

class Image(pygame.sprite.Sprite):
    def __init__(self, name, pos, *groups):
        super().__init__(*groups)
        self.image = load_image(name)
        self.rect = self.image.get_rect().move(pos)

class Status(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.font = pygame.font.Font('fonts/DSEG7Classic-Bold.ttf', 24)
        self.image = pygame.Surface((315, 245), pygame.SRCALPHA)
        self.rect = self.image.get_rect().move(pos)
        self.counter = 1
        self.type = 0
        self.time = '00:00'
        
    def update(self, event):
        global accuracy, distance
        if self.counter % 6 == 0:
            self.image = pygame.Surface((315, 324), pygame.SRCALPHA)
            if self.counter % 20 == 0:
                if (self.counter // 60) % 60 < 10:
                    seconds = '0' + str((self.counter // 60) % 60)
                else:
                    seconds = str((self.counter // 60) % 60)
                if self.counter // 3600 < 10:
                    minutes = '0' + str(self.counter // 3600)
                else:
                    minutes = str(self.counter // 3600)
                self.time = f"{minutes}:{seconds}"
            if self.counter % 420 == 0:
                self.type += 1
                self.type %= 2
            if self.type == 0:
                self.image.blit(self.font.render(str(round(accuracy, 2)), 0, (241, 156, 48)), (0, 0))
                self.image.blit(self.font.render(self.time, 0, (241, 156, 48)), (222, 0))
            elif self.type == 1:
                text = f'21-09-09            16:0{4 + self.counter // 3600}'
                self.image.blit(self.font.render(text, 0, (241, 156, 48)), (0, 0))
            self.image.blit(self.font.render('    ' + str(28390 + (distance // 5)), 0, (241, 156, 48)), (0, 221))
            

        self.counter += 1

class Field(pygame.sprite.Sprite):
    def __init__(self, *actors, player, group):
        super().__init__(group)
        self.image = pygame.Surface((326, 177), pygame.SRCALPHA)
        self.rect = self.image.get_rect().move(24, 333)
        self.actors = actors
        self.player = player

    def update(self, args):
        self.image = pygame.Surface((326, 177), pygame.SRCALPHA)
        for elem in self.actors:
            elem.update(args)
            self.image.blit(elem.image, elem.rect[:2])
        self.image.blit(self.player.image, self.player.rect[:2])


class Player(pygame.sprite.Sprite):
    def __init__(self, inp, *groups):
        self.size = 100, 26
        super().__init__(*groups)
        self.image = pygame.transform.scale(load_image("sight.png"), self.size)
        self.pos = (168, 86)
        self.rect = self.image.get_rect().move(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
        self.player_pos_record = inp
        
    def update(self, *args):
        global keybinds
        i = args[0]
        delta_x = 75 if i[keybinds[2]] else 25
        a, b = 1, 1
        if i[keybinds[0]] and a:
            self.rect.x -= delta_x
            self.player_pos_record.append((pygame.time.get_ticks() - starting_point, self.rect.x))
            a = 0
        if i[keybinds[1]] and b:
            self.rect.x += delta_x
            self.player_pos_record.append((pygame.time.get_ticks() - starting_point, self.rect.x))
            b = 0
        if i[keybinds[0]] and b:
            a = 1
        if i[keybinds[1]] and a:
            b = 1


class Noise(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self.size = 326, 100
        super().__init__(*groups)
        self.passive = pygame.Surface(self.size, pygame.SRCALPHA)
        self.image = self.passive
        self.pos = (163, 35)
        self.alpha = 15
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect().move(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
        self.counter = 0

    def update(self, args):
        if self.counter % 6 == 0:
            self.passive = pygame.Surface(self.size, pygame.SRCALPHA)
            for count in range(0, 326):
                pygame.draw.line(self.passive, (241, 156, 48), (count, 100 - random.randint(0, self.alpha) / 3), (count, 100))
            self.image = self.passive
            self.counter = 0
        self.counter += 1

    def noise(self):
        self.alpha = 90
    
    def disappear(self):
        if self.alpha > 15:
            self.alpha -= 1

class Wave(pygame.sprite.Sprite):
    def __init__(self, inp, *groups):
        self.size = 50, 125
        super().__init__(*groups)
        self.image = load_image("wave_hitbox.png")
        self.pos = (128, 46)
        self.rect = self.image.get_rect().move(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
        self.image_buf = [pygame.Surface((1, 1)), pygame.Surface((1, 1))]
        self.wave_pos_record = inp
        self.counter = 0

    def event_move(self, event_move):
        global cooldown
        if event_move == "dash_left":
            self.rect.x -= 75
        elif event_move == "left":
            self.rect.x -= 25
        elif event_move == "right":
            self.rect.x += 25
        elif event_move == "dash_right":
            self.rect.x += 75
        cooldown = 6
        self.wave_pos_record.append((pygame.time.get_ticks() - starting_point, self.rect.x))


def converted_pos(x, t, wave_pos_record):
    return x + 7, 50 + t / wave_pos_record[-1][0] * 500


def load_table(screen, player_pos_record, wave_pos_record):
    image = pygame.Surface((250, 500))
    pygame.draw.rect(image, (10, 5, 15), (0, 0, 250, 500))
    for time, pos_record in player_pos_record:
        result = converted_pos(pos_record, time, wave_pos_record)
        pygame.draw.circle(image, (255, 255, 255), result, 3)
    screen.blit(image, (450, 50))


class RadioSignal(pygame.sprite.Sprite):
    def __init__(self, bpm, *groups):
        self.size = 50, 50
        super().__init__(*groups)
        self.image = pygame.transform.scale(load_image("radio_signal.png"), self.size)
        self.pos = (371, 309)
        self.alpha = 0
        self.time = 0
        self.quick = 0
        self.bpm = bpm
        self.rect = self.image.get_rect().move(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
        self.counter = True
    
    def blink(self):
        self.time = pygame.time.get_ticks()
        self.alpha = 255
        self.image.set_alpha(self.alpha)
        if self.counter:
            turn_sound.play()
            self.counter = False

    def blink_fade(self):
        bpm = self.bpm
        tick = 20000 if self.quick else 40000
        if self.time and self.alpha:
            self.alpha = 255 - ((pygame.time.get_ticks() - self.time) / (tick / bpm)) * 255
            if self.alpha < 0:
                self.alpha = 0
            if self.alpha < 200:
                self.counter = True
        self.image.set_alpha(self.alpha)


class Dialogue(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self.size = 1000, 50
        super().__init__(*groups)
        self.y = 0
        self.image = pygame.transform.scale(load_image("dialogue_bar.png"), self.size)
        self.font = pygame.font.Font(None, 36)
        self.rect = self.image.get_rect()
        self.rect.move_ip(0, self.y)
        self.rendered_text = 0

    def render_text(self, text):
        text_render = self.font.render(text, 1, (0, 0, 0))
        text_rect = text_render.get_rect()
        text_rect.move_ip(50, self.y + 10)
        self.rendered_text = text_render, text_rect

def init(level):
    global running, up_hit, bpm_x, quit, turn_sound, cooldown
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
    quit = 0

    turn_sound = pygame.mixer.Sound("sounds/turn.mp3")    
    level_data = load_level(f"chart/level_{level}.txt")
    time_until_event = int(level_data[0][0])
    bpm = 162
    bpm_x = bpm

    player_pos_record = []
    wave_pos_record = []
    
    car_view = Animation((450,  270), f"stable", 2, 60000 / bpm, all_sprite)
    radio = Image("radio.png", (0, 0), all_sprite)
    wave = Wave(wave_pos_record)
    radio_signal = RadioSignal(bpm, all_sprite)
    on = RadioSignal(bpm, all_sprite)
    on.rect.x, on.rect.y, on.alpha = 372, 285, 20
    on.image = pygame.transform.scale(load_image("power_signal.png"), on.size)
    on.blink()
    noise = Noise()
    player = Player(player_pos_record)
    stable = 0

    closed = load_image('noise-button-pressed.png', -1)
    opened = load_image('noise-button.png')
    
    button = Image('noise-button.png', (283, 520), all_sprite)
    status = Status((26, 302))
    
    waves = Field(wave, noise, status, player=player, group=all_sprite)
    
    return locals()

def action(car_view, level, level_events, shown):
    if not shown:
        if level == 3 and level_events[1].startswith("dash"):
            car_view.change_frame_list(f"level-{level}\\{level_events[1]}", 4)
        else:
            car_view.change_frame_list(f"level-{level}\\{level_events[1]}", 2)
    return True

def generate(level):
    file = open(f"chart/level_{level}_wave.txt", 'r')
    output = []
    data = file.read().split(';')
    for elem in data:
        image = pygame.Surface((258, 100), pygame.SRCALPHA)
        final = elem.split(',')
        for count, value in enumerate(final):
            pygame.draw.line(image, (241, 156, 48), (count + 129, 100 - float(value)), (count + 129, 100))
        image.blit(pygame.transform.flip(image, True, False), (0, 0))
        output.append(pygame.transform.scale(image, (129, 100)))
    return output
