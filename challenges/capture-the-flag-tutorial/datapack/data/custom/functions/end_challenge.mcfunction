############################
### END_CHALLENGE.MCFUNCTION
############################

# This function is called when the game ends, only if the game is ongoing

# determine winners and losers
# winners need to have 1000000 points on the game_score objective
# losers are all players who do not have 1000000 points on the game_score objective

# EDIT THIS PART

# Award points to the winning player (player who captured the flag)
execute as @a[nbt={Inventory:[{id:"minecraft:red_banner"}]}] at @s if block ~ ~-1 ~ minecraft:blue_wool run scoreboard players add @s game_score 1000000

# Create victory effects for the winner
execute as @a[nbt={Inventory:[{id:"minecraft:red_banner"}]}] at @s if block ~ ~-1 ~ minecraft:blue_wool run function custom:victory_effects

# If time ran out (no winner)
execute if score game_timer game_score matches 0 run tellraw @a {"text":"Time's up! No one managed to capture the flag!!","color":"red"}

# Show everyone's final scores
tellraw @a {"text":"\nFinal Scores:","color":"white"}
execute as @a run tellraw @a [{"selector":"@s","color":"white"},{"text":": ","color":"white"},{"score":{"name":"@s","objective":"game_score"},"color":"green"}]

# Clear all players' inventories except spectators and watcher
execute as @a[gamemode=!spectator,name=!watcher] run clear @s

# IMPORTANT!! DO NOT EDIT THIS PART
# Mark the game as over
scoreboard players set game_state game_score 1