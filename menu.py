import pygame
from foundation import *


class Object(pygame.sprite.Sprite):
    def __init__(self, screen, img, rect=[0, 0, 100, 100], groups=[]):
        super().__init__(groups)
        self.image = pygame.transform.scale(img, (rect[2], rect[3]))
        self.rect = self.image.get_rect()
        self.parent = screen
        self.rect.x = rect[0]
        self.rect.y = rect[1]
        self.frame = 0
        self.limit = 100
        self.state = True

    def move(self, delta=(0, 0)):
        x, y = delta


class Button(Object):
    def __init__(self, screen, img, command, text="generic", rect=[0, 0, 100, 100]):
        global buttons
        self.action = command
        self.shown = True
        self.clicked = False
        super().__init__(screen, img, debug, groups=buttons, rect=rect)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and args[0].button == pygame.BUTTON_LEFT:
            if self.shown and self.rect.collidepoint(args[0].rect) and not self.clicked:
                self.clicked = True
                self.action()
        if args and args[0].type == pygame.MOUSEBUTTONUP and args[0].button == pygame.BUTTON_LEFT:
            self.clicked = False

    def check_if_click(self):
        if self.rect.collidepoint(pygame.mouse.get_rect()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                self.command()
                self.pressed = 0
            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 1

        
class SideBar(Object):
    def __init__(self, screen, img):
        global main
        self.rect = (0, 0, 150, 600)
        self.parent = screen
        super().__init__(screen, img, groups=main, rect=self.rect)

    def update(self, args):
        if self.frame != self.limit and self.state:
            self.frame += 1
            a = MoveDelta((-150, 0), (0, 0), 'quad', self.frame, self.limit)
            self.rect = (a[0], a[1], 150, 600)
        elif self.frame != self.limit and not self.state:
            self.frame += 1
            a = MoveDelta((0, 0), (-150, 0), 'quad', self.frame, self.limit)
            self.rect = (a[0], a[1], 150, 600)
        

    def switch(self):
        self.state = not self.state
        self.frame = 0


class SettingsBar(Object):
    def __init__(self, screen, img, debug=False):
        global main
        self.rect = (0, 0, 300, 600)
        self.parent = screen
        self.state = False
        super().__init__(screen, img, groups=settings, rect=self.rect)

    def update(self, args):
        if self.frame != self.limit and self.state:
            self.frame += 1
            a = MoveDelta((0, 0), (-300, 0), 'quad', self.frame, self.limit)
            self.rect = (a[0], a[1], 300, 600)
        elif self.frame != self.limit and not self.state:
            self.frame += 1
            a = MoveDelta((-300, 0), (0, 0), 'quad', self.frame, self.limit)
            self.rect = (a[0], a[1], 300, 600)
        

    def switch(self):
        self.state = not self.state
        self.frame = 0
    

class TopBar(Object):
    def __init__(self, screen, img):
        global main
        self.rect = (0, 0, 1000, 60)
        self.parent = screen
        super().__init__(screen, img, groups=main, rect=self.rect)

    def update(self, args):
        if self.frame != self.limit and self.state:
            self.frame += 1
            a = MoveDelta((0, -60), (0, 0), 'quad', self.frame, self.limit)
            self.rect = (a[0], a[1], 1000, 60)
        elif self.frame != self.limit and not self.state:
            self.frame += 1
            a = MoveDelta((0, 0), (0, -60), 'quad', self.frame, self.limit)
            self.rect = (a[0], a[1], 1000, 60)
        

    def switch(self):
        self.state = not self.state
        self.frame = 0


class Image(Object):
    def __init__(self, screen, img, pos, orig, groups=[]):
        global main
        self.pos = pos
        self.orig = orig
        self.rect = img.get_rect()
        self.rect.move_ip(pos)
        self.parent = screen
        super().__init__(screen, img, self.rect, groups)

    def update(self, args):
        if self.frame != self.limit and self.state:
            self.frame += 1
            a = MoveDelta(self.orig, self.pos, 'quad', self.frame, self.limit)
            self.rect = (a[0], a[1], self.rect[2], self.rect[3])
        elif self.frame != self.limit and not self.state:
            self.frame += 1
            a = MoveDelta(self.pos, self.orig, 'quad', self.frame, self.limit)
            self.rect = (a[0], a[1], self.rect[2], self.rect[3])
        

    def switch(self):
        self.state = not self.state
        self.frame = 0


class InfoBar(Object):
    def __init__(self, screen, img):
        global main
        self.rect = [0, 520, 1000, 150]
        self.prop = 520
        self.retracted = True
        self.state = False
        self.selected = False
        super().__init__(screen, img, groups=main, rect=self.rect)

    def select(self):
        if not self.retracted:
            if self.selected:
                self.prop = 520
            else:
                self.prop = 450
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
        

    def switch(self):
        self.state = not self.state
        self.frame = 0
        


buttons = pygame.sprite.Group()
main = pygame.sprite.Group()
settings = pygame.sprite.Group()

buf = load_image("placeholder4.png")
buf.fill((255, 255, 255, 50), None, pygame.BLEND_RGBA_MULT)

bg = pygame.Surface((1100, 700), pygame.SRCALPHA)

for i in range(0, 11):
    for j in range(0, 8):
        bg.blit(buf, (i * 100, j * 100))
