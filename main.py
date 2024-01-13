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
        
def load():
    global locked, quality, refresh, moffset, data
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

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('ReTransmitter')
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    effects = pygame.Surface(size)
    original = pygame.Surface(size)
    running = True
    clock = pygame.time.Clock()

    level = -1
    exec_status = "menu"
    alpha = 30
    
    globals().update(menu.init())

    globals().update(play.init())
    while True:
        if exec_status == "menu":
            try:
                os.mkdir(os.getenv('LOCALAPPDATA') + '\ReTransmitter')
                data = ['Medium', '60', '0ms', [True, False, False, False]]
                save()
            except Exception:
                pass
            finally:
                load()

            tutorial.locked = not locked[0]
            forest.locked = not locked[1]
            highway.locked = not locked[2]
            city.locked = not locked[3]
            
            menu.running = True
            alpha = 30
            
            print('level', level)
            
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
                if alpha > 0:
                    alpha -= 1
                    effects.set_alpha(alpha * 8.5)
                    screen.blit(effects, (0,0))
                
                pygame.display.flip()
            exec_status = menu.exec_status
            if exec_status == "play":
                level = menu.level
        if exec_status == "quit":
            break
        if exec_status == "play":
            starting_point = pygame.time.get_ticks()
            play.starting_point = starting_point
            play.running = True
            play.end_screen = False
            noise.counter = 0
            while play.running:
                if level_events:
                    time_until_event = (int(level_events[0][0]) - pygame.time.get_ticks() + starting_point)
                distance_to_wave = abs(player.rect.x - wave.rect.x)
                cooldown -= 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        i = pygame.key.get_pressed()
                        if i[pygame.K_UP] and noise.alpha == 255:
                            up_hit = pygame.time.get_ticks() + starting_point
                            noise_reduction = 1
                    all_sprite.update(event)

                if noise_reduction:
                    noise.disappear()
                    if noise.alpha == 0:
                        noise_rduction = 0

                if cooldown < 0:
                    if 25 < distance_to_wave < 50:
                        acc = 0.5
                    elif distance_to_wave >= 50:
                        acc = 0
                    elif distance_to_wave < 26:
                        acc = 1

                if level_events:
                    if time_until_event < 0:
                        wave.event_move(level_events[0][1])
                        if level_events[0][1] == "thunder":
                            noise.noise()
                        elif level_events[0][1] == "end":
                            end_screen = 1
                        else:
                            process_cd = 90
                            template.image = load_image(level_events[0][1] + "_process.png")
                            radio_signal.blink()
                        level_events.pop(0)

                if level_events and level_events[0][1] != "thunder" and level_events[0][1] != "end":
                    if 240000 / bpm - 15 < time_until_event < 240000 / bpm + 15:
                        template.image = load_image(level_events[0][1] + ".png")
                        process_cd = 9999
                        radio_signal.blink()
                    if 180000 / bpm - 15 < time_until_event < 180000 / bpm + 15:
                        radio_signal.blink()
                    if 120000 / bpm - 15 < time_until_event < 120000 / bpm + 15:
                        radio_signal.blink()
                    if 60000 / bpm - 15 < time_until_event < 60000 / bpm + 15:
                        radio_signal.blink()

                radio_signal.blink_fade()

                all_sprite.draw(screen)

                acc_ticks += acc
                total_ticks += 1
                if process_cd < 0:
                    process_cd = 0
                    template.image = load_image("stable.png")
                else:
                    process_cd -= 1
                clock.tick(fps)
                pygame.display.flip()

                if end_screen:
                    play.running = False

            accuracy = acc_ticks / total_ticks * 100
            end_overlay = essentials.Image(load_image("end_screen.png"), (0, 0), (0, 0), end_sprite)
            alpha_end = 0
            end_font = pygame.font.Font(None, 50)

            rank_font = pygame.font.Font("fonts/MS PGothic.ttf", 300)
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
            while running_exp:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                count_exp += 1
                if count_exp >= 360:
                    running_exp = False
                clock.tick(60)
                pygame.display.flip()
            globals().update(play.init())
            exec_status = "menu"
    pygame.quit()
