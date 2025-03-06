# Decrement timer if game is ongoing
execute if score game_state game_score matches 0 run scoreboard players remove game_timer game_score 1

# Display time remaining to players (once per second - every 20 ticks)
# Using modulo operation to check for displays every 20 ticks
execute if score game_timer game_score matches 1.. if score game_state game_score matches 0 run scoreboard players operation timer_mod game_score = game_timer game_score
execute if score game_timer game_score matches 1.. if score game_state game_score matches 0 run scoreboard players operation timer_mod game_score %= 20 game_score
execute if score game_timer game_score matches 1.. if score game_state game_score matches 0 if score timer_mod game_score matches 0 run function custom:display_time

# End game if timer runs out
execute if score game_timer game_score matches ..0 run function custom:end_challenge