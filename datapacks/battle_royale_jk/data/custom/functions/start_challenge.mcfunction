# Set players' max health
attribute @a minecraft:generic.max_health base set 20

# Make sure everyone has proper game mode
gamemode survival @a 

# Initialize objectives
scoreboard objectives add game_score dummy
scoreboard players set @a game_score 0
scoreboard players set game_state game_score 0
# Set timer to 3 minutes (3600 ticks = 3 minutes at 20 ticks per second)
scoreboard players set game_timer game_score 3600

# Store the number of initial participants
execute store result score initial_players game_score if entity @a

# Set everyone to survival mode
gamemode survival @a

# Clear all player inventories
clear @a

# Give each player basic survival gear
give @a stone_sword 1
give @a bow 1
give @a arrow 16
give @a cooked_beef 5

# Spread players in a 100x100 area
spreadplayers 0 0 25 50 false @a

# Announce game start
title @a title {"text":"Battle Royale", "color":"red"}
title @a subtitle {"text":"Last player standing wins!", "color":"gold"}
tellraw @a {"text":"Battle Royale has begun! Last player standing wins. You have 3 minutes!", "color":"yellow"} 