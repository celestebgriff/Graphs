from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# visited dictionary
visited = {}
# reverse path for backtracking
reverse_path = []
# opposite directions
opposite_direction = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}


# Add first room to visited dictionary, get its exits
visited[player.current_room.id] = player.current_room.get_exits()

# While visited < length of rooms in the graph
while len(visited) < len(room_graph):
    # if not visited
    if player.current_room.id not in visited:
        # add to visited, get exits
        visited[player.current_room.id] = player.current_room.get_exits()
        # remove direction just visited from unexplored paths
        previous_direction = reverse_path[-1]
        visited[player.current_room.id].remove(previous_direction)

    # if all the paths have been explored
    if len(visited[player.current_room.id]) == 0: 
        # backtrack until unexplored path is found
        # assign the last addition as the previous direction to the reverse_path
        previous_direction = reverse_path[-1]
        # pop from reverse path
        reverse_path.pop()
        # add previous direction to traversal_path
        traversal_path.append(previous_direction)
        # move player that direction
        player.travel(previous_direction)

    # if there is unexplored direction, add direction to traversal_path
    else:
        # go first available direction in the room, assign it to direction
        direction = visited[player.current_room.id][-1]
        # pop from list
        visited[player.current_room.id].pop()
        # add direction to traversal_path
        traversal_path.append(direction)
        # add opposite direction to reverse_path
        reverse_path.append(opposite_direction[direction])
        # move player that direction
        player.travel(direction)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")