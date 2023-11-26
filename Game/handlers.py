import pygame as pg
from CONSTANTS import GRAVITY, CLAMPED_ACCELERATION, JUMP_ACCELERATION, BIRD_WIDTH, JUMP_DURATION, JUMP_COOLDOWN, \
    SPEED_MULTIPLIER
import random
from Pipe import Pipe


def handle_visuals(window, **visuals):
    for visual in visuals:
        obj, coord = visuals[visual]
        window.blit(obj, coord)


def handle_events(bird):
    if bird.y > 500:
        bird.death = True


def handle_movement(entity, dt, tick):
    vx, vy = entity.momentum  # represents distance it should move in one second
    entity.x, entity.y = entity.x + (vx * (dt / (1000 / SPEED_MULTIPLIER))), \
        entity.y + (vy * (dt / (1000 / SPEED_MULTIPLIER)))

    if tick - entity.jump_start_tick > JUMP_DURATION:
        entity.jumping = False

    if not entity.can_jump and tick - entity.jump_start_tick >= JUMP_COOLDOWN:
        entity.can_jump = True

    return entity.jumping


def handle_acceleration(bird, dt):
    if bird.jumping:
        bird.momentum = JUMP_ACCELERATION * dt / (1000 / SPEED_MULTIPLIER)
    bird.momentum = min(bird.momentum + (GRAVITY * dt / (1000 / SPEED_MULTIPLIER)), CLAMPED_ACCELERATION)


def handle_death(bird, pipes):
    if bird.y > 500 or bird.y < -100:
        bird.death = True
        return

    for idx, pipe in enumerate(pipes):
        if pipe.x + 75 > bird.x + BIRD_WIDTH:
            pair = (pipe, pipes[idx + 1])
            break

    pipe1, pipe2 = pair
    # pipe2 : 0, 400 - (50 * pipe2.size)
    # pipe1 : 500, pipe1.size * 50
    # width = 75
    birdx = bird.x + 50
    birdy = bird.y + 45

    if birdx + BIRD_WIDTH >= pipe1.x - 1:
        bird.death = (-1000 <= birdy <= (400 - (50 * pipe2.size))) or (birdy > 500 - pipe1.size * 50)

    return pipe1, pipe2


def handle_pipes(pipes):
    for pipe in pipes:
        pipe.x -= 1

    for pipe in pipes:
        if pipe.x < -90:
            pipes.remove(pipe)
            weighted_nums = [1, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 6, 6]
            size = random.choice(weighted_nums)

            pipe1 = Pipe(False, size)
            pipe2 = Pipe(True, size + 1)

            pipe1.x = pipes[-2].x + 250
            pipe2.x = pipes[-1].x + 250

            pipes.append(pipe1)
            pipes.append(pipe2)


def handle_input(bird, keys, tick):
    if keys[pg.K_SPACE] and bird.can_jump:
        bird.can_jump = False
        bird.jumping = True
        bird.jump_start_tick = tick

    return bird.jumping, bird.jump_start_tick


def handle_ai_input(bird, network, inp, tick):
    prob = network(inp)
    if prob > 0.5 and bird.can_jump:
        bird.can_jump = False
        bird.jumping = True
        bird.jump_start_tick = tick

    return bird.jumping, bird.jump_start_tick
