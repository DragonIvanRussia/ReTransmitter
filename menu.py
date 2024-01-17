import pygame
import essentials
from foundation import *

def SwitchModes():
    global cooldown, last, status, start_btn
    if cooldown <= 0:
        misc = False
        for sprite_object in essentials.main.sprites():
            sprite_object.switch()
        for sprite_object in essentials.settings.sprites():
            sprite_object.switch()
        for sprite_object in essentials.levels.sprites():
            sprite_object.switch()
        if play_btn.state:
            play_btn.replace()
            
        cooldown = 100
        last = status
        status = "Transition"
        active = None
        
        if last == "Settings":
            fake_bar.replace()
        else:
            fake_bar.switch()

def hide():
    global misc, cooldown
    if cooldown <= 0:
        misc = True
        cooldown = 100
        
        for sprite_object in essentials.settings.sprites():
            if sprite_object == bar:
                bar.replace()
            elif sprite_object == closing:
                closing.action = show
            else:
                sprite_object.switch()
        fake_bar.switch()

def show():
    global misc, cooldown2, cooldown, active, pulse
    if cooldown2 <= 0:
        misc = True
        cooldown2 = 100
        cooldown = 100
        
        for sprite_object in essentials.settings.sprites():
            if sprite_object == closing:
                closing.action = SwitchModes
            else:
                sprite_object.switch()
        fake_bar.switch()
    
        for sprite_object in active.sprites():
            sprite_object.switch()
    pulse = True

def blank(event):
    print('ivan you forgot to link the action')

def call(arg):
    global active, cooldown2
    active = arg
    cooldown2 = 100
    hide()
    for sprite_object in active.sprites():
        sprite_object.switch()

def play():
    global counter_play, exec_status, level
    counter_play = True
    exec_status = "play"
    level = essentials.scan_selected(True)

