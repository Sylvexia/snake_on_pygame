import pygame
import pygame_gui
from snake import snake_game
from option import option_gui

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.RESIZABLE, 32)
pygame.display.set_caption("Snake Game")

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

gui_manager = pygame_gui.UIManager((screen_width, screen_height), "theme.json")
container = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (screen_width, screen_height)),
                                        )

label_game_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(150, 100 ,500, 100),
                                               text="Snakers",
                                               manager=gui_manager,
                                               container=container,
                                               anchors={'left': 'left',
                                                        'right': 'right',
                                                        'top': 'top',
                                                        'bottom': 'bottom'}
                                               )

button_new_game = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 250), (100, 30)),
                                               text="New Game",
                                               manager=gui_manager,
                                               container=container,
                                               anchors={'left': 'left',
                                                        'right': 'right',
                                                        'top': 'top',
                                                        'bottom': 'bottom'}
                                               )

button_options = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 300), (100, 30)),
                                              text="Options",
                                              manager=gui_manager,
                                              container=container,
                                              anchors={'left': 'left',
                                                       'right': 'right',
                                                       'top': 'top',
                                                       'bottom': 'bottom'}
                                              )

button_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 350), (100, 30)),
                                           text="Quit",
                                           manager=gui_manager,
                                           container=container,
                                           anchors={'left': 'left',
                                                    'right': 'right',
                                                    'top': 'top',
                                                    'bottom': 'bottom'}
                                           )

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        gui_manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button_new_game:
                snake_game(screen)
            elif event.ui_element == button_options:
                option_gui(screen)
            elif event.ui_element == button_quit:
                is_running = False

    gui_manager.update(pygame.time.Clock().tick(60) / 1000.0)

    screen.fill((0, 0, 0))

    gui_manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
