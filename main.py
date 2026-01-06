import random
import turtle
import time
from PIL import Image


TURTLE_BASE_SIZE = 20
TURTLE_SPEED = 2

# Resize an image
def resize_image_to_smaller(input_path, output_path, scale_factor):
    with Image.open(input_path) as img:
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        img_resized = img.resize((new_width, new_height))
        img_resized.save(output_path, format="GIF")
resize_image_to_smaller('smallflag.gif','flag.gif',0.2)

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
        if tim.distance(wall) < 16:
            wall_collision(False)

    for obj in flags:
        if tim.distance(obj)<5:
            obj.hideturtle()
            flags.pop(flags.index(obj))
            update_score()
    screen.ontimer(move_forward, 50)

def test_for_boundary_coll():
    tim_x = tim.pos()[0]
    tim_y = tim.pos()[1]
    if tim_x >= 420.0:
        tim.setpos(419.0, tim_y)
        wall_collision(True)
    if tim_x <= -425.0:
        tim.setpos(-424, tim_y)
        wall_collision(True)
    if tim_y >= 211:
        tim.setpos(tim_x, 210)
        wall_collision(True)
    if tim_y <= -205:
        tim.setpos(tim_x, -204)
        wall_collision(True)

def wall_collision(is_boundary):
    heading = tim.heading()
    pos = tim.pos()
    if heading == 0:
        if not is_boundary:
            tim.setpos(pos[0] - 2, pos[1])
        down()
    if heading == 180:
        if not is_boundary:
            tim.setpos(pos[0] + 2, pos[1])
        up()
    if heading == 90:
        if not is_boundary:
            tim.setpos(pos[0], pos[1] - 2)
        right()
    if heading == 270:
        if not is_boundary:
            tim.setpos(pos[0], pos[1] + 2)
        left()

# Function to create a turtle and calculate its effective collision radius
def create_bouncing_turtle(shape, color, size_x, size_y=None, start_pos=(0, 0), heading=0):
    t = turtle.Turtle(shape)
    t.penup()
    t.color(color)

    if size_y is None:
        size_y = size_x

    t.turtlesize(size_x, size_y)
    t.setheading(heading)
    t.goto(start_pos)
    return t

# Function to draw a full maze covering the screen
def draw_walls():
    global walls
    walls = []

    # Grid and maze settings
    cell_size = 20
    rows = 432 // cell_size
    cols = 864 // cell_size

    # Calculate grid coordinates, adding a buffer to y coordinates
    grid = [(x, y) for x in range(-cols // 2 * cell_size, cols // 2 * cell_size, cell_size)
                    for y in range(-rows // 2 * cell_size, rows // 2 * cell_size, cell_size*2)]

    # Create all walls (fill the screen initially)
    for x, y in grid:
        wall = create_bouncing_turtle('square', 'green', 1, 1, start_pos=(x, y))
        walls.append(wall)

    #Remove the wall at racer and flags spawn position
    for wall in walls:
        if wall.pos() in [(0,-60),(100,140),(330,0),(240,-100),(260,180),(260,-100),(-200,180),
                (-40,-220),(0,60),(-220,180),(-60,-220)]:
            walls.pop(walls.index(wall))
            wall.hideturtle()

    # Randomly remove walls to create paths in the maze
    random.shuffle(walls)
    num_paths = len(walls) // 2
    for _ in range(num_paths):
        #Ensure walls are remaining, then remove and hide half the walls on screen
        if walls:
            wall_to_remove = walls.pop()
            wall_to_remove.hideturtle()

def update_score():
    global score
    score+=1
    score_writer.clear()
    score_writer.write("Score: " + str(score), align="center", font=("Courier", 8, "bold"))
    if score==6:
        game_over=turtle.Turtle()
        game_over.hideturtle()
        game_over.penup()
        while True:
            color=random.choice(['red','blue'])
            game_over.pencolor(color)
            game_over.write("YOU WIN!", align='center', font=('Comic Sans MS', 50, 'bold'))
            time.sleep(0.2)


# Initialize screen
screen = turtle.Screen()
screen.setup(width=864, height=432)

for image in ['racerup.gif', 'racerdown.gif', 'racerleft.gif',
              'racerright.gif', 'rallyx_map.gif', 'flag.gif']:
    screen.register_shape(image)

#Initialize user racer
tim = turtle.Turtle()
tim.color("white")
tim.setheading(90)
tim.penup()
tim.goto(0, -50)
tim.shape("racerup.gif")

#Initialize flags
flags=[]

screen.tracer(0)
for pos in [(0,50),(100,134),(330,0),(250,-100),(-212,181),(-50,-200)]:
    flag=turtle.Turtle()
    flag.shape('flag.gif')
    flag.penup()
    flag.goto(pos)
    flags.append(flag)
screen.update()
screen.tracer(1)

#Initialize scoreboard
screen.tracer(0)
score_bg = turtle.Turtle()
score_bg.hideturtle()
score_bg.penup()
score_bg.goto(510, -88)
score_bg.pendown()
score_bg.fillcolor("black")
score_bg.begin_fill()

# Draw a rectangle for the background
for _ in range(2):  # 2 pairs of width/height
    score_bg.forward(60)  # Width
    score_bg.left(90)
    score_bg.forward(180)  # Height
    score_bg.left(90)
score_bg.end_fill()

# Write the score on top
score = 0
score_writer = turtle.Turtle()
score_writer.hideturtle()
score_writer.penup()
score_writer.goto(540, 60)  # Adjust text position
score_writer.pencolor("red")
score_writer.write("Score: " + str(score), align="center", font=("Courier", 10, "bold"))
screen.tracer(1)
screen.update()

#Initialize screen
screen.bgpic('rallyx_map.gif')

sc = tim.getscreen()
sc.listen()

screen.tracer(0) #Draw the maze walls without animations
draw_walls()
screen.update()
sc.tracer(1) #Turn animations back on

sc.onkey(up, "Up")
sc.onkey(down, "Down")
sc.onkey(left, "Left")
sc.onkey(right, "Right")

move_forward()

turtle.mainloop()