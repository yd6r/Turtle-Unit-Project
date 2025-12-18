import random
import turtle
import time
from opcode import *
from PIL import Image
from PIL.ImageOps import scale


# Function to resize an image to smaller dimensions
def resize_image_to_smaller(input_path, output_path, scale_factor):
    with Image.open(input_path) as img:
        # Calculate new dimensions by scaling down
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        img_resized = img.resize((new_width, new_height))  # Resize the image
        img_resized.save(output_path, format="GIF")  # Save in GIF format

def right():
    tim.shape("small_racerright.gif")
    tim.setheading(0)

def left():
    tim.shape("small_racerleft.gif")
    tim.setheading(180)

def up():
    tim.shape("small_racerup.gif")
    tim.setheading(90)

def down():
    tim.shape("small_racerdown.gif")
    tim.setheading(270)

def move_forward():
    get_loc()
    tim.forward(2)
    screen.ontimer(move_forward, 50)

def print_loc(x,y):
    print(x,y)


def get_loc():
    tim_x=tim.pos()[0]
    tim_y=tim.pos()[1]
    if tim_x>=370.0:
        tim.setpos(370.0,tim_y)
    if tim_x<=-370.0:
        tim.setpos(-370,tim_y)

tim = turtle.Turtle()
tim.color("white")
tim.setheading(90)
tim.penup()
screen = turtle.Screen()
screen.setup(width=864,height=432)
for image in ['small_racerup.gif','small_racerdown.gif','small_racerleft.gif',
              'small_racerright.gif','small_rallyx_map.gif']:
    screen.register_shape(image)

tim.shape("small_racerup.gif")
screen.bgpic('small_rallyx_map.gif')

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