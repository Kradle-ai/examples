# Count alive players
execute store result score alive_players game_score if entity @a[gamemode=survival]

# Announce each death
execute as @a[scores={death_count=1..}] run tellraw @a [{"selector":"@s","color":"red"},{"text":" has been eliminated!","color":"gold"}]
execute as @a[scores={death_count=1..}] run scoreboard players set @s death_count 0
execute as @a[gamemode=!survival,gamemode=!spectator] run gamemode spectator @s

# End game if only one player remains
execute if score alive_players game_score matches ..1 if score game_state game_score matches 0 run function custom:end_challenge 