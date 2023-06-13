import pygame, sys
from pytmx.util_pygame import load_pygame
from os import walk
import pyscroll 

pygame.init()
screen_width, screen_height = (1920, 1080)
#screen_width = 1280
#screen_height = 720 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Topdown game level created by Tiled")

FPS = 60
clock = pygame.time.Clock()
dt = clock.tick(FPS)/1000

#import animation
def import_assets(assets_path):
    surface_list = []

    for i,j,image_file in walk(assets_path):
        for image in image_file:
            file_path = assets_path + '/' + image
            print(file_path)
            image_surf = pygame.image.load(file_path).convert_alpha
            surface_list.append(image_surf)

    return surface_list 

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, surf, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()
        self.speed = 2

        # animation
        self.import_player_animations()
        #self.frame_index = 0
        self.status = 'down'

    def import_player_animations(self):
        self.animation_dict = {'up':[],'down':[],'right':[],'left':[]}
        print(self.animation_dict.key())

        for animation in self.animation_dict.keys():
            anim_path = '../graphics/player_anim' + '/' + animation
            self.animation_dict[animation] = import_assets(anim_path)

    def player_animate(self,dt):
        self.frame_index += 4* dt
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
        
        self.rect.x += self.direction.x * speed
        self.rect.y += self.direction.y * speed
    
    def update(self,dt):
        self.input()
        self.move(self.speed)
        self.player_animate(dt)


# Import tiled layers with pytmx
tmx_data = load_pygame('C:\\Users\\170361\\Desktop\\KR01\\Tiled\\Mult_Layer.tmx')

map_data = pyscroll.TiledMapData(tmx_data)

# Make Scrolling layer
camera_w, camera_h = screen.get_size()
map_layer = pyscroll.BufferedRenderer(
    map_data,
    (camera_w,camera_h),
    clamp_camera = True,
    alpha = False)

# Pyscrolling group
pyscroll_group = pyscroll.PyscrollGroup(map_layer=map_layer)

# Sprite Group for Tileset
tile_sprite_group = pygame.sprite.Group()

# Sprite Group for Objects
player_sprite_group = pygame.sprite.Group()
#object_sprite_group = pygame.sprite.Group()

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos )

for layer in tmx_data.visible_layers:
    if hasattr(layer,'data'):
        for x,y,surf in layer.tiles():
            pos = (x * 32, y * 32)  # Mult by tilesize
            Tile(pos = pos, surf = surf, groups = tile_sprite_group)

# Get Objects layer 
for layer in ['Rock_Layer','Foliage_Layer','House_Layer','Tree_Layer']:
    for obj in tmx_data.get_layer_by_name(layer):
        pos = (obj.x,obj.y)
        pyscroll_group.add(Tile(pos = pos, surf = obj.image, groups = tile_sprite_group))

player_layer = tmx_data.get_layer_by_name('Player_Layer')
for obj in player_layer:
    if obj.name == 'Player_Start':
        pos = (obj.x,obj.y)
        player = Player(pos=pos,surf=obj.image,groups = player_sprite_group)
        pyscroll_group.add(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
    
    # Draw camera group
    pyscroll_group.center(player.rect.center)
    pyscroll_group.draw(screen)

    #tile_sprite_group.draw(screen)
    #player_sprite_group.draw(screen)
    player_sprite_group.update(dt)
    
    pygame.display.update()
    clock.tick(FPS)