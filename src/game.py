import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Educational Trivia")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
HOVER_BLUE = (100, 170, 220)
GREEN = (34, 139, 34)
RED = (220, 20, 60)

# Fonts
font = pygame.font.Font(None, 40)

# Define the path to the assets folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)  # Sube un nivel
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")  # Ahora está fuera de "src"

# Load sounds
try:
    pygame.mixer.init()
    correct_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Correct.mp3"))
    wrong_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Wrong.wav"))
except pygame.error as e:
    print(f"Error loading sound files: {e}")
    correct_sound = None
    wrong_sound = None

# Questions and answers (you can change it)
questions = [
    ("What year did Columbus discover America?", ["1492", "1600", "1776", "1810"], "1492"),
    ("Who wrote 'Don Quixote'?", ["Cervantes", "Shakespeare", "Borges", "Neruda"], "Cervantes"),
    ("What is the capital of France?", ["Madrid", "Paris", "London", "Rome"], "Paris")
]

# Question format
'''
[Question, [Answer 1, Answer 2, Answer 3, Answer 4], Correct Answer]
'''

# Shuffle questions and answer choices
random.shuffle(questions)
for q in questions:
    random.shuffle(q[1])

random.shuffle(questions)
current_question = 0
score = 0

# Function to draw text
def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# Function to show the final score
def show_final_score():
    total_questions = len(questions)
    percentage = (score / total_questions) * 100  # Calculate percentage

    if percentage == 100:
        final_text = "Perfect Score! Well Done!"
    elif percentage >= 80:
        final_text = f"Excellent job! Score: {score}/{total_questions}"
    elif percentage >= 50:
        final_text = f"Good effort! Score: {score}/{total_questions}"
    elif percentage >= 30:
        final_text = f"Keep practicing! Score: {score}/{total_questions}"
    else:
        final_text = f"Better luck next time! Score: {score}/{total_questions}"

    screen.fill(WHITE)
    draw_text(final_text, 250, 250, GREEN if percentage >= 50 else RED)
    pygame.display.flip()
    pygame.time.delay(3000)


# Function of the start screen
def show_start_screen():
    screen.fill(WHITE)

    # Start screen text
    draw_text("Welcome to Educational Trivia!", 200, 200, BLUE)
    draw_text("Click anywhere to start", 250, 300, BLACK)
    pygame.display.flip()

    # Wait until user presses anywhere in the screen
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

show_start_screen()

# Timer settings
time_limit = 10  # Seconds per question
start_ticks = pygame.time.get_ticks()  # Initialize timer

running = True
while running:
    screen.fill(WHITE)

    # Timer logic
    time_left = time_limit - (pygame.time.get_ticks() - start_ticks) // 1000
    draw_text(f"Time Left: {max(0, time_left)}", 600, 20)

    # Show question
    question_text = questions[current_question][0]
    draw_text(question_text, 100, 100)

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Draw answer buttons with hover effect
    buttons = []
    y_offset = 250
    for option in questions[current_question][1]:
        rect = pygame.Rect(250, y_offset, 300, 50)
        is_hovered = rect.collidepoint(mouse_x, mouse_y)

        color = HOVER_BLUE if is_hovered else BLUE
        pygame.draw.rect(screen, color, rect, border_radius=10)
        draw_text(option, rect.x + 20, rect.y + 10, WHITE)

        buttons.append((rect, option))
        y_offset += 70

    pygame.display.flip()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button, option in buttons:
                if button.collidepoint(event.pos):
                    if option == questions[current_question][2]:
                        if correct_sound is not None:
                            correct_sound.play()
                        score += 1
                    else:
                        if wrong_sound is not None:
                            wrong_sound.play()

                    pygame.time.delay(1500)  # Pause for 1.5 seconds to show feedback
                    current_question += 1

                    # If no more questions, show final score
                    if current_question >= len(questions):
                        show_final_score()
                        running = False
                    else:
                        start_ticks = pygame.time.get_ticks()  # Reset timer for new question

    # If time runs out, move to the next question
    if time_left <= 0:
        current_question += 1
        if current_question >= len(questions):
            show_final_score()
            running = False
        else:
            start_ticks = pygame.time.get_ticks()  # Reset timer for new question

pygame.quit()
