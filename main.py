import os
import csv
import pygame
import essentials, menu, play
from foundation import *

def save():
    global data
    file = os.getenv('LOCALAPPDATA') + '\ReTransmitter\settings.csv'
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"')
        writer.writerow(data)
    load()

def keybind(screen, position):
    global data
    s = pygame.Surface((1000, 600))
    s.set_alpha(128)
    screen.blit(s, (0, 0))
    font = pygame.font.Font(None, 48)
    res = font.render("Enter your key", 1, (255, 255, 255))
    screen.blit(res, ((1000 - res.get_width()) / 2, 200))
    res = font.render(f"Current key:{pygame.key.name(data[4][position])}", 1, (255, 255, 255))
    screen.blit(res, ((1000 - res.get_width()) / 2, 300))
    count = 100
    delta = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exec_status = 'quit'
                menu.running = False
                break
            if event.type == pygame.KEYDOWN and delta != 1:
                buf = event
                delta = 1
                res = font.render(f"New key selected:{pygame.key.name(buf.key)}", 1, (255, 255, 255))
                screen.blit(res, ((1000 - res.get_width()) / 2, 400))
        count -= delta
        if count == 0:
            break
        clock.tick(60)
        pygame.display.flip()
    data[4][position] = buf.key
   
def load():
    global locked, quality, refresh, moffset, data, keybinds
    file = os.getenv('LOCALAPPDATA') + '\ReTransmitter\settings.csv'
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            data = row
            break
    quality.set(data[0])
    refresh.set(data[1])
    moffset.set(data[2])
    locked = data[3][1:-1].split(', ')
    for index, elem in enumerate(locked):
        if elem == 'True':
            locked[index] = True
        else:
            locked[index] = False
    data[4] = data[4][1:-1].split(', ')
    for i in range(0, 4):
        data[4][i] = int(data[4][i])
    keybinds = data[4]
    data = [*data[:3], locked, keybinds]
            

