import pygame
from foundation import *


class Object(pygame.sprite.Sprite):
    def __init__(self, img, rect=[0, 0, 100, 100], orig=[0, 0], groups=[]):
        super().__init__(groups)
        self.image = pygame.transform.scale(img, (rect[2], rect[3]))
        self.rect = self.image.get_rect()
        self.rect.x = rect[0]
        self.rect.y = rect[1]
        
        self.orig = orig
        self.point = rect[:2]
        
        self.frame = 0
        self.limit = 100
        self.state = True

    def move(self, delta=(0, 0)):
        x, y = delta

    def update(self, event):
        if self.frame != self.limit and self.state:
            self.frame += 1
            a = MoveDelta(self.orig, self.point, 'quad', self.frame, self.limit)
            self.rect = (*a, *self.rect[2:])
        elif self.frame != self.limit and not self.state:
            self.frame += 1
            a = MoveDelta(self.point, self.orig, 'quad', self.frame, self.limit)
            self.rect = (*a, *self.rect[2:])
        
    def replace(self):
        self.switch()
        self.frame = self.limit - 1
        
    
    def switch(self):
        self.state = not self.state
        self.frame = 0


class Button(Object):
    def __init__(self, img, command, text="generic", rect=[0, 0, 100, 100], orig=[0,0], groups=[]):
        global buttons
        self.action = command
        self.shown = True
        self.clicked = False
        super().__init__(img, groups=groups, rect=rect, orig=orig)

    def update(self, *args, cont=True):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and args[0].button == pygame.BUTTON_LEFT:
            if self.shown and pygame.Rect(self.rect).collidepoint(args[0].pos) and not self.clicked:
                self.clicked = True
                self.action()
        if args and args[0].type == pygame.MOUSEBUTTONUP and args[0].button == pygame.BUTTON_LEFT:
            self.clicked = False
        if cont:
            super().update(None)

class Settings_Select(Button):
    def __init__(self, img, text, font, rect, action, groups):
        global buttons
        try:
            buf = pygame.font.SysFont(*font)
        except:
            buf = pygame.font.Font(*font)
        text = buf.render(text, True, (255, 255, 255))
        
        buf = pygame.Surface((rect[2] + text.get_width(), rect[3]), pygame.SRCALPHA)
        buf.blit(img, (0, 0))
        buf.blit(text, (rect[2], (rect[3] - text.get_rect()[3]) / 2))
        
        size = buf.get_rect()[2:]
        self.rect = pygame.Rect(rect[0], rect[1], *size)
        self.orig = self.rect

        self.sel = 0
        self.Lsel = 0
        self.last_pos = (0, 0)
        
        super().__init__(buf, action, rect=self.rect, groups=groups, orig=self.orig)

    def update(self, *args):
        if self.frame != self.limit and self.state:
            self.frame += 1
            a = MoveDelta(self.orig[:2], (-400, self.orig[1]), 'quad', self.frame, self.limit)
            self.rect = pygame.Rect(a[0], a[1], *self.rect[2:])
        elif self.frame != self.limit and not self.state:
            self.frame += 1
            a = MoveDelta((-400, self.orig[1]), self.orig[:2], 'quad', self.frame, self.limit)
            self.rect = pygame.Rect(a[0], a[1], *self.rect[2:])
        
        if args and args[0].type == pygame.MOUSEMOTION:
            self.last_pos = args[0].pos

        if self.frame == self.limit:
            self.Lsel = self.sel
            if self.shown and pygame.Rect(self.rect).collidepoint(self.last_pos):
                self.sel += 1
            else:
                self.sel -= 1
            if self.sel < 0:
                self.sel = 0
            elif self.sel > 20:
                self.sel = 20
            self.rect.x = self.rect.x + self.sel - self.Lsel
        super().update(*args, cont=False)

    def switch(self):
        self.state = not self.state
        self.frame = 0


