import pygame, sys
from os import walk
from pytmx.util_pygame import load_pygame
import pyscroll
#import pyscroll.data
#from pyscroll.group import PyscrollGroup

from debug_movement import debug_on_screen

pygame.init()
screen_width, screen_height = (1920, 1080)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Topdown game level created by Tiled")

FPS = 60
clock = pygame.time.Clock()
dt = clock.tick(FPS) / 1000

# Utils Import Assets from folder path We can separate this to other file #
def import_assets(assets_path):
    surface_list = []

    for i, j ,image_files in walk(assets_path):
        for image in image_files:
            file_path = assets_path + '/' + image
            print(file_path)
            image_surf = pygame.image.load(file_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list



class Player(pygame.sprite.Sprite):

    def __init__(self, pos, surf, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = pygame.math.Vector2()
        self.speed = 2
        
        self.import_player_animations()
        self.status = 'down'
        self.frame_index = 0 

    def import_player_animations(self):
        
        #self.animation_dict = {'up':[], 'down':[], 'right':[], 'left':[], 'down_right':[], 'down_left':[],
        #            'up_right':[], 'up_left':[]}
        
        self.animation_dict = {'up':[], 'down':[], 'right':[], 'left':[]}
        print(self.animation_dict.keys())
        for animation in self.animation_dict.keys():
            anim_path = '../graphics/player/player_anim/' + animation
            print(anim_path)
            self.animation_dict[animation] = import_assets(anim_path)

    def player_animate(self,dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animation_dict[self.status]):
            self.frame_index = 0 
        
        self.image = self.animation_dict[self.status][int(self.frame_index)]


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'

        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
            
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'

        else:
            self.direction.x = 0
    
    def move(self,speed):
        
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        #self.rect.x += self.direction.x * speed * dt
        self.rect.x += self.direction.x * speed

        # set collision state to horizon
        
        #self.rect.y += self.direction.y * speed * dt
        self.rect.y += self.direction.y * speed
        # set collision state to vertical
    
    
    def update(self,dt):
        self.input()
        self.move(self.speed)
        self.player_animate(dt)


# Import tiled layers with pytmx
tmx_data = load_pygame('C:\\Users\\Uncle Engineer\\Desktop\\pygame-tiled\\TiledClass\\Tiled_Editor\\Mult_Layer.tmx')

# Config for pyscroll
map_data = pyscroll.TiledMapData(tmx_data)

camera_w, camera_h = screen.get_size()

# Make the scrolling layer
map_layer = pyscroll.BufferedRenderer(
    map_data,
    (camera_w, camera_h),
    clamp_camera = True, 
    alpha= True)

# Make the pygame SpriteGroup with a scrolling map
pyscroll_group = pyscroll.PyscrollGroup(map_layer=map_layer)

# Sprite Group for Tileset
tile_sprite_group = pygame.sprite.Group()

# Sprite Group for Objects
player_sprite_group = pygame.sprite.Group()
object_sprite_group = pygame.sprite.Group()

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = surf.get_rect(topleft = pos)
        #self.rect = self.image.get_rect(topleft = pos )

for layer in tmx_data.visible_layers:
    if hasattr(layer,'data'):
        for x,y,surf in layer.tiles():
            pos = (x * 32, y * 32)  # Mult by tilesize
            Tile(pos = pos, surf = surf, groups = tile_sprite_group)
            #pyscroll_group.add(Tile(pos = pos, surf = surf, groups = tile_sprite_group))  # cuz the game to lagged out and weird rendering
            

for layer in ['Wooden_Layer', 'House_Layer', 'Tree_Layer', 'Rock_Layer', 'Foliage_Layer']:
    #print(layer)
    for obj in tmx_data.get_layer_by_name(layer):
        #print(obj.properties)
        pos = (obj.x, obj.y)
        pyscroll_group.add(Tile(pos = pos , surf = obj.image, groups = tile_sprite_group))

player_layer = tmx_data.get_layer_by_name('Player_Layer')
for obj in player_layer:

    if obj.name == 'Player_Start':
        pos = (obj.x , obj.y)
        player = Player(pos = pos, surf = obj.image, groups = player_sprite_group)
        pyscroll_group.add(player)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
    
    #object_sprite_group.draw(screen)

    # Draw camera sprite group
    pyscroll_group.center(player.rect.center) # set camera center to player

    #tile_sprite_group.draw(screen)
    pyscroll_group.draw(screen)
    #player_sprite_group.draw(screen)  # player is in pyscroll_group
    
    #debug_on_screen(player.direction)
    debug_on_screen(player.frame_index, 10, 10)

    player_sprite_group.update(dt)
    
    pygame.display.update()
    clock.tick(FPS)