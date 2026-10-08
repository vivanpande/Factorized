import pygame
from Simulation.creation import Material, Machine, Recipe



iron_ore = Material("Iron_ore")
r_iron_ingot = Recipe("Iron_ingot", inputs={"Iron_ore": 1}, outputs={"Iron_ingot": 1}, process_time=5)
smelter = Machine("Smelter", r_iron_ingot)


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

screen_width, screen_height = screen.get_size()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
