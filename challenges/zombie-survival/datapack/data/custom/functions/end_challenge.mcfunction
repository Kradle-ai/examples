############################
### END_CHALLENGE.MCFUNCTION
############################

# This function is called when the game ends, only if the game is ongoing

# determine winners and losers
# winners need to have 1000000 points on the game_score objective
# losers are all players who do not have 1000000 points on the game_score objective

# EDIT THIS PART

# Kill all zombies
kill @e[type=zombie]

# Set the time to day
time set 0

# Award 1,000,000 points to successful players (those who survived)
execute as @a[gamemode=survival,scores={death_count=0}] run scoreboard players add @s game_score 1000000

# Display the winners
execute if entity @a[gamemode=survival,scores={death_count=0}] run say The winners are @a[gamemode=survival,scores={death_count=0}]!!
execute unless entity @a[gamemode=survival,scores={death_count=0}] run say There are no winners this time since all participants died!!

# Clear any scheduled functions since the game has ended
schedule clear custom:spawn_zombies

# IMPORTANT!! DO NOT EDIT THIS PART
# Mark the game as over
scoreboard players set game_state game_score 1