import pygame

clock = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode((618, 359))
pygame.display.set_caption("Игра платформер")
icon = pygame.image.load("images/icon.png").convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load("images/bg.png").convert_alpha()

walk_left = [
    pygame.image.load("images/player_left/1.png").convert_alpha(),
    pygame.image.load("images/player_left/2.png").convert_alpha(),
    pygame.image.load("images/player_left/3.png").convert_alpha(),
    pygame.image.load("images/player_left/4.png").convert_alpha(),
]
walk_right = [
    pygame.image.load("images/player_right/1.png").convert_alpha(),
    pygame.image.load("images/player_right/2.png").convert_alpha(),
    pygame.image.load("images/player_right/3.png").convert_alpha(),
    pygame.image.load("images/player_right/4.png").convert_alpha(),
]

monstr = pygame.image.load("images/monstr.png").convert_alpha()

monstr_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 8
player_x = 150
player_y = 250

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound('sounds/bgs.mp3')
bg_sound.play()

monstr_timer = pygame.USEREVENT + 1
pygame.time.set_timer(monstr_timer, 2500)

label = pygame.font.Font('fonts/RobotoMono-LightItalic.ttf', 40)
small_label = pygame.font.Font('fonts/RobotoMono-LightItalic.ttf', 20)

lose_label = label.render("Вы проиграли!", False, (193, 196, 199))
restart_label = label.render("Начать сначала", False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(180, 200))
bullet = pygame.image.load('images/bull.png').convert_alpha()
bullets = []
bullets_left = 5

score = 0
bullet_count = 20

gameplay = True

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 618, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
        if monstr_list_in_game:
            for (i, el) in enumerate(monstr_list_in_game):
                screen.blit(monstr, el)
                el.x -= 10

                if el.x < -10:
                    monstr_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False
                else:
                    if player_rect.colliderect(el) or player_rect.colliderect(el.move(0, 30)):
                        monstr_list_in_game.pop(i)
                        score += 30  # Увеличение счета на 30 за убийство монстра
                    elif player_rect.colliderect(el.move(0, -30)):
                        score += 20  # Увеличение счета на 20 за перепрыгивание монстра

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1

            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x <= -618:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 630:
                    bullets.pop(i)

                if monstr_list_in_game:
                    for (index, monstr_el) in enumerate(monstr_list_in_game):
                        if el.colliderect(monstr_el):
                            monstr_list_in_game.pop(index)
                            bullets.pop(i)
                            score += 30  # Увеличение счета на 30 за убийство монстра

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)

        bullets.clear()
        bullet_count = 0
        score = 0

        bg_sound.stop()

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            monstr_list_in_game.clear()
            bullets.clear()
            bullets_left = 5
            bullet_count = 5
            score = 0
            bg_sound.play()

    # Отображение счетчика патронов
    if gameplay:
        bullet_label = small_label.render("Патроны: " + str(bullet_count), True, (255, 255, 255))
        screen.blit(bullet_label, (10, 10))

    # Отображение счета очков
    if gameplay:
        score_label = small_label.render("Счет: " + str(score), True, (255, 255, 255))
        screen.blit(score_label, (10, 30))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == monstr_timer:
            monstr_list_in_game.append(monstr.get_rect(topleft=(620, 250)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1
            bullet_count -= 1

    clock.tick(15)
