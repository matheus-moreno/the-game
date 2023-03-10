import pygame

from .functions import (
    checkInitialEvents,
    updateInitialScreen,
    checkOptionsEvents,
    updateOptionsScreen,
    checkShipsEvents,
    updateShipsScreen,
    checkLevelEvents,
    updateLevelScreen,
    checkControlsEvents,
    updateControlsScreen,
    updateCountScreen,
    checkLeadEvents,
    updateLeadScreen,
    updateEnd,
    gameOver,
)

from .settings import Settings
from .canvas import Background, Initial, Options, Ships, Level, Controls, Count, End
from .ship import Ship
from .enemies import Pawn, Knight, Bishop
from .utils import wait

from random import randint


def run():
    """run game"""

    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode((settings.width, settings.height))

    pygame.display.set_caption(settings.display)

    background = Background(screen)
    initial = Initial(screen)
    options = Options(screen)
    ships = Ships(screen)
    level = Level(screen)
    controls = Controls(screen)
    end = End(screen)

    while True:
        settings.back = [230, 230, 230]
        background.on = True

        # Start Screen
        while True:
            checkInitialEvents(initial, background)
            updateInitialScreen(settings, screen, background, initial)

            if initial.value == 0:
                break
            elif initial.value == 1:
                # Options Screen
                while True:
                    checkOptionsEvents(options, background)
                    updateOptionsScreen(settings, screen, background, options)

                    if options.value == 0:
                        options.state = 0
                        options.value = -1

                        # Ship Choose
                        while True:
                            checkShipsEvents(ships, background)
                            updateShipsScreen(settings, screen, background, ships)

                            if ships.back:
                                ships.back = False
                                break

                            wait(settings.delay)

                    elif options.value == 1:
                        options.state = 0
                        options.value = -1

                        # Level Choose
                        while True:
                            checkLevelEvents(level, background)
                            updateLevelScreen(settings, screen, background, level)

                            if level.back:
                                level.back = False
                                break

                            wait(settings.delay)

                    elif options.value == 2:
                        options.state = 0
                        options.value = -1

                        # Controls Visualizer
                        while True:
                            checkControlsEvents(controls, background)
                            updateControlsScreen(settings, screen, background, controls)

                            if controls.back:
                                controls.back = False
                                break

                            wait(settings.delay)

                    elif options.value == 3:
                        options.state = 0
                        options.value = -1

                        initial.state = 0
                        initial.value = -1
                        break

                    wait(settings.delay)
                wait(settings.delay)
            wait(settings.delay)

        ship = Ship(
            screen,
            ships.color,
            settings.amounts[level.value()]["ship"]["velocity"],
            settings.amounts[level.value()]["ship"]["life"],
        )

        pawns = [
            Pawn(
                screen,
                randint(0, 2),
                randint(400, 800),
                settings.amounts[level.value()]["pawns"]["velocity"],
                settings.amounts[level.value()]["pawns"]["life"],
            )
            for _ in range(0, settings.amounts[level.value()]["pawns"]["amount"])
        ]
        knights = [
            Knight(
                screen,
                randint(0, 3),
                randint(200, 1000),
                settings.amounts[level.value()]["knights"]["velocity"],
                settings.amounts[level.value()]["knights"]["life"],
            )
            for _ in range(0, settings.amounts[level.value()]["knights"]["amount"])
        ]
        bishops = [
            Bishop(
                screen,
                randint(0, 3),
                randint(100, 1100),
                settings.amounts[level.value()]["bishops"]["velocity"],
                settings.amounts[level.value()]["bishops"]["life"],
            )
            for _ in range(0, settings.amounts[level.value()]["bishops"]["amount"])
        ]

        rate = settings.amounts[level.value()]["back"]["rate"]

        enemies = pawns + knights + bishops
        defeat = False

        count = Count(screen)

        # Count
        for number in range(1, 4):
            for _ in range(0, 20):
                updateCountScreen(settings, screen, background, count, number)

                wait(settings.delay)

        # Game
        for enemy in enemies:
            steps = 0

            while True:
                if steps % rate == 0 and background.on:
                    if settings.back[0] >= 1:
                        settings.back[0] -= 1
                        settings.back[1] -= 1
                        settings.back[2] -= 1

                checkLeadEvents(ship, background)

                ship.update()
                enemy.move()
                ship.bullet.update(ship.rect.centerx, ship.rect.bottom, ship.velocity)

                updateLeadScreen(settings, screen, background, ship, enemy)

                enemy.colision(ship)

                if enemy.invade():
                    ship.hit()

                    if ship.life == 0:
                        defeat = True

                    break

                if enemy.death():
                    break

                steps += 1

                wait(settings.step)

            if gameOver(defeat):
                break

        for _ in range(0, 40):
            updateEnd(settings, screen, background, end, defeat)

            wait(settings.delay)

        initial.value = -1
