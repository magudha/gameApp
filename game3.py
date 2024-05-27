import pygame
import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import random
# Initialize Pygame
pygame.init()

# Define game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)
BRICK_SIZE = 40
BOARD_WIDTH = 8
BOARD_HEIGHT = 12
TIMER_FONT_SIZE = 36

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CRYPTRIS")

# Game state
is_game_running = False
is_key_created = False
is_encryption_done = False
is_decryption_done = False

# Define fonts
font = pygame.font.Font(None, 36)
text_color = (255, 255, 255)

# User data
username = ""
# Tetris-like block shapes
BLOCKS = [
    [[1, 1, 1, 1]],  # I-block
    [[1, 1], [1, 1]],  # O-block
    [[1, 1, 1], [0, 0, 1]],  # L-block
    [[1, 1, 1], [1, 0, 0]],  # J-block
    [[1, 1, 1], [0, 1, 0]],  # T-block
    [[1, 1, 0], [0, 1, 1]],  # S-block
    [[0, 1, 1], [1, 1, 0]]  # Z-block
]

class Block:
    def __init__(self, shape):
        self.shape = shape
        self.rotation = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def get_current_shape(self):
        return self.shape[self.rotation]

def get_random_block():
    return Block(random.choice(BLOCKS))

# # Example of generating and displaying a random Tetris-like block
# if __name__ == "__main__":
#     random_block = get_random_block()
#     current_shape = random_block.get_current_shape()
    
#     for row in current_shape:
#         print(' '.join(['#' if cell == 1 else ' ' for cell in row]))

class CryptRisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("CRYPTRIS")
        self.is_running = False
        self.private_key = None
        self.public_key = None
        self.timer = 60
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        # self.current_block = self.get_random_block()
        self.current_block_x = 3
        self.current_block_y = 0

    def draw_about_screen(self):
        self.screen.fill(BACKGROUND_COLOR)

    def draw_game_interface(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_board()
        self.draw_block()
        self.draw_timer()
        self.draw_controls()
        self.draw_other_elements()

    def draw_main_menu(self):
        self.screen.fill(BACKGROUND_COLOR)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not is_game_running:
            # Display the main menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                # Start a new game
                is_game_running = True
                username = ""  # Reset the username
                is_key_created = False
                is_encryption_done = False
                is_decryption_done = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                # Show the "About" screen
                # Implement your "About" screen logic here
                def draw_about_screen(self):
                    self.screen.fill(BACKGROUND_COLOR)
            
                    # Create a font for the about screen text
                    font = pygame.font.Font(None, 36)

                    about_text = [
                        "CRYPTRIS - A Game of Encryption and Decryption",
                        "--------------------------------------------",
                        "In this game, you'll experience the principles of asymmetric cryptography.",
                        "Use your skills to encrypt and decrypt messages using keys.",
                        "Created as a fun and educational way to learn about encryption techniques.",
                        "Enjoy the game and stay secure!",
                        "",
                        "Press 'B' to go back to the main menu."
                        ]

                    y = 100
                    for line in about_text:
                        text = font.render(line, True, (255, 255, 255))
                        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
                        self.screen.blit(text, text_rect)
                        y += 50


        else:
            # Game logic
            if not is_key_created:
                # Implement key creation logic
                # Generate a key pair
                private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

                # Serialize the keys
                private_pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption())

                public_key = private_key.public_key()
                public_pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo)

                # Save the keys for later use
                with open("private_key.pem", "wb") as f:
                    f.write(private_pem)
                    with open("public_key.pem", "wb") as f:
                        f.write(public_pem)

            if is_encryption_done:
                # Implement encryption logic
                # Load the recipient's public key
                with open("public_key.pem", "rb") as f:
                     public_key_pem = f.read()
                     recipient_public_key = serialization.load_pem_public_key(public_key_pem)

                # Encrypt a message
                message = "This is a secret message"
                encrypted_message = recipient_public_key.encrypt(
                    message.encode('utf-8'),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None))

            if is_decryption_done:
                # Implement decryption logic
                # Load the player's private key
                with open("private_key.pem", "rb") as f:
                    private_key_pem = f.read()
                    player_private_key = serialization.load_pem_private_key(private_key_pem, password=None)

                # Decrypt the message
                decrypted_message = player_private_key.decrypt(
                    encrypted_message,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None))

                print(decrypted_message.decode('utf-8'))

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    if not is_game_running:
        # Display the main menu options
        # Implement your main menu graphics here
        def draw_main_menu(self):
            self.screen.fill(BACKGROUND_COLOR)
        
            # Create a font for the menu text
            font = pygame.font.Font(None, 36)

            # Render and display menu text
            text = font.render("CRYPTRIS", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(text, text_rect)

            # Render and display menu options
            menu_options = ["New Game (Press 'N')", "About This Game (Press 'A')"]
            for i, option in enumerate(menu_options):
                text = font.render(option, True, (255, 255, 255))
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 50))
                self.screen.blit(text, text_rect)

    else:
        # Implement the game interface
          def draw_game_interface(self):
              self.screen.fill(BACKGROUND_COLOR)
              # Draw the game board
              for row in range(12):
                  for col in range(8):
                      pygame.draw.rect(self.screen, self.get_color(self.game_board[row][col]), [col * 50, row * 50, 50, 50])
                   
                 # Draw player's keys
              key_font = pygame.font.Font(None, 36)

              for i, key in enumerate(self.player_keys):
                text = key_font.render(key, True, (255, 255, 255))
                text_rect = text.get_rect(center=(i * 60 + 40, 550))
                self.screen.blit(text, text_rect)

                # Draw timer
              timer_font = pygame.font.Font(None, 36)
              timer_text = timer_font.render(f"Time: {self.timer}", True, (255, 255, 255))
              timer_rect = timer_text.get_rect(topleft=(20, 20))
              self.screen.blit(timer_text, timer_rect)

        # Draw controls/arrows
        # Implement the rendering of controls here
        
   

    def draw_controls(self):
        font = pygame.font.Font(None, 36)

        # Render and display control instructions
        controls_text = [
            "Controls:",
            "LEFT/RIGHT: Move Key",
            "UP/SPACE: Invert Key",
            "DOWN: Confirm Key",
            "ESC: Pause/Resume",
        ]

        y = 20
        for line in controls_text:
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(topleft=(20, y))
            self.screen.blit(text, text_rect)
            y += 40

        # Draw other game elements as needed
        # Implement rendering of other game elements

    def get_color(self, value):
        if value == "-1":
            return (0, 0, 255)  # Blue-azure
        elif value == "0":
            return (0, 0, 128)  # Blue-dark
        elif value == "1":
            return (173, 216, 230)  # Blue-light
        # Include the Tetris-like board, keys, timer, controls, etc.
    def draw_board(self):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                brick = self.board[row][col]
                pygame.draw.rect(self.screen, self.get_brick_color(brick), (col * BRICK_SIZE, row * BRICK_SIZE, BRICK_SIZE, BRICK_SIZE))

    def draw_block(self):
        for row in range(len(self.current_block)):
            for col in range(len(self.current_block[0])):
                if self.current_block[row][col] != 0:
                    x = (self.current_block_x + col) * BRICK_SIZE
                    y = (self.current_block_y + row) * BRICK_SIZE
                    pygame.draw.rect(self.screen, self.get_brick_color(self.current_block[row][col]), (x, y, BRICK_SIZE, BRICK_SIZE))

    def draw_timer(self):
        font = pygame.font.Font(None, TIMER_FONT_SIZE)
        timer_text = font.render(f"Time: {self.timer}", True, (255, 255, 255))
        self.screen.blit(timer_text, (20, 20))

    def draw_controls(self):
        # Implement the rendering of controls here
        pass


    def get_brick_color(self, value):
        if value == -1:
            return (0, 0, 255)  # Blue-azure
        elif value == 0:
            return (0, 0, 128)  # Blue-dark
        elif value == 1:
            return (173, 216, 230)  # Blue-light


    if __name__ == "__main__":
        game = CryptRisGame()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle user input for game controls here
                if game.is_running and not game.about_screen:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            game.move_block(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            game.move_block(1, 0)
                        elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                            game.invert_block()
                        elif event.key == pygame.K_DOWN:
                            game.confirm_block()
                        elif event.key == pygame.K_ESCAPE:
                            game.toggle_pause()

            if not game.is_running:
                if game.draw_about_screen:
                    game.draw_about_screen()
                else:
                    game.draw_main_menu()
            else:
                game.draw_game_interface()

            pygame.display.flip()

    