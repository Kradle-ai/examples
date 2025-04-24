##############################
### START_CHALLENGE.MCFUNCTION
##############################

# This is called at the start of the challenge

# DO NOT EDIT THIS PART

# Set up the scoreboard #
# Remove old objectives if they exist
scoreboard objectives remove game_score

# Create primary game_score objective and initialize it to 0
scoreboard objectives add game_score dummy
scoreboard players set @a game_score 0

# Display the game_score scoreboard
scoreboard objectives setdisplay sidebar game_score

# Initialize game state (0 = ongoing, 1 = over)
scoreboard players set game_state game_score 0

# EDIT THIS PART

# Set up a timer (optional)
# Create game_timer for tracking time (1200 ticks = 60 seconds)
scoreboard players set game_timer game_score 2400

# use in-game objectives
# e.g. count how many time players died
scoreboard objectives remove death_count
scoreboard objectives add death_count deathCount
scoreboard players set @a death_count 0

# SET UP THE WORLD

# Kill any existing zombies before starting the challenge
kill @e[type=zombie]

# Initialize participants with starting resources
execute as @a run function custom:init_participants

# Schedule zombie spawning in 60 seconds
# Clear any scheduled functions from previous runs
schedule clear custom:spawn_zombies
schedule function custom:spawn_zombies 60s

# Announce the challenge in chat
tellraw @a {"text": "Challenge starting! You have 60 seconds to build your cover before the wave of zombies come!", "color": "yellow"}
