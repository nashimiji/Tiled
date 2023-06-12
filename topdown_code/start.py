import pygame,sys
from pytmx.util_pygame import load_pygame

pygame.init()
screen_width, screen_height = (1024,1024)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Topdown game level created by Tiled")

FPS = 60
clock = pygame.time.Clock()

# Import Tiled layers with pytmx
tmx_data = load_pygame('D:\\งานนานา\\โครงงานคอม\\Tiled\\topdown.tmx')
# print(tmx_data)

# Created two spritegroup
tile_sprite = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()

# Create Tile class
class Tile(pygame.sprite.Sprite):
	def __init__(self, pos ,surf,groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)

# Get tileset from Tile Layer
for layer in tmx_data.visible_layers:
	if hasattr(layer,'data'):
		#print(layer)
		for x,y,surf in layer.tiles():
			pos = (x * 32,y * 32)
			Tile(pos = pos,surf = surf , groups = tile_sprite)

# Create Player class
class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surf,groups):
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		


# Get objects and player obj
object_layer = tmx_data.get_layer_by_name('Object_Layer')
#print(dir(object_layer))
for obj in object_layer:
	#print(obj)

	if obj.name == 'Player':
		'''
		print(obj.x)
		print(obj.y)
		print(obj.image)
		'''
		pos = (obj.x,obj.y)
		## Implement Player Class here
		player = Player(pos = pos , surf = obj.image , groups = player_sprite)
'''
	else:
		print(obj)
		pos = (obj.x,obj.y)
		Tile(pos = pos, surf = obj.image, groups = tile_sprite)
'''

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# screen.fill('black')
	tile_sprite.draw(screen)
	player_sprite.draw(screen)
	# sprite_group.draw
	# render sprites on to screen

	pygame.display.update()
	clock.tick(FPS)