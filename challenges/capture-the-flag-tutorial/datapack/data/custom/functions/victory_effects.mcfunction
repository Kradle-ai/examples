##############################
### VICTORY_EFFECTS.MCFUNCTION
##############################

# Announce winner
tellraw @a [{"selector":"@s","color":"gold"},{"text":" has captured the flag and won the game!","color":"yellow"}]

# Create celebration effects at the victory location
particle minecraft:totem_of_undying ~ ~ ~ 0.5 0.5 0.5 0.1 100
particle minecraft:firework ~ ~ ~ 0.5 0.5 0.5 0.1 50
playsound entity.player.levelup master @a ~ ~ ~ 1 1