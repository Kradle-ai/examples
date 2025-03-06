# Gradually shrink the play area by applying damage to players outside a boundary
# Start shrinking after 1 minute (1200 ticks)
execute if score game_timer game_score matches ..2400 run effect give @a[distance=65..] wither 1 1 true

# After 2 minutes, shrink further
execute if score game_timer game_score matches ..1200 run effect give @a[distance=40..] wither 1 2 true 

# Final minute, very small play area
execute if score game_timer game_score matches ..600 run effect give @a[distance=20..] wither 1 3 true 