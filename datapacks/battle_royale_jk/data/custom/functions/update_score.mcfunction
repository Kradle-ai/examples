# In this Battle Royale, no specific score to update during gameplay
# The main score is determined at the end based on survival status

# Debug - show alive players count
execute if score game_state game_score matches 0 run title @a actionbar [{"text":"Players alive: ","color":"yellow"},{"score":{"name":"alive_players","objective":"game_score"},"color":"green"}] 