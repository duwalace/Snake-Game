import pygame
import random
import sys

pygame.init()

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

DARK_GRAY = (220, 220, 220)
BLACK = (0, 0, 0)
BUTTON_BLUE = (0, 0, 255)
GOLD = (77, 109, 243)
DARK_RED = (139, 0, 0)

try:
    menu_font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 36)
except:
    menu_font = pygame.font.SysFont('Arial', 48, bold=True)
    button_font = pygame.font.SysFont('Arial', 36, bold=True)

try:
    laugh_sound = pygame.mixer.Sound("PeterGriffinLaugh.mp3")
    laugh_sound.set_volume(1.0)
    button_sound = pygame.mixer.Sound("Botao.mp3")
    button_sound.set_volume(1.0)
    gameover_sound = pygame.mixer.Sound("GameOver.mp3")
    gameover_sound.set_volume(1.0)
    brian_eat_sound = pygame.mixer.Sound("BrianBark.mp3")
    brian_eat_sound.set_volume(1.0)
except:
    laugh_sound = None
    button_sound = None
    gameover_sound = None
    brian_eat_sound = None

GRID_SIZE = 40
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

try:
    head_img = pygame.image.load("snake_head.png")
    body_img = pygame.image.load("snake_body.png")
    tail_img = pygame.image.load("snake_tail.png")
    brian_head_img = pygame.image.load("brian_head.png")
    brian_body_img = pygame.image.load("brian_body.png")
    brian_tail_img = pygame.image.load("brian_tail.png")
    apple_img = pygame.image.load("apple.png")
    pizza_img = pygame.image.load("pizza.png")
    beer_img = pygame.image.load("beer.png")
    game_over_img = pygame.image.load("GameOver.png")
    peter_gameover_img = pygame.image.load("petergameover.png")
    brian_gameover_img = pygame.image.load("maxresdefault.png")
    menu_background = pygame.image.load("fundomenu.jpeg")
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Erro ao carregar imagens: {e}")
    head_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
    head_img.fill((0, 255, 0))
    body_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
    body_img.fill((0, 200, 0))
    tail_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
    tail_img.fill((0, 150, 0))
    brian_head_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
    brian_head_img.fill((255, 255, 0))
    brian_body_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
    brian_body_img.fill((200, 200, 0))
    brian_tail_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
    brian_tail_img.fill((150, 150, 0))
    apple_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
    apple_img.fill((255, 0, 0))
    pizza_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
    pizza_img.fill((255, 165, 0))
    beer_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
    beer_img.fill((255, 255, 0))
    game_over_img = pygame.Surface((400, 300))
    game_over_img.fill((255, 0, 0))
    peter_gameover_img = pygame.Surface((600, 450))
    peter_gameover_img.fill((255, 0, 0))
    brian_gameover_img = pygame.Surface((600, 450))
    brian_gameover_img.fill((255, 255, 0))
    menu_background = None

apple_img = pygame.transform.scale(apple_img, (40, 40))
pizza_img = pygame.transform.scale(pizza_img, (40, 40))
beer_img = pygame.transform.scale(beer_img, (40, 40))

nova_largura = 600
nova_altura = 450
peter_gameover_img = pygame.transform.scale(peter_gameover_img, (nova_largura, nova_altura))
brian_gameover_img = pygame.transform.scale(brian_gameover_img, (nova_largura, nova_altura))

food_images = {
    "apple": apple_img,
    "pizza": pizza_img,
    "beer": beer_img
}

try:
    menu_background = pygame.image.load("fundomenu.jpeg")
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
except Exception as e:
    menu_background = None

direction = (1, 0)
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2), (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2)]
foods = []
walls = []
grow_snake = False
shield = False
shield_time = 0
inverted_controls = False
inverted_controls_time = 0
game_over = False
paused = False
in_menu = True
current_character = "peter"
transition_alpha = 0
transition_complete = False
game_over_time = 0
final_transition_alpha = 0
final_transition_complete = False
wall_pass = False
wall_pass_time = 0

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hover = False
        self.glow_size = 0
        self.glow_direction = 1
        self.max_glow = 10
        self.min_glow = 0
        self.glow_speed = 0.5
        
    def draw(self, surface):
        if self.hover:
            self.glow_size += self.glow_direction * self.glow_speed
            if self.glow_size >= self.max_glow:
                self.glow_direction = -1
            elif self.glow_size <= self.min_glow:
                self.glow_direction = 1
                
            glow_rect = pygame.Rect(
                self.rect.x - self.glow_size, 
                self.rect.y - self.glow_size, 
                self.rect.width + 2 * self.glow_size, 
                self.rect.height + 2 * self.glow_size
            )
            pygame.draw.rect(surface, GOLD, glow_rect, 3, border_radius=5)
            
        pygame.draw.rect(surface, BLACK, self.rect, border_radius=5)
        pygame.draw.rect(surface, GOLD, self.rect, 2, border_radius=5)
        
        text_surf = button_font.render(self.text, True, GOLD)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)
        return self.hover

