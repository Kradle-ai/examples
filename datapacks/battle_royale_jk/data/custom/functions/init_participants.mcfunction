# No specific roles in this challenge, but we'll set all players to full health
effect give @a instant_health 1 10 true

# Give all players a small speed boost for the start
effect give @a speed 30 1 true

# Set players' max health
attribute @a minecraft:generic.max_health base set 20

# Make sure everyone has proper game mode
gamemode survival @a 