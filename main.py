import pygame
import menu
from foundation import *


class BGColor():
    def __init__(self, delta, variation='linear', *args):
        global bg_color
        self.delta = delta
        self.variation = variation
        self.args = args
        self.original = bg_color
        if self.variation == 'sine' and len(self.args) == 1:
            self.args = (0, self.args[0])

    def __call__(self):
        global bg_color
        bg_color = ColorDelta(bg_color, self.delta, self.variation, *self.args, self.original)
        if self.variation == 'sine':
            self.args = (self.args[0] + 1, self.args[1])

def test():
    print("hi")

def SwitchModes():
    print(1)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('ReTransmitter')
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    running = True
    clock = pygame.time.Clock()
    
    status = "Menu"
    last = "Settings"
    cooldown = 100
    ticks = 0
    
    bg_color = (0, 20, 80)
    placeholder = load_image("placeholder.png")
    placeholder2 = load_image("placeholder2.png")
    placeholder3 = load_image("placeholder3.png")
    BG = BGColor((0, 80, 160), "sine", 500)
    
    menu.SideBar(screen, placeholder)
    info = menu.InfoBar(screen, placeholder)
    menu.TopBar(screen, placeholder)
    # menu.Button(screen, placeholder, SwitchModes, debug=True)
    
    menu.SettingsBar(screen, placeholder2)
    menu.Image(screen, placeholder3, (1000, 100), (500, 100), menu.settings)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if cooldown <= 0:
                    for sprite_object in menu.main.sprites():
                        sprite_object.switch()
                    for sprite_object in menu.settings.sprites():
                        sprite_object.switch()
                    cooldown = 100
                    last = status
                    status = "Transition"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                info.select()
        
        BG()
        screen.fill(bg_color)
        screen.blit(menu.bg, (ticks % 100 - 100, ticks % 100 - 100))
        
        if status == "Settings" or status == "Transition":
            menu.settings.update(event)
            menu.settings.draw(screen)
        if status == "Menu" or status == "Transition":
            menu.main.update(event)
            menu.main.draw(screen)
        if cooldown == 0:
            if last == "Menu":
                status = "Settings"
            elif last == "Settings":
                status = "Menu"
        
        cooldown -= 1
        ticks += 1
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