def reset_game():
    global snake, direction, foods, walls, grow_snake, shield, shield_time, inverted_controls, inverted_controls_time, game_over, paused
    global transition_alpha, transition_complete, final_transition_alpha, final_transition_complete, wall_pass, wall_pass_time, gameover_sound_played

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2), (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2)]
    direction = (1, 0)

    foods = []
    generate_foods()

    walls = []

    grow_snake = False
    shield = False
    shield_time = 0
    inverted_controls = False
    inverted_controls_time = 0
    wall_pass = False
    wall_pass_time = 0
    
    game_over = False
    paused = False

    transition_alpha = 0
    transition_complete = False
    final_transition_alpha = 0
    final_transition_complete = False

def generate_foods():
    global foods
    
    if len(foods) < 2:
        num_foods_to_generate = 2 - len(foods)
        
        existing_food_types = [food["type"] for food in foods]
        
        all_food_types = ["apple", "pizza", "beer"]
        
        for _ in range(num_foods_to_generate):
            available_types = [t for t in all_food_types if t not in existing_food_types]
            
            if not available_types:
                available_types = [t for t in all_food_types if t != existing_food_types[-1]]
            
            food_type = random.choice(available_types)
            
            food_pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            while food_pos in snake or food_pos in walls or food_pos in [food["pos"] for food in foods]:
                food_pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            
            foods.append({"type": food_type, "pos": food_pos})
            
            existing_food_types.append(food_type)

