# thank to Nate @ http://natewm.com/blog/2012/01/python-recursive-maze-example/
"""maze.py: Creates a maze to illustrate recursion."""
 
import random
 
def makeMaze(width, height):
    """Initializes an 2D list for the maze then begins the recurseive function.
 
    Args:
        width: Number of junction points accross (maze width is twice the size)
        height: Number of junction points down (maze height is twice the size)
 
    Returns:
        A 2D list containing a maze of twisted passageways.
    """
 
    # Create the list of lists filled with zeros to hold the maze information.
    # The maze will actually be twice as tall and wide as the size given.
    maze = [[0 for j in range(width*2)] for i in range(height*2)]
 
    # Begin recursion starting in the center and are even numbers.
    recurseMaze(maze, int(width / 2) * 2, int(height / 2) * 2, 0, 0)
 
    # The maze returned has all it's hallways in place.
    return maze
 
 
def recurseMaze(maze, x, y, dirx, diry):
    """This function is added to the call stack each time it is called.  It keeps
    track if it's location and directions, so when functions are removed from the
    stack and returns here the functions know where it's left off.
 
    Args:
        maze: The 2D list that the maze data will be stored in.
        x: The X location of the current cell in the maze.
        y: The Y location of the current cell in the maze.
        dirx: The x direction that was taken to get to this cell.
        diry: The y direction that was taken to get to this cell.
 
    Returns:
        Nothing
    """
 
    # Return if x or y is out of bounds or if the space is not wall.
    if not 0 <= y < len(maze) or not 0 <= x < len(maze[0]) or maze[y][x] != 0:
        return
 
    # Mark the hallway between the current space and space leading here.
    maze[y-diry][x-dirx] = 1
 
    # Mark the current space as a hallway.
    maze[y][x] = 1
 
    # Initialize the directions the hallway can go.
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
 
    # Shuffle those directions so our maze will have random paths
    random.shuffle(directions)
 
    # Go through each of these directions and call the recursive function.
    for dx, dy in directions:
        recurseMaze(maze, x + dx * 2, y + dy * 2, dx, dy)
 
 
def mazeString(maze, chars):
    """This function takes the lists of 1's and 0's and returns a string that
    can easily be printed to the screen.
 
    Args:
        maze: The maze lists holding the maze information.
        chars: The characters that should be used for drawing the maze (wall, hall)
 
    Returns:
        A string representing the maze that is ready for printing.
    """
 
    # Start with a solid wall on the top
    s = chars[0] * (len(maze[0]) + 1) + "\n"
 
    for row in maze:
        # Put a wall on the left edge
        s += chars[0]
 
        for cell in row:
            # Fill in the maze
            s += chars[cell]
 
        # New line at the end of each row
        s += "\n"
 
    # Return maze ready for printing.
    return s