class Level(Object):
    def __init__(self, img, state, command, rect=[0, 0, 100, 100]):
        global level
        if state == 0:
            self.x_frame = 0
            self.y_frame = 150
        elif state == 1:
            self.x_frame = 50
            self.y_frame = 0
        elif state == 2:
            self.x_frame = 100
            self.y_frame = 50
        elif state == 3:
            self.x_frame = 150
            self.y_frame = 100
            
        self.x_offset = 0
        self.y_offset = 0
        self.action = command
        self.clicked = True
        self.shown = True
        self.selected = False
        self._layer = 0
        self.sel = 0
        self.last_pos = (-100, -100)
        
        super().__init__(img, rect, groups=levels)

    def click(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and args[0].button == pygame.BUTTON_LEFT:
            if self.shown and self.rect.collidepoint(args[0].pos) and not self.clicked:
                self.clicked = True
                self.selected = not self.selected
            elif not self.rect.collidepoint(args[0].pos) and pygame.Rect((150, 60, 850, 390)).collidepoint(args[0].pos):
                self.selected = False
            self.action()
        if args and args[0].type == pygame.MOUSEBUTTONUP and args[0].button == pygame.BUTTON_LEFT:
            self.clicked = False
        if args and args[0].type == pygame.MOUSEMOTION:
            self.last_pos = args[0].pos

    def update(self, args):
        global levels
        
        self.x_frame += 0.3
        self.y_frame += 0.3
        self.rect.x = MoveDelta((300, 200), (750, 300), 'sine', self.y_frame, 100)[0] + self.x_offset
        self.rect.y = MoveDelta((300, 200), (750, 300), 'sine', self.x_frame, 100)[1] + self.y_offset + self.sel
        
        if self.frame != self.limit and self.state:
            self.frame += 1
            a = MoveDelta((0, 500), (0, 0), 'quad', self.frame, self.limit)
            self.y_offset = a[1]
        elif self.frame != self.limit and not self.state:
            self.frame += 1
            a = MoveDelta((0, 0), (0, 500), 'quad', self.frame, self.limit)
            self.y_offset = a[1]
        
        if self.frame == self.limit:
            self.shown = True
            if self.rect.y > 250:
                levels.change_layer(self, 1)
            else:
                levels.change_layer(self, 0)
        if args != ():
            self.click(args)

        if self.shown and self.rect.collidepoint(self.last_pos) or self.selected:
            self.sel -= 1
        else:
            self.sel += 1
        if self.sel < -20:
            self.sel = -20
        elif self.sel > 0:
            self.sel = 0
        
    
    def switch(self):
        self.state = not self.state
        self.frame = 0
        
class SideBar(Object):
    def __init__(self, img):
        global main
        self.rect = (0, 0, 150, 600)
        super().__init__(img, groups=main, rect=self.rect, orig=(-150, 0))


class SettingsBar(Object):
    def __init__(self, img):
        global main
        self.rect = (-350, 0, 350, 600)
        self.state = False
        super().__init__(img, groups=settings, rect=self.rect)

    

class TopBar(Object):
    def __init__(self, img, font):
        global main
        self.rect = (0, 0, 1000, 60)
        super().__init__(img, groups=main, rect=self.rect, orig=(0, -60))
        
        try:
            buf = pygame.font.SysFont(*font)
        except:
            buf = pygame.font.Font(*font)
        text = buf.render("Main Menu", True, (255, 255, 255))
        self.image.blit(text, (150, 12))


class Image(Object):
    def __init__(self, img, pos, orig, groups=[]):
        global main
        self.pos = pos
        self.orig = orig
        self.rect = img.get_rect()
        self.rect.move_ip(pos)
        self.orig_img = img
        
        super().__init__(img, self.rect, groups=groups, orig=orig)

        

class InfoBar(Object):
    def __init__(self, img):
        global main
        self.rect = [0, 520, 1000, 150]
        self.prop = 520
        self.retracted = True
        self.state = False
        self.selected = False
        super().__init__(img, groups=main, rect=self.rect)

    def select(self):
        level = scan_selected()
        if not self.retracted:
            if level == None:
                if self.prop != 520:
                    self.btn.state = False
                    self.btn.frame = 0
                self.prop = 520
            else:
                if self.prop != 450:
                    self.btn.state = True
                    self.btn.frame = 60
                self.prop = 450
                self.btn.state = True
            self.selected = not self.selected
            self.rect = (0, self.prop, 1000, 150)
    def update(self, args):
        if self.frame != self.limit and self.state:
            self.frame += 1
            a = MoveDelta((0, 600), (0, self.prop), 'quad', self.frame, self.limit)
            self.rect = (a[0], a[1], 1000, 150)
        elif self.frame != self.limit and not self.state:
            self.frame += 1
            a = MoveDelta((0, self.prop), (0, 600), 'quad', self.frame, self.limit)
            self.rect = (a[0], a[1], 1000, 150)
        
        if not self.state:
            self.retracted = True
        if self.frame == self.limit:
            if not self.state:
                self.prop = 520
            else:
                self.retracted = False

    def connect(self, btn):
        self.btn = btn

    def switch(self):
        self.state = not self.state
        self.frame = 0
        

def scan_selected():
    for sprite_object in levels.sprites():
        if sprite_object.selected:
            return sprite_object

misc = pygame.sprite.Group()
buttons = pygame.sprite.Group()
main = pygame.sprite.Group()
settings = pygame.sprite.Group()
levels = pygame.sprite.LayeredUpdates()
selection = pygame.sprite.Group()

audio = pygame.sprite.Group()
config = pygame.sprite.Group()
language = pygame.sprite.Group()
credit = pygame.sprite.Group()

buf = load_image("bg_grid.png")
buf.fill((255, 255, 255, 255), None, pygame.BLEND_RGBA_MULT)
size = buf.get_rect()[2:]
bg = pygame.Surface((1100, 700), pygame.SRCALPHA)

for i in range(0, 12):
    for j in range(0, 9):
        bg.blit(buf, (size[0] * i, size[1] * j))
