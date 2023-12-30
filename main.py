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

def intro():
    pygame.event.pump()
    text = ["Game inspired by Rhythm Doctor and...", "Hold on this isnt ReTransmitter...", "wait", "...", "OMG"]
    timing = [3000, 2500, 1500, 1700, 1300]
    for i in range(len(text)):
        screen.fill("black")
        font = pygame.font.SysFont(None, 48)
        img = font.render(text[i], True, (255, 255, 255))
        location = (1000 - img.get_rect()[2]) / 2
        screen.blit(img, (location, 200))
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.delay(timing[i])

    screen.fill("black")
    font = pygame.font.SysFont(None, 48)
    img = font.render("NO WAY IT'S", True, (255, 255, 255))
    screen.blit(img, (400, 200))
    pygame.display.flip()
    pygame.time.delay(1000)
    
    screen.blit(intro_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

def SwitchModes():
    global cooldown, last, status, start_btn
    if cooldown <= 0:
        misc = False
        for sprite_object in menu.main.sprites():
            sprite_object.switch()
        for sprite_object in menu.settings.sprites():
            sprite_object.switch()
        for sprite_object in menu.levels.sprites():
            sprite_object.switch()
        if play_btn.state:
            play_btn.replace()
            
        cooldown = 100
        last = status
        status = "Transition"
        
        if last == "Settings":
            fake_bar.replace()
        else:
            fake_bar.switch()

def hide():
    global misc, cooldown
    if cooldown <= 0:
        misc = True
        cooldown = 100
        
        for sprite_object in menu.settings.sprites():
            if sprite_object == bar:
                bar.replace()
            elif sprite_object == closing:
                closing.action = show
            else:
                sprite_object.switch()
        fake_bar.switch()

def show():
    global misc, cooldown
    if cooldown <= 0:
        misc = True
        cooldown = 100
        
        for sprite_object in menu.settings.sprites():
            if sprite_object == closing:
                closing.action = SwitchModes
            else:
                sprite_object.switch()
        fake_bar.switch()

def Audio():
    hide()

def Config():
    hide()

def Language():
    hide()

def Credit():
    hide()

def Play():
    print("init")
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('ReTransmitter')
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    running = True
    clock = pygame.time.Clock()

    pygame.mixer.music.load("sounds/bgm.mp3")
    pygame.mixer.music.play(-1)
    
    status = "Menu"
    last = "Settings"
    misc = False
    cooldown = 100
    ticks = 0
    
    bg_color = (0, 50, 100)
    BG = BGColor((0, 120, 160), "sine", 500)
    placeholder = load_image("placeholder.png")
    placeholder2 = load_image("placeholder2.png")
    intro_img = pygame.transform.scale(load_image("intro.png"), (1000, 600))
    icon = load_image("icon.png")
    
    audio_img = load_image("audio.png")
    settings_img = load_image("settings.png")

    # intro()

    side_bar = load_image("side_bar.png")
    side_bar2 = load_image("side_bar2.png")
    Lexend = 'fonts/Lexend-Medium.ttf'

    credits_icon = pygame.transform.scale(load_image("icon-credits.png"), (100, 100))
    settings_icon = pygame.transform.scale(load_image("icon-settings.png"), (100, 100))
    audio_icon = pygame.transform.scale(load_image("icon-audio.png"), (100, 100))
    
    forest_img = load_image("level-forest.png")
    thunder_img = load_image("level-thunder.png")
    city_img = load_image("level-city.png")
    
    menu.SideBar(side_bar2)
    info = menu.InfoBar(placeholder)
    menu.TopBar(placeholder, (Lexend, 60))
    
    bar = menu.SettingsBar(side_bar)
    fake_bar = menu.Object(side_bar, (-250, 0, 350, 600), (0, 0), menu.misc)
    settings_btn = menu.Button(settings_icon, SwitchModes, rect=[25, 25, 100, 100], orig=[-125, 25], groups=menu.main)
    play_btn = menu.Button(placeholder2, Play, rect=[800, 540, 200, 60], orig=[800, 800], groups=menu.buttons)
    closing = menu.Button(icon, SwitchModes, rect=[-60, 5, 50, 50], orig=[5, 5], groups=menu.settings)
    
    audio_image = menu.Image(audio_img, (1000, 100), (500, 100), menu.settings)
    settings_image = menu.Image(settings_img, (1000, 100), (500, 100), menu.settings)
    language_image = menu.Image(audio_img, (1000, 100), (500, 100), menu.settings)
    credit_image = menu.Image(settings_img, (1000, 100), (500, 100), menu.settings)
    
    audio = menu.Settings_Select(audio_icon, "Audio", (Lexend, 64), (10, 80, 100, 100), Audio, menu.settings)
    settings = menu.Settings_Select(settings_icon, "Settings", (Lexend, 64), (10, 215, 100, 100), Config, menu.settings)
    language = menu.Settings_Select(icon, "Language", (Lexend, 64), (10, 345, 100, 100), Language, menu.settings)
    credit = menu.Settings_Select(credits_icon, "Credits", (Lexend, 64), (10, 480, 100, 100), Credit, menu.settings)

    forest = menu.Level(forest_img, 0, info.select)
    highway = menu.Level(thunder_img, 1, info.select)
    city = menu.Level(city_img, 2, info.select)
    bus = menu.Level(icon, 3, info.select)

    info.connect(play_btn)
    play_btn.replace()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        BG()
        screen.fill(bg_color)
        screen.blit(menu.bg, (ticks % 100 - 100, ticks % 80 - 80))

        if misc:
            menu.misc.update(event)
            menu.misc.draw(screen)
        
        if status == "Settings" or status == "Transition":
            menu.settings.update(event)
            menu.settings.draw(screen)
        
        if status == "Menu" or status == "Transition":
            menu.levels.update(event)
            menu.levels.draw(screen)
            menu.main.update(event)
            menu.main.draw(screen)

        menu.buttons.update(event)
        menu.buttons.draw(screen)
        
        if cooldown == 0:
            if last == "Menu":
                status = "Settings"
            elif last == "Settings":
                status = "Menu"
        cooldown -= 1
        ticks += 1
        clock.tick(60)
        if cooldown % 100 == 0:
            print(clock.get_fps())
        pygame.display.flip()
    pygame.quit()
