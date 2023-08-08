from PIL import Image, ImageDraw
from random import choice, randint
import math
import csv

# Function to convert RGB to hex color code
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

# CSV file columns
csv_columns = ["TokenID", "name","file_name", "image_name", "Attribute[Hat]", "Attribute[Mood]", "Attribute[Face]"]
csv_file_path = "metadata.csv"


# Function to generate a random color
def random_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

# Constants
MAX_SUPPLY = 200
WIDTH, HEIGHT = 350, 350
BACKGROUND_COLOR = (220, 225, 225)  # Light gray

# Define colors for the hat and face
HAT_COLOR = (139, 69, 19)  # Brown
random_face_color = (255, 228, 196)  # Peach

# Constants for face and hat
FACE_RADIUS = 80
HAT_HEIGHT = 80
HAT_WIDTH = 160
EYE_SIZE = 8
MOUTH_WIDTH = 20
NOSE_SIZE = 10

# Lowering the nose by adjusting its vertical position
NOSE_Y_OFFSET = 10  # Offset to lower the nose

# Define colors for the hat and face
HAT_COLOR = (139, 69, 19)  # Brown


# Constants for the gentleman's hat
BRIM_WIDTH = HAT_WIDTH
CROWN_WIDTH = HAT_WIDTH // 2
CROWN_TOP_HEIGHT = 20

# Constants for the hat's brim and crown
BRIM_HEIGHT = 10
CROWN_HEIGHT = 30

