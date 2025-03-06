# Calculate remaining time in seconds
scoreboard players operation seconds game_score = game_timer game_score
scoreboard players operation seconds game_score /= 20 game_score

# Display time remaining
title @a actionbar [{"text":"Time Remaining: ","color":"gold"},{"score":{"name":"seconds","objective":"game_score"},"color":"yellow"},{"text":" seconds","color":"gold"}]

# Special warnings at key time points
execute if score seconds game_score matches 60 run tellraw @a {"text":"60 seconds remaining!","color":"yellow"}
execute if score seconds game_score matches 30 run tellraw @a {"text":"30 seconds remaining!","color":"gold"}
execute if score seconds game_score matches 10 run tellraw @a {"text":"10 seconds remaining!","color":"red"}
execute if score seconds game_score matches 5 run tellraw @a {"text":"5","color":"red","bold":true}
execute if score seconds game_score matches 4 run tellraw @a {"text":"4","color":"red","bold":true}
execute if score seconds game_score matches 3 run tellraw @a {"text":"3","color":"red","bold":true}
execute if score seconds game_score matches 2 run tellraw @a {"text":"2","color":"red","bold":true}
execute if score seconds game_score matches 1 run tellraw @a {"text":"1","color":"red","bold":true} 