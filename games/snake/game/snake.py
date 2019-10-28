import pygame

from mlgame.gamedev.generic import quit_or_esc, KeyCommandMap
from mlgame.gamedev.recorder import get_record_handler

from .gamecore import Scene, GameStatus
from .gameobject import SnakeAction
from ..main import get_log_dir

class Snake:
    def __init__(self, fps, one_shot_mode, record_progress):
        self._init_pygame()

        self._scene = Scene()

        self._fps = fps
        self._keyboard_action = KeyCommandMap({
            pygame.K_UP:    SnakeAction.UP,
            pygame.K_DOWN:  SnakeAction.DOWN,
            pygame.K_LEFT:  SnakeAction.LEFT,
            pygame.K_RIGHT: SnakeAction.RIGHT,
        }, SnakeAction.NONE)

        self._one_shot_mode = one_shot_mode
        self._record_handler = get_record_handler(record_progress, {
            "status": (GameStatus.GAME_OVER, )
        }, get_log_dir())

    def _init_pygame(self):
        pygame.display.init()
        pygame.display.set_caption("Snake")
        self._screen = pygame.display.set_mode( \
            (Scene.area_size.width, Scene.area_size.height + 25))

        self._clock = pygame.time.Clock()

        pygame.font.init()
        self._font = pygame.font.Font(None, 22)
        self._font_pos = (1, Scene.area_size.width + 5)

    def game_loop(self):
        while not quit_or_esc():
            command = self._keyboard_action.get_command()
            self._record_scene(command)

            game_status = self._scene.update(command)

            if game_status == GameStatus.GAME_OVER:
                self._record_scene(None)
                print("Score: {}".format(self._scene.score))

                if self._one_shot_mode:
                    return

                self._scene.reset()

            self._draw_scene()
            self._clock.tick(self._fps)

    def _draw_scene(self):
        self._screen.fill((50, 50, 50))
        self._screen.fill((0, 0, 0), Scene.area_size)
        self._scene.draw_gameobjects(self._screen)

        # Draw score
        font_surface = self._font.render( \
            "Score: {}".format(self._scene.score), True, (255, 255, 255))
        self._screen.blit(font_surface, self._font_pos)

        pygame.display.flip()

    def _record_scene(self, command):
        scene_info = self._scene.get_scene_info()
        scene_info.command = command
        self._record_handler(scene_info)