def init():
    global running, active, cooldown2, cooldown, misc, last, status, play_btn, fake_bar, bar, closing, pulse
    
    status = "Menu"
    last = "Settings"
    misc = False
    active = None
    running = True
    pulse = False

    last = 0
    cooldown = 100
    cooldown2 = 100
    ticks = 0
    transition = 20
    cur_offset = 0
    offset = 0
    set_offset = 0

    BG = BGColor((0, 50, 100), (0, 80, 160), "sine", 500)
    placeholder = load_image("placeholder.png")
    placeholder2 = load_image("placeholder2.png")
    intro_img = pygame.transform.scale(load_image("intro.png"), (1000, 600))
    icon = load_image("icon.png")
    arrow = load_image("arrow.png")
    
    audio_img = load_image("audio.png")
    settings_img = load_image("settings.png")
    lang_img = load_image("language.png")
    credit_img = load_image("credits.png")

    # intro()

    side_bar = load_image("side_bar.png")
    side_bar2 = load_image("side_bar2.png")
    Lexend = 'fonts/Lexend-Medium.ttf'

    credits_icon = pygame.transform.scale(load_image("icon-credits.png"), (100, 100))
    settings_icon = pygame.transform.scale(load_image("icon-settings.png"), (100, 100))
    audio_icon = pygame.transform.scale(load_image("icon-audio.png"), (100, 100))

    tutorial_img = "level-tutorial.png"
    forest_img = "level-forest.png"
    thunder_img = "level-thunder.png"
    city_img = "level-city.png"
    
    essentials.SideBar(side_bar2)
    info = essentials.InfoBar(placeholder)
    essentials.TopBar(placeholder, (Lexend, 60))
    
    bar = essentials.SettingsBar(side_bar)
    fake_bar = essentials.Object(side_bar, (-250, 0, 350, 600), (0, 0), essentials.misc)
    settings_btn = essentials.Button(settings_icon, SwitchModes, rect=[25, 25, 100, 100], orig=[-125, 25], groups=essentials.main)
    play_btn = essentials.Button(placeholder2, play, rect=[800, 540, 200, 60], orig=[800, 800], groups=essentials.buttons)
    closing = essentials.Button(icon, SwitchModes, rect=[-60, 5, 50, 50], orig=[5, 5], groups=essentials.settings)
    
    audio_image = essentials.Image(audio_img, (1000, 100), (450, 100), essentials.settings)
    settings_image = essentials.Image(settings_img, (1000, 700), (450, 700), essentials.settings)
    language_image = essentials.Image(lang_img, (1000, 1300), (450, 1300), essentials.settings)
    credit_image = essentials.Image(credit_img, (1000, 1900), (450, 1900), essentials.settings)
    image_list = [audio_image, settings_image, language_image, credit_image]
    
    audio = essentials.Settings_Select(audio_icon, "Audio", (Lexend, 64), (10, 80, 100, 100), call, essentials.settings, essentials.audio)
    settings = essentials.Settings_Select(settings_icon, "Settings", (Lexend, 64), (10, 215, 100, 100), call, essentials.settings, essentials.config)
    language = essentials.Settings_Select(icon, "Language", (Lexend, 64), (10, 345, 100, 100), call, essentials.settings, essentials.language)
    credit = essentials.Settings_Select(credits_icon, "Credits", (Lexend, 64), (10, 480, 100, 100), call, essentials.settings, essentials.credit)

    audio.assign(0)
    settings.assign(1)
    language.assign(2)
    credit.assign(3)

    forest = essentials.Level(forest_img, 1, info.select)
    highway = essentials.Level(thunder_img, 2, info.select)
    city = essentials.Level(city_img, 3, info.select)
    tutorial = essentials.Level(tutorial_img, 0, info.select)

    info.connect(play_btn)
    play_btn.replace()

    quality = essentials.Text_Selection((250, -500), (250, -500), ['Low', 'Medium', 'High'], "Quality", (Lexend, 64), arrow, essentials.config)
    refresh = essentials.Text_Selection((250, -550), (250, 50), ['60', '100', '120'], "Frame Limiter", (Lexend, 48), arrow, essentials.config)

    down_btn_img = essentials.Selection_Bar((0, 0, 400, 75), ['Link Down Button'], 0, (Lexend, 48))
    left_btn_img = essentials.Selection_Bar((0, 0, 400, 75), ['Link Left Button'], 0, (Lexend, 48))
    right_btn_img = essentials.Selection_Bar((0, 0, 400, 75), ['Link Right Button'], 0, (Lexend, 48))
    up_btn_img = essentials.Selection_Bar((0, 0, 400, 75), ['Link Up Button'], 0, (Lexend, 48))
    
    button_down = essentials.Button(down_btn_img.image, blank, text=[2], rect=(350, -400, 400, 75), orig=(350, 200), groups=essentials.config)
    button_left = essentials.Button(left_btn_img.image, blank, text=[0], rect=(350, -300, 400, 75), orig=(350, 300), groups=essentials.config)
    button_right = essentials.Button(right_btn_img.image, blank, text=[1], rect=(350, -200, 400, 75), orig=(350, 400), groups=essentials.config)
    button_up = essentials.Button(up_btn_img.image, blank, text=[3], rect=(350, -100, 400, 75), orig=(350, 500), groups=essentials.config)
    
    moffset = essentials.Text_Selection((250, -300), (250, 300), list(map(lambda x: str(x) + 'ms', list(range(-30, 31)))) , "Music Offset", (Lexend, 48), arrow, essentials.audio)
    moffset.bar.limit = 1
    moffset.bar.selected = 29
    moffset.inc()

    rhythm = essentials.Text_Link("Inspired by Rhythm Doctor(7th Beat Games)", (Lexend, 48), 'https://store.steampowered.com/app/774181/Rhythm_Doctor/', (150, -550), (150, 50), essentials.credit)
    notice = essentials.Text_Link("you can click on these to check the linked websites", (Lexend, 24), 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', (150, -510), (150, 90), essentials.credit)
    bgm = essentials.Text_Link("background music: allo made it in like 5 hours i think", (Lexend, 36), '', (150, -450), (150, 150), essentials.credit)
    level1 = essentials.Text_Link("1st level: Rhythm Doctor 2-2 Supraventricular Tachycardia", (Lexend, 36), 'https://store.steampowered.com/app/774181/Rhythm_Doctor/', (150, -410), (150, 190), essentials.credit)
    level2 = essentials.Text_Link("2nd level: P4koo - 8th Planet [Re-Search]", (Lexend, 36), 'https://www.youtube.com/watch?v=q0v1IfRgcQM', (150, -370), (150, 230), essentials.credit)
    chaoz = essentials.Text_Link("3rd level: ParagonX9 - Chaoz Fantasy", (Lexend, 36), 'https://www.newgrounds.com/audio/listen/85046', (150, -330), (150, 270), essentials.credit)
    dseg = essentials.Text_Link("7-segment font provided by keshikan", (Lexend, 36), 'https://github.com/keshikan/DSEG/blob/master/DSEG-LICENSE.txt', (150, -290), (150, 310), essentials.credit)
    lexend = essentials.Text_Link("Lexend font provided by Google Fonts Team", (Lexend, 36), 'https://github.com/googlefonts/lexend/blob/main/OFL.txt', (150, -250), (150, 350), essentials.credit)
    lexend = essentials.Text_Link("Nexa Rust font provided by Svetoslav Simov/Fontfabric", (Lexend, 36), 'https://www.1001fonts.com/nexa-rust-font.html', (150, -210), (150, 390), essentials.credit)
    lexend = essentials.Text_Link("Dragon Ivan - Main Developer & Artist", (Lexend, 48), 'https://dragonivanrussia.itch.io/', (150, -150), (150, 450), essentials.credit)
    lexend = essentials.Text_Link("AlloRus162 - Developer & Music Producer", (Lexend, 48), '', (150, -100), (150, 500), essentials.credit)
    
    return locals()

