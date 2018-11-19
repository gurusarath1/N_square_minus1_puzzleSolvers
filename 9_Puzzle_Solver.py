import copy

# This functions all possible states that are not yet visited
def Next_State_Generator(current_state, visited_states):
	allowed_states = []
	allowed_swaps = []
	max_col_index = len(current_state[0]) - 1
	max_row_index = len(current_state) - 1

	current_x_mark_pos = find_x_pos(current_state)

	# Generate all the possible swaps from the current states
	# Maximum possible swaps 4
	# Minimum possible swaps 2
	if(current_x_mark_pos[0] + 1 <= max_row_index):
		allowed_1_swap = [[current_x_mark_pos[0], current_x_mark_pos[1]], [current_x_mark_pos[0] + 1, current_x_mark_pos[1]]]
	else:
		allowed_1_swap = None

	if(current_x_mark_pos[0] - 1 >= 0):
		allowed_2_swap = [[current_x_mark_pos[0], current_x_mark_pos[1]], [current_x_mark_pos[0] - 1, current_x_mark_pos[1]]]
	else:
		allowed_2_swap = None

	if(current_x_mark_pos[1] + 1 <= max_col_index):
		allowed_3_swap = [[current_x_mark_pos[0], current_x_mark_pos[1]], [current_x_mark_pos[0], current_x_mark_pos[1] + 1]]
	else:
		allowed_3_swap = None

	if(current_x_mark_pos[1] - 1 >= 0):
		allowed_4_swap = [[current_x_mark_pos[0], current_x_mark_pos[1]], [current_x_mark_pos[0], current_x_mark_pos[1] - 1]]
	else:
		allowed_4_swap = None

	allowed_swaps = (allowed_1_swap, allowed_2_swap, allowed_3_swap, allowed_4_swap)

	i = 0

	for swapX in allowed_swaps:

		if swapX == None:
			pass
		else:
			state = copy.deepcopy(current_state)
			swapped_state = perform_piece_swap(state, allowed_swaps[i])
			# add the state into allowed_states only if the state was never visited
			if not (swapped_state in visited_states):
				allowed_states.append(swapped_state)

		i = i + 1

	#Uncomment the section below to track the algorithm
	#print('-------')
	#print(current_state)
	#print(allowed_states)
	
	return allowed_states


# Function that swaps two pieces in a state
def perform_piece_swap(state, swap):
	swap_piece_val = state[swap[1][0]] [swap[1][1]]
	state[swap[0][0]] [swap[0][1]] = swap_piece_val
	state[swap[1][0]] [swap[1][1]] = 'x'
	# Return the two elements to be swapped 
	# [X location, Number's location]
	return state


#function that finds the current blank ('x') position
def find_x_pos(state):
	found = 0

	for r in range(0, len(state)):
		for c in range(0, len(state[0])):
			if state[r][c] == 'x':
				found = 1
				break
		if found == 1:
			break

	# Return the indices the blank piece location
	return [r,c]

# This function prints the elements in a proper fashion
def print_state(state, text = ''):
	print('-------------------- ' + text)

	for r in range(0, len(state)):
		for c in range(0, len(state[0])):
			print(state[r][c], end='')
			print(' ', end='')
		print('')

# -------X**2 - 1 Puzzle Solver -----------------------------------------------------------------------------

goal_state = [[1,2,3],[4,5,6],[7,8,'x']]
#start_state = [['x',2,3],[4,5,1],[7,8,6]]
start_state = [[7,3,'x'], [8,1,5], [6,4,2]]

# Present state is start state in the beginning
present_state = copy.deepcopy(start_state)
visited_states = []
solution_path = []
available_states = []
number_of_iterations = 0
camefrom_dict = dict()

# Print the size of the board
print('This is a ' + str(len(goal_state)) + 'x' + str(len(goal_state[0])) + '-1 or ' + str(len(goal_state) * len(goal_state[0]) - 1) + ' Puzzle')

# Print the start state (To indicate start of searching....)
print_state(start_state, 'Start state')

next_states = Next_State_Generator(start_state, visited_states)
available_states.extend(next_states)
visited_states.append(start_state)

for next_state_x in next_states:
	next_state_x_str = str(next_state_x)
	camefrom_dict.update({next_state_x_str: present_state})

while available_states and present_state != goal_state:
	# Breadth first search -----------------------
	# Deque the first element from the available_states (Not inspected states)
	present_state = available_states[0]
	available_states = available_states[1:]
	# Add the present state to the visited state (inspected states list)
	visited_states.append(present_state)
	next_states = Next_State_Generator(present_state, visited_states)
	# Add the newly found states to the available_states list
	available_states.extend(next_states)

	# Add the currently discovered states to a dictionary with its previous states 
	# (all discovered states will have same previous state)
	# This step is necessary to generate the solution path to goal state
	for next_state_x in next_states:
		# Key of a dictionary should be a immutable object, hence it is converted to string
		next_state_x_str = str(next_state_x)
		camefrom_dict.update({next_state_x_str: present_state})

	# Count the number of iterations (For analysis purpose only)
	number_of_iterations += 1

tracking_state = copy.deepcopy(present_state)



# Print the solution if it was found
if(present_state == goal_state):
	print('Number of iterations of search = ' + str(number_of_iterations))

	# This while loop generates the solution path from end state to start state (Hence, reverse it later)
	while tracking_state != start_state:
		# Create the solution path (Back tracking to the start state)
		solution_path.append(camefrom_dict[str(tracking_state)])
		tracking_state = camefrom_dict[str(tracking_state)]

	# Reverse the path (Start state -> step before Goal state)
	solution_path.reverse()

	print('Number of steps to reach the goal state = ' + str(len(solution_path)))

	# Print the solution path
	for x in solution_path:
		print_state(x)

	# Print goal state
	print_state(goal_state)
else:
	print("It is impossible to reach the goal state " + str(number_of_iterations))