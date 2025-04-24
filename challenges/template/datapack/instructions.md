## This is an instruction set to create a datapack for a Minecraft game.

Code will have to be written in mcfunction files.

## Initial Structure

When creating a datapack, start with copying the `template` datapack, which has the following structure:
```
📦 datapack
 ┣ 📂 data
 ┃ ┗ 📂 custom
 ┃ ┃ ┣ 📂 functions
 ┃ ┃   ┣ 📜 start_challenge.mcfunction
 ┃ ┃   ┣ 📜 on_tick.mcfunction
 ┃ ┃   ┣ 📜 end_challenge.mcfunction
 ┃ ┃   ┣ 📜 call_on_tick.mcfunction
 ┃ ┃   ┗ 📜 call_on_challenge.mcfunction
 ┃ ┗ 📂 minecraft
 ┃     ┗ 📂 tags
 ┃       ┗ 📂 functions
 ┃         ┗ 📜 tick.json
 ┗ 📜 pack.mcmeta
```

## general principle
- Kradle runs a minecraft server with your datapack loaded
- Kradle uses the `game_score` scoreboard to keep track of the state of the run and determine winners and loosers at the end. A score of 1,000,000 or more is a winning score, a score of less than that number if a losing score. A special entry in the `game_score` scoreboard named `game_state` determines whether the run is still ongoing or not. 0 = ongoing, 1 = finished
- when the run starts, the `start_challenge` function gets called. it sets up the main `game_score` scoreboard, as well as the game timer (optional), and sets up various initial conditions e.g. place certain items in the world, equip players with certain items, place them in certain positions...
- at every tick, the `on_tick` function gets called. it decrements the timer, and checks for game ending conditions. If these conditions are met, it calls the `call_end_challenge` function.
- when the ending conditions are met, the `end_challenge` gets called (only once). Winners and loosers are determined and their `game_score` updated accordingly. Then the `game_state` key gets set to 1, and Kradle ends the run.


## Participant roles
- in some challenges, participants can have specific roles, e.g. `healer` and `wizard`. Kradle allocates roles to agents by tagging them with that role. This is done before the `start_challenge` function is called.
- if you want to select all participants with a given role, you can use the `tag=ROLE_NAME` selector. E.g. `give @a[tag=fighter] wooden_sword` gives all players how are a `fighter` a wooden sword.
- if you want to determine winning conditions by role, you can also use the tag selector, e.g. `execute as @p[scores={pigs_farmed=2..,tag=fighter}] run scoreboard players add @s game_score 1000000` declares all players who are `fighter` successful if they farmed 2 pigs.
```