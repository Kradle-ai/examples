############################
### SPAWN_ZOMBIES.MCFUNCTION
############################

# Announce to players that zombies are coming
tellraw @a {"text": "Time's up! Here come the zombies!", "color": "red"}

# Set the time to night so that zombies don't catch on fire
time set night

# Spawn 8 zombies 10 blocks away from the player (X, Y, Z)
# For runs for closest participant to watcher with @p
execute at @p run summon zombie ~10 ~ ~
execute at @p run summon zombie ~-10 ~ ~
execute at @p run summon zombie ~ ~ ~-10
execute at @p run summon zombie ~ ~ ~10

execute at @p run summon zombie ~10 ~ ~5
execute at @p run summon zombie ~-10 ~ ~-5
execute at @p run summon zombie ~-5 ~ ~-10
execute at @p run summon zombie ~5 ~ ~10
