######################
### ON_TICK.MCFUNCTION
######################
# this runs on each tick of the game, only if the game is ongoing

# EDIT THIS PART

# Timer functions
# Decrement the game timer if it's greater than 0
execute if score game_timer game_score matches 1.. run scoreboard players remove game_timer game_score 1

# End the challenge when the game timer reaches 0 (players survive the entire duration)
execute if score game_timer game_score matches 0 run function custom:call_end_challenge

# End the challenge if any player dies (failure state)
execute unless entity @a[gamemode=survival,scores={death_count=0}] run function custom:call_end_challenge