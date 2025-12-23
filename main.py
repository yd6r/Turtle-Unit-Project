import random
import turtle
import time
from opcode import *
from PIL import Image
from PIL.ImageOps import scale

TURTLE_BASE_SIZE = 20
TURTLE_SPEED=2

# Function to resize an image to smaller dimensions
def resize_image_to_smaller(input_path, output_path, scale_factor):
    with Image.open(input_path) as img:
        # Calculate new dimensions by scaling down
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        img_resized = img.resize((new_width, new_height))  # Resize the image
        img_resized.save(output_path, format="GIF")  # Save in GIF format


def right():
    tim.shape("racerright.gif")
    tim.setheading(0)

def left():
    tim.shape("racerleft.gif")
    tim.setheading(180)

def up():
    tim.shape("racerup.gif")
    tim.setheading(90)

def down():
    tim.shape("racerdown.gif")
    tim.setheading(270)

def move_forward():
    test_for_boundary_coll()
    tim.forward(2)
    for wall in walls:
        if tim.distance(wall)<15:
            wall_collision(False)
    screen.ontimer(move_forward, 50)

def print_loc(x,y):
    print(x,y)


def test_for_boundary_coll():
    tim_x=tim.pos()[0]
    tim_y=tim.pos()[1]
    if tim_x>=378.0:
        tim.setpos(377.0,tim_y)
        wall_collision(True)
    if tim_x<=-378.0:
        tim.setpos(-377,tim_y)
        wall_collision(True)
    if tim_y>=211:
        tim.setpos(tim_x,210)
        wall_collision(True)
    if tim_y<=-205:
        tim.setpos(tim_x,-204)
        wall_collision(True)

def wall_collision(is_boundary):
    heading=tim.heading()
    pos = tim.pos()
    if heading==0:
        if not is_boundary:
            tim.setpos(pos[0]-2,pos[1])
        down()
    if heading==180:
        if not is_boundary:
            tim.setpos(pos[0]+2,pos[1])
        up()
    if heading==90:
        if not is_boundary:
            tim.setpos(pos[0],pos[1]-2)
        right()
    if heading==270:
        if not is_boundary:
            tim.setpos(pos[0],pos[1]+2)
        left()

# Function to create a turtle and calculate its effective collision radius
def create_bouncing_turtle(shape, color, size_x, size_y=None, start_pos=(0, 0), heading=0):
    """
    Creates a turtle and calculates its effective collision radius based on its size.
    """
    t = turtle.Turtle(shape)
    t.penup()
    t.color(color)

    # Handle rectangle-like shapesize (e.g., shapesize(1, 3))
    if size_y is None:
        size_y = size_x

    # Set the visual size
    t.turtlesize(size_x, size_y)

    t.setheading(heading)
    t.goto(start_pos)

    return t

#Initialize screen and user racer
tim = turtle.Turtle()
tim.color("white")
tim.setheading(90)
tim.penup()
tim.goto(0,-50)
screen = turtle.Screen()
screen.setup(width=864,height=432)

#Draw walls
walls=[
    create_bouncing_turtle('square','green',1,1, (-50,y)) for y in [-200,-180,-160]
    ]

for image in ['racerup.gif','racerdown.gif','racerleft.gif',
              'racerright.gif','rallyx_map.gif']:
    screen.register_shape(image)

tim.shape("racerup.gif")
screen.bgpic('rallyx_map.gif')

sc = tim.getscreen()
sc.listen()

sc.onclick(print_loc)
sc.listen()
sc.onkey(up, "Up")
sc.onkey(down, "Down")
sc.onkey(left, "Left")
sc.onkey(right, "Right")


move_forward()

turtle.mainloop()