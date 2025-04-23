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


# SET UP THE WORLD

# Set the time to day
time set 0

# Clear all red and blue wool blocks within a 4-chunk radius (64x64 blocks) and replace them with grass
fill -559 3 2912 -431 3 3040 minecraft:grass_block replace minecraft:red_wool
fill -559 3 2912 -431 3 3040 minecraft:grass_block replace minecraft:blue_wool

# Remove all banners within a 4-chunk radius
fill -559 3 2912 -431 3 3040 minecraft:air replace minecraft:red_banner
fill -559 3 2912 -431 3 3040 minecraft:air replace minecraft:blue_banner

# Prevent mob spawning globally
gamerule doMobSpawning false

# Kill all existing mobs to start with a clean state
kill @e[type=!player]

# Create the blue base at spawn (5x5 square with a blue banner)
fill -497 3 2974 -493 3 2978 minecraft:blue_wool replace
setblock -495 4 2976 minecraft:blue_banner{Patterns:[{Pattern:"cs",Color:4},{Pattern:"bts",Color:11}]} replace

# Create the red base 42 blocks away from spawn in negative Z direction (5x5 square with a red banner)
fill -497 3 2937 -493 3 2933 minecraft:red_wool replace
setblock -495 4 2935 minecraft:red_banner{Patterns:[{Pattern:"cs",Color:1},{Pattern:"bts",Color:14}]} replace

# SET UP THE PARTICIPANTS

# Clear inventory
clear @a[name=!"watcher"]

# Set gamemode to adventure
gamemode survival @a[name=!"watcher"]

# Teleport to spawn point
tp @a[name=!"watcher"] -495 4 2976

# Fill hunger and saturation
effect give @a[name=!"watcher"] saturation 1 255 true



# Game start announcements
tellraw @a {"text": "Capture the Flag challenge starting!", "color": "yellow"}
tellraw @a {"text": "The enemy's red flag is placed further ahead of your spawn. Break it and bring it back to your base to win!", "color": "green"}
tellraw @a {"text": "Break the enemy's red flag with the provided pickaxe and return it to your base!", "color": "red"}