def generate_walls():
    global walls
    wall_pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
    while wall_pos in snake or wall_pos in [food["pos"] for food in foods] or wall_pos in walls:
        wall_pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
    walls.append(wall_pos)

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = (180, 180, 180) if (x + y) % 2 == 0 else GOLD
            pygame.draw.rect(screen, color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_snake():
    global current_character

    if current_character == "peter":
        head = head_img
        body = body_img
        tail = tail_img
    else:
        head = brian_head_img
        body = brian_body_img
        tail = brian_tail_img

    for i, (x, y) in enumerate(snake):
        if i == 0:
            if direction == (0, -1):
                head_rotated = pygame.transform.rotate(head, 90)
            elif direction == (0, 1):
                head_rotated = pygame.transform.rotate(head, -90)
            elif direction == (-1, 0):
                head_rotated = pygame.transform.flip(head, True, False)
            elif direction == (1, 0):
                head_rotated = head
            screen.blit(head_rotated, (x * GRID_SIZE, y * GRID_SIZE))
        elif i == len(snake) - 1:
            prev_x, prev_y = snake[i - 1]
            tail_direction = (prev_x - x, prev_y - y)
            if tail_direction == (1, 0):
                tail_rotated = pygame.transform.flip(tail, True, False)
            elif tail_direction == (-1, 0):
                tail_rotated = tail
            elif tail_direction == (0, 1):
                tail_rotated = pygame.transform.rotate(tail, 90)
            elif tail_direction == (0, -1):
                tail_rotated = pygame.transform.rotate(tail, -90)
            else:
                tail_rotated = tail
            screen.blit(tail_rotated, (x * GRID_SIZE, y * GRID_SIZE))
        else:
            prev_x, prev_y = snake[i - 1]
            next_x, next_y = snake[i + 1] if i + 1 < len(snake) else (x, y)
            body_rotated = body
            if prev_x == next_x:
                body_rotated = pygame.transform.rotate(body, 90)
            screen.blit(body_rotated, (x * GRID_SIZE, y * GRID_SIZE))

def draw_foods():
    for food in foods:
        food_type = food["type"]
        food_pos = food["pos"]
        screen.blit(food_images[food_type], (food_pos[0] * GRID_SIZE, food_pos[1] * GRID_SIZE))

def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen, BLACK, (wall[0] * GRID_SIZE, wall[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

try:
    menu_background = pygame.image.load("fundomenu.jpeg")
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
except Exception as e:
    menu_background = None

try:
    titulo_img = pygame.image.load("Titulo.png")
    original_width, original_height = titulo_img.get_size()
    new_height = 700
    new_width = int((new_height / original_height) * original_width)
    titulo_img = pygame.transform.scale(titulo_img, (new_width, new_height))
except Exception as e:
    titulo_img = None

def menu_screen():
    if menu_background:
        screen.blit(menu_background, (0, 0))
    else:
        screen.fill(DARK_RED)
        for y in range(0, HEIGHT, 2):
            color_value = 100 + (y // 4) % 50
            pygame.draw.rect(screen, (color_value, 0, 0), (0, y, WIDTH, 2))

    if titulo_img:
        titulo_rect = titulo_img.get_rect(center=(WIDTH // 2, 100))
        screen.blit(titulo_img, titulo_rect.topleft)
    else:
        title = menu_font.render("SNAKE GAME", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title, title_rect)

    button_width = 280
    button_height = 60
    button_x = WIDTH // 2 - button_width // 2
    
    peter_button = Button(button_x, 280, button_width, button_height, "PLAY (PETER)")
    brian_button = Button(button_x, 360, button_width, button_height, "PLAY (BRIAN)")
    quit_button = Button(button_x, 440, button_width, button_height, "QUIT")
    
    mouse_pos = pygame.mouse.get_pos()
    peter_button.check_hover(mouse_pos)
    brian_button.check_hover(mouse_pos)
    quit_button.check_hover(mouse_pos)
    
    peter_button.draw(screen)
    brian_button.draw(screen)
    quit_button.draw(screen)
    
    pygame.display.update()
    
    return peter_button, brian_button, quit_button

def game_over_screen():
    global transition_alpha, transition_complete, game_over_time
    global final_transition_alpha, final_transition_complete

    if current_character == "peter":
        gameover_img = peter_gameover_img
    else:
        gameover_img = brian_gameover_img

    if not transition_complete:
        img_rect = gameover_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(gameover_img, img_rect.topleft)  
        
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.set_alpha(255 - transition_alpha)
        fade_surface.fill(BLACK)
        screen.blit(fade_surface, (0, 0))

        if transition_alpha < 255:
            transition_alpha += 15
        else:
            transition_alpha = 255
            transition_complete = True
            game_over_time = pygame.time.get_ticks()

    elif pygame.time.get_ticks() - game_over_time >= 1000 and not final_transition_complete:
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.set_alpha(final_transition_alpha)
        fade_surface.fill(BLACK)
        screen.blit(fade_surface, (0, 0))

        if final_transition_alpha < 255:
            final_transition_alpha += 15
        else:
            final_transition_alpha = 255
            final_transition_complete = True

    if final_transition_complete:
        screen.fill(BLACK)

        img_rect = game_over_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(game_over_img, img_rect.topleft)

        menu_button = Button(WIDTH // 2 - 125, HEIGHT // 2 + 150, 250, 50, "BACK TO MENU")
        
        mouse_pos = pygame.mouse.get_pos()
        menu_button.check_hover(mouse_pos)
        
        menu_button.draw(screen)

        pygame.display.update()
        return menu_button

    pygame.display.update()
    return None

def main():
    global direction, snake, foods, game_over, grow_snake, paused, in_menu, current_character
    global shield, shield_time, inverted_controls, inverted_controls_time, walls
    global wall_pass, wall_pass_time

    clock = pygame.time.Clock()
    
    reset_game()
    
    music_playing = False

    while True:
        if in_menu:
            peter_button, brian_button, quit_button = menu_screen()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if button_sound:
                        button_sound.play()
                    
                    if peter_button.rect.collidepoint(mouse_pos):
                        current_character = "peter"
                        in_menu = False
                        reset_game()
                        
                        try:
                            pygame.mixer.music.load('music.mp3')
                            pygame.mixer.music.set_volume(0.2)
                            pygame.mixer.music.play(-1)
                            music_playing = True
                        except:
                            print("Não foi possível carregar a música de fundo.")
                    
                    elif brian_button.rect.collidepoint(mouse_pos):
                        current_character = "brian"
                        in_menu = False
                        reset_game()
                        
                        try:
                            pygame.mixer.music.load('music.mp3')
                            pygame.mixer.music.set_volume(0.2)
                            pygame.mixer.music.play(-1)
                            music_playing = True
                        except:
                            print("Não foi possível carregar a música de fundo.")
                    
                    elif quit_button.rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    
                    if button_sound:
                        button_sound.play()
                
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    peter_button.check_hover(mouse_pos)
                    brian_button.check_hover(mouse_pos)
                    quit_button.check_hover(mouse_pos)
            
        elif game_over:
            menu_button = game_over_screen()
            
            if menu_button:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if menu_button.rect.collidepoint(mouse_pos):
                            in_menu = True
                            game_over = False
                            transition_alpha = 0
                            transition_complete = False
                            final_transition_alpha = 0
                            final_transition_complete = False
                            
                            if music_playing:
                                pygame.mixer.music.stop()
                                music_playing = False
                            
                            if button_sound:
                                button_sound.play()
            
        elif paused:
            pause_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                    if event.key == pygame.K_ESCAPE:
                        in_menu = True
                        paused = False
                        reset_game()
                        
                        if music_playing:
                            pygame.mixer.music.stop()
                            music_playing = False
                            
                        if button_sound:
                            button_sound.play()
            
        else:
            draw_grid()
            draw_snake()
            draw_foods()
            draw_walls()

            if len(foods) < 2:
                generate_foods()
            
            head_x, head_y = snake[0]
            
            for food in foods:
                if (head_x, head_y) == food["pos"]:
                    if food["type"] == "pizza":
                        wall_pass = True
                        wall_pass_time = pygame.time.get_ticks()
                    elif food["type"] == "beer":
                        inverted_controls = True
                        inverted_controls_time = pygame.time.get_ticks()
                    
                    grow_snake = True
                    
                    generate_walls()
                    
                    if current_character == "peter" and laugh_sound:
                        laugh_sound.play()
                    elif current_character == "brian" and brian_eat_sound:
                        brian_eat_sound.play()
                    
                    foods.remove(food)
                    generate_foods()
                    break
            
            if grow_snake:
                snake.append(snake[-1])
                grow_snake = False
            
            new_head = (head_x + direction[0], head_y + direction[1])
            
            if not wall_pass:
                if (new_head in walls or 
                    new_head in snake[1:] or 
                    new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
                    new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                    game_over = True
                    transition_alpha = 0
                    transition_complete = False
                    final_transition_alpha = 0
                    final_transition_complete = False
                    
                    if gameover_sound:
                        gameover_sound.play()
                    
                    if music_playing:
                        pygame.mixer.music.stop()
                        music_playing = False
            else:
                if new_head[0] < 0:
                    new_head = (GRID_WIDTH - 1, new_head[1])
                elif new_head[0] >= GRID_WIDTH:
                    new_head = (0, new_head[1])
                elif new_head[1] < 0:
                    new_head = (new_head[0], GRID_HEIGHT - 1)
                elif new_head[1] >= GRID_HEIGHT:
                    new_head = (new_head[0], 0)
                
                pass
            
            if not game_over:
                snake = [new_head] + snake[:-1]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        in_menu = True
                        reset_game()
                        
                        if music_playing:
                            pygame.mixer.music.stop()
                            music_playing = False
                    if event.key == pygame.K_p:
                        paused = True
                    
                    if not inverted_controls:
                        if event.key == pygame.K_w and direction != (0, 1):
                            direction = (0, -1)
                        if event.key == pygame.K_s and direction != (0, -1):
                            direction = (0, 1)
                        if event.key == pygame.K_a and direction != (1, 0):
                            direction = (-1, 0)
                        if event.key == pygame.K_d and direction != (-1, 0):
                            direction = (1, 0)
                    else:
                        if event.key == pygame.K_w and direction != (0, -1):
                            direction = (0, 1)
                        if event.key == pygame.K_s and direction != (0, 1):
                            direction = (0, -1)
                        if event.key == pygame.K_a and direction != (-1, 0):
                            direction = (1, 0)
                        if event.key == pygame.K_d and direction != (1, 0):
                            direction = (-1, 0)
            
            if wall_pass and pygame.time.get_ticks() - wall_pass_time > 5000:
                wall_pass = False
            if inverted_controls and pygame.time.get_ticks() - inverted_controls_time > 4000:
                inverted_controls = False
            
            pygame.display.update()
            clock.tick(10)

if __name__ == "__main__":
    main()