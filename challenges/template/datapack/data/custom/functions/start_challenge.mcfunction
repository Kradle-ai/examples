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
scoreboard players set game_timer game_score 1200

# use in-game objectives
# e.g. count how many time players died
# scoreboard objectives add death_count deathCount
# scoreboard players set @a death_count 0

# or how many pigs players have farmed
# scoreboard objectives add pigs_farmed minecraft.killed:minecraft.pig
# scoreboard players set @a pigs_farmed 0


# set initial conditions for participants
# e.g. give everyone who is not a spectator a wooden sword
# give @a[gamemode=survival] wooden_sword


say the game has started!!!