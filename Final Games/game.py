import pygame
from pygame.locals import *

from Engine.scenenode import *
from Engine.texturemanager import *
from Engine.inputmanager import *
from Engine.object import *
from player import *


class Game:
    def __init__(self):
        self.screen_width = 640
        self.screen_height = 480
        self.running = True
        self.lastTime = pygame.time.get_ticks()/1000.0
        self.animation_fps = 4

    # Updates time
    def updateTime(self):
        self.lastTime = pygame.time.get_ticks()/1000.0


    def setup(self):
        size = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(size)

        # Loading Textures
        TextureManager.load_texture('steve', 'textures/steve.gif')
        TextureManager.load_texture('player_idle_right', 'textures/character.png', (32, 32), (0,32), 13)
        TextureManager.load_texture('player_idle_left', 'textures/character.png', (32, 32), (0,256), 13)

        TextureManager.load_texture('player_walk_right', 'textures/character.png', (16, 24), (0,32), 4)
        TextureManager.load_texture('player_walk_left', 'textures/character.png', (16, 24), (0,96), 4)
        TextureManager.load_texture('player_walk_up', 'textures/character.png', (16, 24), (0,64), 4)
        TextureManager.load_texture('player_walk_down', 'textures/character.png', (16, 24), (0,0), 4)

        # Setup controls
        InputManager.assign_control('move_up', pygame.K_UP)
        InputManager.assign_control('move_left', pygame.K_LEFT)
        InputManager.assign_control('move_right', pygame.K_RIGHT)
        InputManager.assign_control('move_down', pygame.K_DOWN)

        self.rootSceneNode = SceneNode()


    def create_scene(self):
        # Creating the scene
        self.player = Player()
        playerNode = SceneNode(self.rootSceneNode, self.player)

    def update(self):
        dT = pygame.time.get_ticks()/1000.0 - self.lastTime
        self.rootSceneNode.update(dT)

    def render(self):
        fillcolour = Color(25, 25, 40, 1)
        self.screen.fill(fillcolour)

        self.rootSceneNode.render(self.screen)

        pygame.display.flip()

    def quit(self):
        self.running = False

    def start_game(gameclass):
        pygame.init() # Start pygame.
        InputManager.setup()

        game = gameclass
        game.setup() # Set up the window
        game.create_scene()

        animation_frame_time = 0.0
        while(game.running):
            events = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.quit()
                else:
                    events.append(event)
            InputManager.update(events)

            animation_frame_time += pygame.time.get_ticks()/1000.0 - game.lastTime
            if animation_frame_time >= 1/game.animation_fps:
                TextureManager.next_frame()
                animation_frame_time = 0.0

            game.update() # Update the game code
            game.render() # Render all the game objects
            game.updateTime()
            pygame.time.delay(int((1/60.0) * 1000))


if __name__ == "__main__":
    Game.start_game( Game())