############################
### END_CHALLENGE.MCFUNCTION
############################

# This function is called when the game ends, only if the game is ongoing

# determine winners and losers
# winners need to have 1000000 points on the game_score objective
# losers are all players who do not have 1000000 points on the game_score objective

# EDIT THIS PART

# E.g. If there's exactly one player alive, they win
# execute if score alive_players game_score matches 1 run scoreboard players add @a[gamemode=survival] game_score 1000000
# but if time ran out and multiple players are alive, nobody wins
# execute if score alive_players game_score matches 2.. run tellraw @a {"text":"No winner!","color":"red"} 

# E.g. if a player has farmed 2 pigs, they win
# execute as @p[scores={pigs_farmed=2..}] run scoreboard players add @s game_score 1000000

# Declare the winner
# if a player has 1000000 points, they win
execute as @a[scores={game_score=1000000..}] run say The winner is @s!

# IMPORTANT!! DO NOT EDIT THIS PART
# Mark the game as over
scoreboard players set game_state game_score 1