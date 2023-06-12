import pygame
pygame.init()

font = pygame.font.Font(None, 32)

def debug_on_screen(command, x, y):

    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(command), True, 'Red')
    #print(display_surf.get_rect().topright)  # (1920,0)
    display_surf_topright = display_surf.get_rect().topright
    debug_rect = debug_surf.get_rect(topright = (display_surf_topright[0] - x,display_surf_topright[1] + y))
    pygame.draw.rect(display_surf, 'Black', debug_rect)  # add black bg
    display_surf.blit(debug_surf, debug_rect)