if __name__ == '__main__':
    pygame.mixer.pre_init()
    pygame.init()
    pygame.display.set_caption('ReTransmitter')
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    effects = pygame.Surface(size)
    original = pygame.Surface(size)
    running = True
    clock = pygame.time.Clock()

    level = 2
    exec_status = "menu"
    alpha = 30
    
    globals().update(menu.init())

    button_down.action = keybind
    button_down.args = [screen, 2]
    button_left.action = keybind
    button_left.args = [screen, 0]
    button_right.action = keybind
    button_right.args = [screen, 1]
    button_up.action = keybind
    button_up.args = [screen, 3]

    
    fade = essentials.Image(load_image("end_screen.png"), pos=(0, 0), orig=(0, 0))
    fade.image.fill((0, 0, 0))
    fade.image.set_alpha(0)
    
    while True:
        if exec_status == "menu":
            try:
                os.mkdir(os.getenv('LOCALAPPDATA') + '\ReTransmitter')
                data = ['Medium', '60', '0ms', [True, False, False, False], [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]]
                save()
            except Exception:
                load()

            tutorial.locked = not locked[0]
            forest.locked = not locked[1]
            highway.locked = not locked[2]
            city.locked = not locked[3]
            
            menu.running = True
            alpha = 30
            menu.counter_play = False

            for i in range(0, 3):
                if locked[i] == False:
                    break
                unlocked = i
            
            while menu.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        menu.running = False
                        menu.exec_status = "quit"
                
                original.fill(BG())
                original.blit(essentials.bg, (ticks % 100 - 100, ticks % 80 - 80))

                if menu.pulse:

                    print('saved')
                    save()
                    menu.pulse = False

                if menu.misc:
                    essentials.misc.update(event)
                    essentials.misc.draw(original)
                
                if menu.status == "Settings" or menu.status == "Transition":
                    essentials.settings.update(event)
                    if essentials.offset != cur_offset:
                        transition = 0
                        cur_offset = essentials.offset
                        set_offset = offset
                    if transition < 50:
                        transition += 1
                        offset = MoveDelta((0, set_offset), (0, cur_offset), 'out_quad', transition, 50)[1]
                    for sprite in image_list:
                        buf = sprite.rect
                        sprite.rect = (buf[0], sprite.pos[1] + offset, *buf[2:])
                    essentials.settings.draw(original)
                    
                if menu.status == "Menu" or menu.status == "Transition":
                    essentials.levels.update(event)
                    essentials.levels.draw(original)
                    essentials.main.update(event)
                    essentials.main.draw(original)

                if menu.active is not None:
                    menu.active.update(event)
                    menu.active.draw(original)
                
                essentials.buttons.update(event)
                essentials.buttons.draw(original)
                
                if menu.cooldown == 0:
                    if menu.last == "Menu":
                        menu.status = "Settings"
                    elif menu.last == "Settings":
                        menu.status = "Menu"

                menu.cooldown -= 1
                menu.cooldown2 -= 1
                ticks += 1
                clock.tick(60)

                screen.blit(original, (0, 0))
                if alpha > 0 and not menu.counter_play:
                    alpha -= 1
                    effects.set_alpha(alpha * 8.5)
                    screen.blit(effects, (0,0))
                
                if menu.counter_play:
                    alpha += 1
                    effects.set_alpha(alpha * 8.5)
                    screen.blit(effects, (0,0))
                    if alpha * 8.5 == 255:
                        menu.running = False
                
                pygame.display.flip()
                
            exec_status = menu.exec_status
            if exec_status == "play":
                level = menu.level
        if exec_status == "quit":
            break
        if exec_status == "play":
            play.level = level
            pygame.mixer.init()
            globals().update(play.init(level))
            play.running = True
            play.end_screen = False
            noise.counter, anim_counter = 0, 0
            audio_output = play.generate(level)
            bpm = play.bpm
            starting_point = pygame.time.get_ticks()
            play.keybinds = keybinds
            play.quit = 0
            level_events, bpm_events = [], []
            for i in level_data:
                i = str(int(i[0]) + starting_point - 200), *i[1:]
                if i[1] == 'change_bpm':
                    bpm_events.append(i)
                else:
                    level_events.append(i)
            play.starting_point = starting_point
            shown = False
            play.accuracy = 100
            pygame.mixer.music.load(play.music_name)
            pygame.mixer.music.play(1, start=0)
            while play.running:
                if (pygame.time.get_ticks() - starting_point) % 1200 <= 50:
                    screen.blit(load_image(f'level-{level}\\side_{((pygame.time.get_ticks() - starting_point) // 1200) % 2}.png'), (0, 0))
                cooldown = play.cooldown
                play.cooldown -= 1
                car_view.update_frame()
                distance_to_wave = abs(player.rect.x - 15 - wave.rect.x)
                play.distance = player.rect.x
                cooldown -= 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exec_status = 'quit'
                        play.running = False
                        play.quit = 1
                    if event.type == pygame.KEYDOWN:
                        i = pygame.key.get_pressed()
                        player.update(i)
                        if i[play.keybinds[3]] and noise.alpha == 90:
                            button.image = closed
                            up_hit = pygame.time.get_ticks()
                            noise_reduction = 1
                    all_sprite.update(event)

                if noise_reduction:
                    noise.disappear()
                    if noise.alpha == 70:
                        button.image = opened
                    if noise.alpha == 20:
                        noise_reduction = 0

                if cooldown < 0:
                    if distance_to_wave > 45:
                        acc = 0
                    if 10 < distance_to_wave < 45:
                        acc = 0.5
                if distance_to_wave < 10:
                    acc = 1

                if bpm_events:
                    time_until_event = int(bpm_events[0][0]) - pygame.time.get_ticks()
                    if time_until_event < 0:
                        bpm = int(bpm_events[0][2])
                        del bpm_events[0]
                
                if level_events:
                    time_until_event = int(level_events[0][0]) - pygame.time.get_ticks()
                    if time_until_event < 0:
                        wave.event_move(level_events[0][1])
                        if level_events[0][1] == "thunder":
                            noise.noise()
                        elif level_events[0][1] == "end":
                            end_screen = 1
                            play.running = False
                        else:
                            car_view.change_frame_list(f"level-{level}\\stable", 2)
                            process_cd = 1
                        if len(level_events) > 1 and abs(int(level_events[0][0]) - int(level_events[1][0])) < 242000 / bpm:
                            radio_signal.quick = 1
                        else:
                            radio_signal.quick = 0
                        radio_signal.blink()
                        level_events.pop(0)
                        shown = False

                if level_events and level_events[0][1] != "thunder" and level_events[0][1] != "end":
                    tick = 30000 if radio_signal.quick else 60000
                    if 4 * tick / bpm - 20 < time_until_event < 4 * tick / bpm + 20:
                        stable = 1
                        event = 0
                        process_cd = 9999
                        radio_signal.blink()
                        shown = play.action(car_view, level, level_events[0], shown)
                    elif 3 * tick / bpm - 20 < time_until_event < 3 * tick / bpm + 20:
                        radio_signal.blink()
                        shown = play.action(car_view, level, level_events[0], shown)
                    elif 2 * tick / bpm - 20 < time_until_event < 2 * tick / bpm + 20:
                        radio_signal.blink()
                        shown = play.action(car_view, level, level_events[0], shown)
                    elif tick / bpm - 20 < time_until_event < tick / bpm + 20:
                        radio_signal.blink()
                        shown = play.action(car_view, level, level_events[0], shown)

                radio_signal.blink_fade()

                wave.image = audio_output[(pygame.time.get_ticks() - starting_point) // 100]
                waves.update(event)
                all_sprite.draw(screen)
                screen.blit(status.image, status.rect[:2])

                acc_ticks += acc
                total_ticks += 1
                if process_cd < 0:
                    process_cd = 0
                else:
                    process_cd -= 1
                clock.tick(fps)
                # screen.blit(dialogue.rendered_text[0], dialogue.rendered_text[1])
                pygame.display.flip()
                    
                accuracy = acc_ticks / total_ticks * 100
                play.accuracy = accuracy
                if total_ticks % 100 == 50:
                    print(clock.get_fps())
                if end_screen:
                    quit = 0
                    running = 0
            
            accuracy = acc_ticks / total_ticks * 100
            end_overlay = essentials.Image(load_image("end_screen.png"), (0, 0), (0, 0), end_sprite)
            alpha_end = 0
            end_font = pygame.font.Font(None, 50)

            rank_font = pygame.font.Font(None, 300)
            rank = "C", "mediumpurple"
            if accuracy >= 98:
                rank = "A+", "lightcoral"
            elif 95 <= accuracy < 98:
                rank = "A", "orange"
            elif 90 < accuracy < 95:
                rank = "B", "aquamarine"

            clear = end_font.render("Level clear!", 1, (255, 255, 255))
            acc_text = end_font.render(f"Accuracy:{round(accuracy, 2)}%", 1, (255, 255, 255))
            rank_text = rank_font.render(rank[0], 1, rank[1])

            end_sprite.draw(screen)
            intro_rect = clear.get_rect()
            intro_rect.move_ip(50, 50)
            screen.blit(clear, intro_rect)

            intro_rect = acc_text.get_rect()
            intro_rect.move_ip(50, 100)
            screen.blit(acc_text, intro_rect)

            intro_rect = rank_text.get_rect()
            intro_rect.move_ip(25, 150)
            screen.blit(rank_text, intro_rect)
            running = 1

            play.load_table(screen, player_pos_record, wave_pos_record)
            count_exp = 0
            running_exp = True
            while running_exp and not play.quit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or play.quit:
                        exec_status = 'quit'
                    if count_exp >= 360 and pygame.MOUSEBUTTONDOWN:
                        exec_status = "menu"
                        running_exp = False
                count_exp += 1
                clock.tick(60)
                pygame.display.flip()
            if accuracy > 90 and end_screen and level == unlocked:
                unlocked += 1
                if unlocked > 3:
                    unlocked = 3
                locked[unlocked] = True
                save()
            pygame.mixer.quit()
    pygame.quit()
