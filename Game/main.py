import pygame as pg
from Bird import Bird
from CONSTANTS import SCREEN_SIZE, BACKGROUND_IMAGE, BIRD_START, GEN_SIZE
from handlers import handle_visuals, handle_movement, handle_acceleration, handle_death, handle_pipes, handle_input, \
    handle_ai_input
from Pipe import Pipe
import random
from AI.NeuralNet import NeuralNet, mutate
import time
import numpy as np


def get_distx(bird, pipe):
    return pipe.x - bird.x


def get_disti(bird, pipe1, pipe2):
    x, y = SCREEN_SIZE

    y1 = x - pipe1.size * 50
    y2 = ((y-100) - (50 * pipe2.size))

    ideal_y = (y1 + y2) / 2

    return bird.y + 45 - ideal_y


def declare_initials(visuals, ai):
    # this function exists to massively reduce visual clutter

    if visuals:
        window = pg.display.set_mode(SCREEN_SIZE)
    else:
        window = None

    clock = pg.time.Clock()

    background_image = pg.image.load(BACKGROUND_IMAGE)
    bgx = 1

    if not ai:
        bird = Bird(*BIRD_START)
    else:
        bird = [Bird(*BIRD_START) for _ in range(GEN_SIZE)]

    pipes = []
    for i in range(3):
        weighted_nums = [1, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 6, 6]
        size = random.choice(weighted_nums)

        pipe1 = Pipe(False, size)
        pipe2 = Pipe(True, size + 1)

        pipe1.x += 250 * i
        pipe2.x += 250 * i

        pipes.append(pipe1)
        pipes.append(pipe2)

    tick = 0
    pipe1, pipe2 = pipes[:2]

    return window, clock, background_image, bgx, bird, pipes, tick, pipe1, pipe2


def game_loop(models, visuals=True, ai=False):

    pg.init()
    initial_values = declare_initials(visuals, ai)
    window, clock, background_image, bgx, bird, pipes, tick, pipe1, pipe2 = initial_values

    tick_map = dict()
    final_tick = -1

    while True:
        bgx -= 1
        dt = clock.tick(60)
        tick += dt

        if not ai:
            keys = pg.key.get_pressed()

        # required event loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return 0

        if visuals:
            if not ai:
                bird_visual = {'bird': (bird.current_sprite, (bird.x, bird.y))}
            else:
                bird_visual = {f'bird{i}': (b.current_sprite, (b.x, b.y)) for i, b in enumerate(bird)}

            handle_visuals(window, **{  # 'obj tag'      : (obj,                           (x, y))
                               'background_image': (background_image, (bgx % -490, 0)),
                               'second_bg_image': (background_image, (490 + bgx, 0)),
                               **bird_visual,
                               # this was the easiest way for me to make the code modular, essentially i am just saying
                               # what to draw and where on any given frame.
                               **{
                                   f'pipe_sprite{i}': (pipe.sprite, (pipe.x, pipe.y))
                                   for i, pipe in enumerate(pipes)
                               },

                           })

        if not ai:
            handle_acceleration(bird, dt)
            bird.jumping, bird.jump_start_tick = handle_input(bird, keys, tick)
            bird.jumping = handle_movement(bird, dt, tick)
        else:
            for model, b in zip(models, bird):
                handle_acceleration(b, dt)
                b.jumping, b.jump_start_tick = handle_ai_input(
                    b, model, [b.y + 45, get_disti(b, pipe1, pipe2), get_distx(b, pipe1), b.y+100, b.y-500], tick
                )
                b.jumping = handle_movement(b, dt, tick)

        if not ai:
            try:
                pipe1, pipe2 = handle_death(bird, pipes)
            except TypeError:
                bird.death = True

            if bird.death:
                final_tick = tick
                break
        else:
            for model, b in zip(models, bird):
                try:
                    pipe1, pipe2 = handle_death(b, pipes)
                except TypeError:
                    b.death = True

                if b.death:
                    tick_map[model] = tick
                    bird.remove(b)
                    models.remove(model)

            if not bird:
                break

        handle_pipes(pipes)

        if visuals:
            pg.display.update()

    if not ai:
        return final_tick

    return tick_map


def main(ai=False, visuals=True, preloaded_weights=None):

    if ai and not preloaded_weights:
        mrate = 0.9
        mrange = 0.25

        generation = [NeuralNet(5, 6, 1) for _ in range(GEN_SIZE)]

        tick_map = game_loop(generation, visuals, ai)

        fittest = max(tick_map, key=tick_map.get)
        longest_time = tick_map[fittest]
        while True:
            generation = [fittest]
            for _ in range(GEN_SIZE - 5):
                new_base_weights   = mutate(fittest.base_weights, mrate, mrange)
                new_base_biases    = mutate(fittest.base_biases, mrate, mrange*10)
                new_hidden_weights = mutate(fittest.hidden_weights, mrate, mrange)
                new_hidden_biases  = mutate(fittest.hidden_biases, mrate, mrange)

                new = NeuralNet(5, 6, 1, new_base_weights, new_base_biases, new_hidden_weights, new_hidden_biases)
                generation.append(new)

            for _ in range(4):
                generation.append(NeuralNet(5, 6, 1))

            start = time.perf_counter()
            tick_map = game_loop(generation, visuals, ai)

            if tick_map == 0:
                break

            end = time.perf_counter()

            fittest = max(tick_map, key=tick_map.get)

            if tick_map[fittest] > longest_time:
                longest_time = tick_map[fittest]

            mrate = (2 * max(0.0, 60 - (end-start)))/150 + 0.1
            mrate = max(0.1, mrate)

            mrange = (3 * max(0.0, 60 - (end-start)))/1200 + 0.1
            mrange = max(0.1, mrange)

            print(f'Time taken: {end-start}, Fittest tick duration: {longest_time}')
            print(f'\t\tMutation rate: {mrate}, Mutation range: {mrange}, Debug: {len(tick_map)}')

        print(fittest.base_weights)
        print(fittest.base_biases)
        print(fittest.hidden_weights)
        print(fittest.hidden_biases)

    elif ai:
        network = NeuralNet(3, 6, 1, *preloaded_weights)
        _ = game_loop([network], visuals, ai)

    else:
        game_loop(0, visuals, ai)


if __name__ == '__main__':
    main(True)

