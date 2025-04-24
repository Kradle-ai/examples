###############################
### INIT_PARTICIPANT.MCFUNCTION
###############################

# do this when the initialization for each participant is long - also if you need to initialize multiple roles

# Clear inventory of each participant
clear @s

# Give multiple blocks to each participant
give @s minecraft:cobblestone 64
give @s minecraft:oak_planks 64
give @s minecraft:dirt 64
give @s minecraft:torch 64

# Give an iron sword to each participant
give @s minecraft:iron_sword 1