# Draw the circle
center = (WIDTH // 2, HEIGHT // 2)

# Adjustments for a higher and thicker hat
THICKER_BRIM_HEIGHT = 15  # Thicker brim
THICKER_CROWN_HEIGHT = 40  # Thicker crown

# Position the brim even higher
higher_brim_top_left = (center[0] - BRIM_WIDTH // 2, center[1] - EYE_SIZE - BRIM_HEIGHT - THICKER_BRIM_HEIGHT - 40)
higher_brim_bottom_right = (center[0] + BRIM_WIDTH // 2, center[1] - EYE_SIZE - THICKER_BRIM_HEIGHT - 40)
higher_crown_top_left = (center[0] - CROWN_WIDTH // 2, center[1] - EYE_SIZE - BRIM_HEIGHT - THICKER_CROWN_HEIGHT - 40)
higher_crown_bottom_right = (center[0] + CROWN_WIDTH // 2, center[1] - EYE_SIZE - THICKER_BRIM_HEIGHT - 40)

# Function to draw the face, eyes, mouth, and lowered nose
def draw_normal_face(draw):
    # Random face color
    random_face_color = (randint(200, 255), randint(180, 230), randint(180, 200))
    draw.ellipse([center[0] - FACE_RADIUS, center[1] - FACE_RADIUS, center[0] + FACE_RADIUS, center[1] + FACE_RADIUS], outline=random_face_color, fill=random_face_color)
    draw.rectangle([center[0] - EYE_SIZE - 20, center[1] - EYE_SIZE, center[0] - 20, center[1]], fill="black")
    draw.rectangle([center[0] + 20, center[1] - EYE_SIZE, center[0] + EYE_SIZE + 20, center[1]], fill="black")
    draw.line([center[0] - MOUTH_WIDTH // 2, center[1] + 30, center[0] + MOUTH_WIDTH // 2, center[1] + 30], fill="black", width=2)
    draw.ellipse([center[0] - NOSE_SIZE // 2, center[1] - NOSE_SIZE // 2 + NOSE_Y_OFFSET, center[0] + NOSE_SIZE // 2, center[1] + NOSE_SIZE // 2 + NOSE_Y_OFFSET], outline="black", fill="black")

# Function to draw a happy face with a smiling mouth
def draw_happy_face(draw):
    draw_normal_face(draw)  # Start with the normal face
    # Redraw the mouth as a smile (a portion of a circle)
    smile_radius = MOUTH_WIDTH // 2
    draw.arc([center[0] - smile_radius, center[1] + 20, center[0] + smile_radius, center[1] + 40], start=0, end=180, fill="black", width=2)

# Function to draw the hat on the given image
def draw_hat(draw, hat_color, brim_top_left, brim_bottom_right, crown_top_left, crown_bottom_right):
    draw.rectangle([brim_top_left, brim_bottom_right], outline=hat_color, fill=hat_color)
    draw.rectangle([crown_top_left, crown_bottom_right], outline=hat_color, fill=hat_color)

# Function to draw a happy face with a closed-mouth smile (matching the reference image)
def draw_happy_face_mouth_closed(draw):
    # Draw the face, eyes, and nose as before
    random_face_color = (randint(200, 255), randint(180, 230), randint(180, 200))
    draw.ellipse([center[0] - FACE_RADIUS, center[1] - FACE_RADIUS, center[0] + FACE_RADIUS, center[1] + FACE_RADIUS], outline=random_face_color, fill=random_face_color)
    draw.rectangle([center[0] - EYE_SIZE - 20, center[1] - EYE_SIZE, center[0] - 20, center[1]], fill="black")
    draw.rectangle([center[0] + 20, center[1] - EYE_SIZE, center[0] + EYE_SIZE + 20, center[1]], fill="black")
    draw.ellipse([center[0] - NOSE_SIZE // 2, center[1] - NOSE_SIZE // 2 + NOSE_Y_OFFSET, center[0] + NOSE_SIZE // 2, center[1] + NOSE_SIZE // 2 + NOSE_Y_OFFSET], outline="black", fill="black")

    # Draw the new closed-mouth smile (a continuous curved line)
    smile_radius = MOUTH_WIDTH // 2
    smile_path = []
    for i in range(center[0] - smile_radius, center[0] + smile_radius, 1):
        angle = math.acos((i - center[0]) / smile_radius)
        y = center[1] + 25 + smile_radius * math.sin(angle)  # Adjusted to create a closed smile
        smile_path.append((i, y))
    draw.line(smile_path, fill="black", width=2)

# Function to draw the body with a T-shirt
def draw_body(draw, shirt_color):
    body_top = center[1] + FACE_RADIUS
    body_bottom = center[1] + FACE_RADIUS + BODY_HEIGHT
    draw.rectangle([center[0] - BODY_WIDTH // 2, body_top, center[0] + BODY_WIDTH // 2, body_bottom], outline=shirt_color, fill=shirt_color)

# Constants for body and T-shirt
BODY_WIDTH = 120
BODY_HEIGHT = 200

def runBatch():
    # Generate and save 10 images with random hat colors
    with open(csv_file_path, mode="w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()

        for i in range(1, MAX_SUPPLY+1):
            # Create a new image with the same background color
            image_random_face = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
            draw_random_face = ImageDraw.Draw(image_random_face)
            

            # Choose one of the three face expressions
            expression_func = choice([draw_normal_face, draw_happy_face, draw_happy_face_mouth_closed])
            expression_func(draw_random_face)
            mood = "Neutral" if expression_func == draw_normal_face else "Happy" if expression_func == draw_happy_face else "Smiling"
            # Randomly include a hat or not
            hat_color_hex = ""
            random_hat_color = (randint(120, 255), randint(120, 255), randint(120, 255))
            if choice([True, False]):
                hat_color_hex = rgb_to_hex(random_hat_color)
                draw_hat(draw_random_face, random_hat_color, higher_brim_top_left, higher_brim_bottom_right, higher_crown_top_left, higher_crown_bottom_right)
            draw_body(draw_random_face, random_hat_color)
            # Save the image
            image_random_face.save(f"{i}.png")
            file_name = f"{i}.png"
            token_name=f"#{i}"
            # Write data to CSV
            writer.writerow({
                "TokenID": i,
                "name": token_name,
                "file_name": file_name,
                "image_name": file_name,
                "Attribute[Hat]": hat_color_hex,
                "Attribute[Mood]": mood,
                "Attribute[Face]": rgb_to_hex(random_face_color)
            })


def createSpecial():
    # Create a new image with the same background color
    image_random_face = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw_random_face = ImageDraw.Draw(image_random_face)
    FACE_COLOR = (255, 228, 196)  # Peach
    # Choose one of the three face expressions
    expression_func = choice([draw_normal_face])
    expression_func(draw_random_face)
    mood = "Neutral" if expression_func == draw_normal_face else "Happy" if expression_func == draw_happy_face else "Smiling"
    # Randomly include a hat or not
    hat_color_hex = ""
    random_hat_color = (randint(0, 0), randint(0, 0), randint(0, 0))
    if choice([True, False]):
        hat_color_hex = rgb_to_hex(random_hat_color)
        draw_hat(draw_random_face, random_hat_color, higher_brim_top_left, higher_brim_bottom_right, higher_crown_top_left, higher_crown_bottom_right)
    draw_body(draw_random_face, random_hat_color)
    # Save the image
    file_name = f"{randint(0, 100)}.png"
    image_random_face.save(f"{file_name}")
    


runBatch()
#createSpecial()
