#!/usr/bin/env python
# Example file showing a circle moving on screen
import pygame
import numpy as np

# pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

font = pygame.font.Font(pygame.font.get_default_font(), 36)

# now print the text
intro = True
while intro:
    print(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            super_running = False
            intro = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        print(False)
        intro = False
    text_surface = font.render('Asteroids', True, (255, 255, 255))
    screen.blit(text_surface, dest=(screen.get_width() / 2, screen.get_height() / 2))
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
print(2)



def dist(a, b):
    return np.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

super_running = True

while super_running:
    running = True
    dt = 0
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    end_pos = pygame.Vector2(screen.get_width() / 2 + 200, screen.get_height() / 2 + 200)
    player_vel = pygame.Vector2(0, 0)
    dragging = False
    rotation = 0
    speed = 0
    shoot = False
    shoot_timer = 0
    bullets = []
    asteroids = []
    new_ring = False
    ring_timer = -1
    lightning_timer = -1
    while len(asteroids) < 10:
        asteroid = [
            pygame.Vector2(np.random.random() * screen.get_width(), np.random.random() * screen.get_height()),
            pygame.Vector2(np.random.random(), np.random.random()),
            (1.2 + np.random.random()) * 20,
        ]
        if dist(asteroid[0], player_pos) > 100:
            asteroids.append(asteroid)

    powerups = []
    while running and asteroids:
        if np.random.random() > 0.995:
            powerups.append({
                'pos': pygame.Vector2(np.random.random() * screen.get_width(), np.random.random() * screen.get_height()),
                'age': 0,
                })

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                super_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                pos = pygame.mouse.get_pos()
                player_pos.x = pos[0]
                player_pos.y = pos[1]
            if event.type == pygame.MOUSEMOTION and dragging:
                pos = pygame.mouse.get_pos()
                player_pos.x = pos[0]
                player_pos.y = pos[1]
            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                pos = pygame.mouse.get_pos()
                player_pos.x = pos[0]
                player_pos.y = pos[1]
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        points = [
            (player_pos.x - 10, player_pos.y + 10),
            (player_pos.x - 10, player_pos.y - 10),
            (player_pos.x + 20, player_pos.y),
        ]
        rot_points = [
            (pygame.math.Vector2(x, y) - player_pos).rotate(-rotation) + player_pos for x, y in points
        ]
        pygame.draw.polygon(screen, "green", rot_points, 5)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_vel.x += 5 * dt * np.cos(rotation * np.pi / 180)
            player_vel.y -= 5 * dt * np.sin(rotation * np.pi / 180)
        if keys[pygame.K_DOWN]:
            player_vel.x -= 5 * dt * np.cos(rotation * np.pi / 180)
            player_vel.y += 5 * dt * np.sin(rotation * np.pi / 180)
        if keys[pygame.K_LEFT]:
            rotation += 180 * dt
        if keys[pygame.K_RIGHT]:
            rotation -= 180 * dt
        if keys[pygame.K_ESCAPE]:
            running = False
            super_running = False
        if keys[pygame.K_SPACE]:
            if shoot_timer < 0:
                shoot = True
        if keys[pygame.K_b]:
            if ring_timer < 0:
                new_ring = True
                ring_timer = 75
        if keys[pygame.K_l]:
            if lightning_timer < -100:
                lightning_timer = 20
        hit_asteroids = []
        ring_timer -= 1
        if new_ring:
            # ring_timer = 1
            ring_radius = 30 + 75 * (75 - ring_timer) * dt
            ring_timer -= 1
            pygame.draw.circle(screen, 'green', player_pos, ring_radius, width=2)
            if ring_timer < 0:
                ring_timer = 75
                new_ring = False
            for asteroid in asteroids:
                if dist(player_pos, asteroid[0]) < ring_radius + asteroid[2]:
                    hit_asteroids.append(asteroid)

        if lightning_timer == 20:
            nearest_asteroids = []
            while len(nearest_asteroids) < 4:
                mdist = 1e9
                for asteroid in asteroids:
                    if nearest_asteroids:
                        last_pos = nearest_asteroids[-1][0]
                    else:
                        last_pos = player_pos
                    adist = dist(last_pos, asteroid[0])
                    if adist < mdist:
                        if asteroid not in nearest_asteroids:
                            mdist = adist
                            nasteroid = asteroid
                nearest_asteroids.append(nasteroid)
                hit_asteroids.append(nasteroid)
            lightning_points = [player_pos] + [
                a[0] for a in nearest_asteroids
            ]
        if lightning_timer > 0:
            pygame.draw.lines(screen, 'yellow', False, lightning_points, 3)
            lightning_points = [player_pos] + [
                p + pygame.Vector2((np.random.random() - 0.5) * 10, (np.random.random() - 0.5) * 10)
                for p in lightning_points[1:]
            ]
        lightning_timer -= 1

        if shoot:
            bullet = [
                pygame.math.Vector2(player_pos.x, player_pos.y),
                pygame.math.Vector2(player_vel.x, player_vel.y),
                rotation,
                0
                ]
            bullets.append(bullet)
            shoot = False
            shoot_timer = 1
        shoot_timer -= 1
        for bullet in bullets:
            bullet[0].x += 525 * dt * np.cos(bullet[2] * np.pi / 180) + bullet[1].x
            bullet[0].y -= 525 * dt * np.sin(bullet[2] * np.pi / 180) - bullet[1].y
            bullet[3] += 1
            pygame.draw.circle(screen, "green", bullet[0], 2)
            for asteroid in asteroids:
                if dist(bullet[0], asteroid[0]) < (asteroid[2] + 5):
                    hit_asteroids.append(asteroid)

        for hit_asteroid in hit_asteroids:
            if hit_asteroid in asteroids:
                asteroids.remove(hit_asteroid)
                radius = hit_asteroid[2]
                if radius > 15:
                    rand_vel = pygame.Vector2(np.random.random(), np.random.random()) + hit_asteroid[1]
                    asteroids.append([
                        pygame.Vector2(hit_asteroid[0]),
                        rand_vel,
                        radius / 2,
                    ])
                    asteroids.append([
                        pygame.Vector2(hit_asteroid[0]),
                        -rand_vel,
                        radius / 2,
                    ])

        for asteroid in asteroids:
            if dist(asteroid[0], player_pos) < max(asteroid[2], 20):
                running = False
            asteroid[0].x += asteroid[1].x
            asteroid[0].y += asteroid[1].y
            pygame.draw.circle(screen, "white", asteroid[0], asteroid[2])
            if asteroid[0].x > screen.get_width():
                asteroid[0].x -= screen.get_width()
            if asteroid[0].y > screen.get_height():
                asteroid[0].y -= screen.get_height()
            if asteroid[0].x < 0:
                asteroid[0].x += screen.get_width()
            if asteroid[0].y < 0:
                asteroid[0].y += screen.get_height()

        powerups_to_remove = []
        for powerup in powerups:
            if dist(powerup['pos'], player_pos) < max(20, 20):
                powerups_to_remove.append(powerup)
            if powerup['age'] > 500:
                powerups_to_remove.append(powerup)
            else:
                pygame.draw.circle(screen, 'blue', powerup['pos'], 20, width=2)
                powerup['age'] += 1

        for powerup in powerups_to_remove:
            powerups.remove(powerup)


        bullets = [b for b in bullets if b[3] < 10000 * dt]

        player_pos.x += player_vel.x
        player_pos.y += player_vel.y

        if player_pos.x > screen.get_width():
            player_pos.x -= screen.get_width()
        if player_pos.y > screen.get_height():
            player_pos.y -= screen.get_height()
        if player_pos.x < 0:
            player_pos.x += screen.get_width()
        if player_pos.y < 0:
            player_pos.y += screen.get_height()

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
pygame.quit()
