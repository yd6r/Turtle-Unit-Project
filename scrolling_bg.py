import turtle
import math  # Needed for an elegant way to center the player later, but not strictly for scrolling

# --- Configuration ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
TILE_SIZE = 7  # Assumes your grass_tile.gif is 100x100 pixels
MAP_GRID_SIZE = 10  # A 10x10 grid of tiles creates a large 1000x1000 world

# 2. The Map Drawer Turtle (responsible for stamping the background)
map_drawer = turtle.Turtle()
# Use the custom shape if it was loaded, otherwise use 'square' as a fallback
map_drawer.shape("square")  # Fallback to a standard shape
map_drawer.color("green")
map_drawer.turtlesize(TILE_SIZE / 20)  # Resize the default 20x20 square to TILE_SIZE
map_drawer.penup()
map_drawer.hideturtle()
map_drawer.speed(0)

# --- Camera & Map State ---
# world_offset is the virtual position of the player in the large world
world_offset_x = 0
world_offset_y = 0

# Store the world coordinates of the center of each tile
tile_centers = []
world_limit = (MAP_GRID_SIZE * TILE_SIZE) / 2

for r in range(-MAP_GRID_SIZE // 2, MAP_GRID_SIZE // 2):
    for c in range(-MAP_GRID_SIZE // 2, MAP_GRID_SIZE // 2):
        # Calculate the world coordinates of the tile center
        center_x = (c * TILE_SIZE) + (TILE_SIZE / 2)
        center_y = (r * TILE_SIZE) + (TILE_SIZE / 2)
        tile_centers.append((center_x, center_y))

def redraw_map():
    """Clears and redraws all map tiles based on the current camera/world offset."""
    #map_drawer.clearstamps()

    # Calculate the visible area (screen center +/- half screen size)
    # This helps skip drawing tiles far outside the current view for performance.
    half_screen_w = SCREEN_WIDTH / 2
    half_screen_h = SCREEN_HEIGHT / 2

    for x_world, y_world in tile_centers:

        # Calculate the tile's position *relative to the screen* (the camera)
        x_screen = x_world - world_offset_x
        y_screen = y_world - world_offset_y

        # Only stamp if the tile is near the screen boundaries (optimisation)
        if (x_screen > -half_screen_w - TILE_SIZE and x_screen < half_screen_w + TILE_SIZE and
                y_screen > -half_screen_h - TILE_SIZE and y_screen < half_screen_h + TILE_SIZE):
            map_drawer.goto(x_screen, y_screen)


def move_camera(dx, dy, racer):
    """
    Moves the camera (world offset) and redraws the scene.
    The player's position is updated by the same amount, but the background compensates.
    """
    global world_offset_x, world_offset_y

    # Update the camera offset (which is the player's true position in the world)
    world_offset_x += dx
    world_offset_y += dy

    # Clamp the world offset to the boundaries of the map
    world_offset_x = max(-world_limit, min(world_offset_x, world_limit))
    world_offset_y = max(-world_limit, min(world_offset_y, world_limit))

    # 1. Redraw the map elements using the new camera offset
    redraw_map()

    # 2. Update the player's screen position
    # The player's *screen* position should remain fixed at the center (0,0) in a perfect system,
    # but we will move it slightly to give the feeling of walking, and the camera is *following* it.
    #racer.setx(racer.xcor() + dx)
    #racer.sety(racer.ycor() + dy)

    # Re-center the player if they move too far from the screen center (optional)
    # The background scrolling itself is the main trick.

    # Finally, update the screen
    from main import screen  # Import screen from main here to avoid circular import
    screen.update()