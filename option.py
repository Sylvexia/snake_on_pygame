import pygame
import pygame_gui


def option_gui(screen):
    gui_manager = pygame_gui.UIManager(
        (screen.get_width(), screen.get_height()))

    volume_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 200), (100, 30)),
                                               text="Volume",
                                               manager=gui_manager)

    volume_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((300, 250), (200, 30)),
                                                           start_value=1.0,
                                                           value_range=(
                                                               0.0, 1.0),
                                                           manager=gui_manager,)
    
    return_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                                    text="Return",
                                                    manager=gui_manager)
    
    is_running = True

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            gui_manager.process_events(event)

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == volume_slider:
                    volume = event.value
                    pygame.mixer.music.set_volume(volume)
                elif event.ui_element == return_button:
                    print("invoked")
                    return

        gui_manager.update(pygame.time.Clock().tick(60) / 1000.0)

        screen.fill((0, 0, 0))

        gui_manager.draw_ui(screen)

        pygame.display.flip()
