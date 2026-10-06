import pygame
import pandas as pd

class Map:
    def __init__(self, map_file):
        self.map_data = pd.read_csv(map_file)
        self.width = self.map_data['x'].max() + 1
        self.height = self.map_data['y'].max() + 1

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # Offsets entity position by camera position
        return entity.move(self.camera.topleft)

    def update(self, target):
        # Centers the camera on the player
        x = -target.rect.x + int(screen_width / 2)
        y = -target.rect.y + int(screen_height / 2)

        # Optional: Limit camera scrolling so it doesn't show the void outside the map
        x = min(0, x)  # Left border
        x = max(-(self.width - screen_width), x) # Right border
        y = min(0, y)  # Top border
        y = max(-(self.height - screen_height), y) # Bottom border

        self.camera = pygame.Rect(x, y, self.width, self.height)
