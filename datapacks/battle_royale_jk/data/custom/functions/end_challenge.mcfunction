# If there's exactly one player alive, they win
execute if score alive_players game_score matches 1 run tellraw @a [{"text":"Game Over! ","color":"gold"},{"selector":"@a[gamemode=survival]","color":"green"},{"text":" is the last player standing!","color":"gold"}]
execute if score alive_players game_score matches 1 run title @a title {"text":"Game Over!","color":"gold"}
execute if score alive_players game_score matches 1 run title @a subtitle [{"selector":"@a[gamemode=survival]","color":"green"},{"text":" Wins!","color":"gold"}]
execute if score alive_players game_score matches 1 run scoreboard players add @a[gamemode=survival] game_score 1000000

# If time ran out and multiple players are alive, nobody wins
execute if score game_timer game_score matches ..0 if score alive_players game_score matches 2.. run tellraw @a {"text":"Time's up! No winner since multiple players are still alive!","color":"red"}
execute if score game_timer game_score matches ..0 if score alive_players game_score matches 2.. run title @a title {"text":"Game Over!","color":"red"}
execute if score game_timer game_score matches ..0 if score alive_players game_score matches 2.. run title @a subtitle {"text":"No Winner!","color":"red"}

# If no players are alive, nobody wins
execute if score alive_players game_score matches 0 run tellraw @a {"text":"Game Over! No survivors!","color":"red"}
execute if score alive_players game_score matches 0 run title @a title {"text":"Game Over!","color":"red"}
execute if score alive_players game_score matches 0 run title @a subtitle {"text":"No Winner!","color":"red"}

# Set all players to spectator mode
gamemode spectator @a

# Set game as over (this should always be last)
scoreboard players set game_state game_score 1 