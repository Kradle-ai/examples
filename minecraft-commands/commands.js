module.exports = 
{
  skills: {
    'skills.activateNearestBlock': '/**\n' +
      '         * Activate the nearest block of the given type.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} type, the type of block to activate.\n' +
      '         * @returns {Promise<boolean>} true if the block was activated, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.activateNearestBlock(bot, "lever");\n' +
      '         * **/\n',
    'skills.attackEntity': '/**\n' +
      '         * Attack mob of the given type.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {Entity} entity, the entity to attack.\n' +
      '         * @returns {Promise<boolean>} true if the entity was attacked, false if interrupted\n' +
      '         * @example\n' +
      '         * await skills.attackEntity(bot, entity);\n' +
      '         **/\n',
    'skills.attackNearest': '/**\n' +
      '         * Attack mob of the given type.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} mobType, the type of mob to attack.\n' +
      '         * @param {boolean} kill, whether or not to continue attacking until the mob is dead. Defaults to true.\n' +
      '         * @returns {Promise<boolean>} true if the mob was attacked, false if the mob type was not found.\n' +
      '         * @example\n' +
      '         * await skills.attackNearest(bot, "zombie", true);\n' +
      '         **/\n',
    'skills.avoidEnemies': '/**\n' +
      '         * Move a given distance away from all nearby enemy mobs.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {number} distance, the distance to move away.\n' +
      '         * @returns {Promise<boolean>} true if the bot moved away, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.avoidEnemies(bot, 8);\n' +
      '         **/\n',
    'skills.breakBlockAt': '/**\n' +
      "         * Break the block at the given position. Will use the bot's equipped item.\n" +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {number} x, the x coordinate of the block to break.\n' +
      '         * @param {number} y, the y coordinate of the block to break.\n' +
      '         * @param {number} z, the z coordinate of the block to break.\n' +
      '         * @returns {Promise<boolean>} true if the block was broken, false otherwise.\n' +
      '         * @example\n' +
      '         * let position = world.getPosition(bot);\n' +
      '         * await skills.breakBlockAt(bot, position.x, position.y - 1, position.x);\n' +
      '         **/\n',
    'skills.clearNearestFurnace': '/**\n' +
      '         * Clears the nearest furnace of all items.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @returns {Promise<boolean>} true if the furnace was cleared, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.clearNearestFurnace(bot);\n' +
      '         **/\n',
    'skills.collectBlock': '/**\n' +
      '         * Collect one of the given block type.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} blockType, the type of block to collect.\n' +
      '         * @param {number} num, the number of blocks to collect. Defaults to 1.\n' +
      '         * @returns {Promise<boolean>} true if the block was collected, false if the block type was not found.\n' +
      '         * @example\n' +
      '         * await skills.collectBlock(bot, "oak_log");\n' +
      '         **/\n',
    'skills.consume': '/**\n' +
      '         * Eat/drink the given item.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} itemName, the item to eat/drink.\n' +
      '         * @returns {Promise<boolean>} true if the item was eaten, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.eat(bot, "apple");\n' +
      '         **/\n',
    'skills.craftRecipe': '/**\n' +
      '         * Attempt to craft the given item name from a recipe. May craft many items.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} itemName, the item name to craft.\n' +
      '         * @returns {Promise<boolean>} true if the recipe was crafted, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.craftRecipe(bot, "stick");\n' +
      '         **/\n',
    'skills.defendSelf': '/**\n' +
      '         * Defend yourself from all nearby hostile mobs until there are no more.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {number} range, the range to look for mobs. Defaults to 8.\n' +
      '         * @returns {Promise<boolean>} true if the bot found any enemies and has killed them, false if no entities were found.\n' +
      '         * @example\n' +
      '         * await skills.defendSelf(bot);\n' +
      '         * **/\n',
    'skills.discard': '/**\n' +
      '         * Discard the given item.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} itemName, the item or block name to discard.\n' +
      '         * @param {number} num, the number of items to discard. Defaults to -1, which discards all items.\n' +
      '         * @returns {Promise<boolean>} true if the item was discarded, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.discard(bot, "oak_log");\n' +
      '         **/\n',
    'skills.equip': '/**\n' +
      '         * Equip the given item to the proper body part, like tools or armor.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} itemName, the item or block name to equip.\n' +
      '         * @returns {Promise<boolean>} true if the item was equipped, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.equip(bot, "iron_pickaxe");\n' +
      '         **/\n',
    'skills.followPlayer': '/**\n' +
      '         * Follow the given player endlessly. Will not return until the code is manually stopped.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} username, the username of the player to follow.\n' +
      '         * @returns {Promise<boolean>} true if the player was found, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.followPlayer(bot, "player");\n' +
      '         **/\n',
    'skills.giveToPlayer': '/**\n' +
      '         * Give one of the specified item to the specified player\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} itemType, the name of the item to give.\n' +
      '         * @param {string} username, the username of the player to give the item to.\n' +
      '         * @param {number} num, the number of items to give. Defaults to 1.\n' +
      '         * @returns {Promise<boolean>} true if the item was given, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.giveToPlayer(bot, "oak_log", "player1");\n' +
      '         **/\n',
    'skills.goToBed': '/**\n' +
      '         * Sleep in the nearest bed.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @returns {Promise<boolean>} true if the bed was found, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.goToBed(bot);\n' +
      '         **/\n',
    'skills.goToNearestBlock': '/**\n' +
      '         * Navigate to the nearest block of the given type.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} blockType, the type of block to navigate to.\n' +
      '         * @param {number} min_distance, the distance to keep from the block. Defaults to 2.\n' +
      '         * @param {number} range, the range to look for the block. Defaults to 64.\n' +
      '         * @returns {Promise<boolean>} true if the block was reached, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.goToNearestBlock(bot, "oak_log", 64, 2);\n' +
      '         * **/\n',
    'skills.goToNearestEntity': '/**\n' +
      '         * Navigate to the nearest entity of the given type.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} entityType, the type of entity to navigate to.\n' +
      '         * @param {number} min_distance, the distance to keep from the entity. Defaults to 2.\n' +
      '         * @param {number} range, the range to look for the entity. Defaults to 64.\n' +
      '         * @returns {Promise<boolean>} true if the entity was reached, false otherwise.\n' +
      '         **/\n',
    'skills.goToPlayer': '/**\n' +
      '         * Navigate to the given player.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} username, the username of the player to navigate to.\n' +
      '         * @param {number} distance, the goal distance to the player.\n' +
      '         * @returns {Promise<boolean>} true if the player was found, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.goToPlayer(bot, "player");\n' +
      '         **/\n',
    'skills.goToPosition': '/**\n' +
      '         * Navigate to the given position.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      "         * @param {number} x, the x coordinate to navigate to. If null, the bot's current x coordinate will be used.\n" +
      "         * @param {number} y, the y coordinate to navigate to. If null, the bot's current y coordinate will be used.\n" +
      "         * @param {number} z, the z coordinate to navigate to. If null, the bot's current z coordinate will be used.\n" +
      '         * @param {number} distance, the distance to keep from the position. Defaults to 2.\n' +
      '         * @returns {Promise<boolean>} true if the position was reached, false otherwise.\n' +
      '         * @example\n' +
      '         * let position = world.world.getNearestBlock(bot, "oak_log", 64).position;\n' +
      '         * await skills.goToPosition(bot, position.x, position.y, position.x + 20);\n' +
      '         **/\n',
    'skills.moveAway': '/**\n' +
      '         * Move away from current position in any direction.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {number} distance, the distance to move away.\n' +
      '         * @returns {Promise<boolean>} true if the bot moved away, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.moveAway(bot, 8);\n' +
      '         **/\n',
    'skills.moveAwayFromEntity': '/**\n' +
      '         * Move away from the given entity.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {Entity} entity, the entity to move away from.\n' +
      '         * @param {number} distance, the distance to move away.\n' +
      '         * @returns {Promise<boolean>} true if the bot moved away, false otherwise.\n' +
      '         **/\n',
    'skills.pickupNearbyItems': '/**\n' +
      '         * Pick up all nearby items.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @returns {Promise<boolean>} true if the items were picked up, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.pickupNearbyItems(bot);\n' +
      '         **/\n',
    'skills.placeBlock': '/**\n' +
      '         * Place the given block type at the given position. It will build off from any adjacent blocks. Will fail if there is a block in the way or nothing to build off of.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} blockType, the type of block to place.\n' +
      '         * @param {number} x, the x coordinate of the block to place.\n' +
      '         * @param {number} y, the y coordinate of the block to place.\n' +
      '         * @param {number} z, the z coordinate of the block to place.\n' +
      "         * @param {string} placeOn, the preferred side of the block to place on. Can be 'top', 'bottom', 'north', 'south', 'east', 'west', or 'side'. Defaults to bottom. Will place on first available side if not possible.\n" +
      '         * @param {boolean} dontCheat, overrides cheat mode to place the block normally. Defaults to false.\n' +
      '         * @returns {Promise<boolean>} true if the block was placed, false otherwise.\n' +
      '         * @example\n' +
      '         * let p = world.getPosition(bot);\n' +
      '         * await skills.placeBlock(bot, "oak_log", p.x + 2, p.y, p.x);\n' +
      `         * await skills.placeBlock(bot, "torch", p.x + 1, p.y, p.x, 'side');\n` +
      '         **/\n',
    'skills.putInChest': '/**\n' +
      '         * Put the given item in the nearest chest.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} itemName, the item or block name to put in the chest.\n' +
      '         * @param {number} num, the number of items to put in the chest. Defaults to -1, which puts all items.\n' +
      '         * @returns {Promise<boolean>} true if the item was put in the chest, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.putInChest(bot, "oak_log");\n' +
      '         **/\n',
    'skills.smeltItem': '/**\n' +
      '         * Puts 1 coal in furnace and smelts the given item name, waits until the furnace runs out of fuel or input items.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} itemName, the item name to smelt. Ores must contain "raw" like raw_iron.\n' +
      '         * @param {number} num, the number of items to smelt. Defaults to 1.\n' +
      '         * @returns {Promise<boolean>} true if the item was smelted, false otherwise. Fail\n' +
      '         * @example\n' +
      '         * await skills.smeltItem(bot, "raw_iron");\n' +
      '         * await skills.smeltItem(bot, "beef");\n' +
      '         **/\n',
    'skills.stay': '/**\n' +
      '         * Stay in the current position until interrupted. Disables all modes.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {number} seconds, the number of seconds to stay. Defaults to 30. -1 for indefinite.\n' +
      '         * @returns {Promise<boolean>} true if the bot stayed, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.stay(bot);\n' +
      '         **/\n',
    'skills.summonMobType': '/**\n' +
      '         * Summon mobs of the given type.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} mobType, the type of mob to summon.\n' +
      '         * @param {number} num, the number of mobs to summon. Defaults to 1.\n' +
      '         * @returns {Promise<boolean>} true if the mobs were summoned, false if the mob type was not found.\n' +
      '         * @example\n' +
      '         * await skills.summonMobType(bot, "zombie", 10);\n' +
      '         **/\n',
    'skills.takeFromChest': '/**\n' +
      '         * Take the given item from the nearest chest.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {string} itemName, the item or block name to take from the chest.\n' +
      '         * @param {number} num, the number of items to take from the chest. Defaults to -1, which takes all items.\n' +
      '         * @returns {Promise<boolean>} true if the item was taken from the chest, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.takeFromChest(bot, "oak_log");\n' +
      '         * **/\n',
    'skills.tillAndSow': '/**\n' +
      '         * Till the ground at the given position and plant the given seed type.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {number} x, the x coordinate to till.\n' +
      '         * @param {number} y, the y coordinate to till.\n' +
      '         * @param {number} z, the z coordinate to till.\n' +
      '         * @param {string} plantType, the type of plant to plant. Defaults to none, which will only till the ground.\n' +
      '         * @returns {Promise<boolean>} true if the ground was tilled, false otherwise.\n' +
      '         * @example\n' +
      '         * let position = world.getPosition(bot);\n' +
      '         * await skills.till(bot, position.x, position.y - 1, position.x);\n' +
      '         **/\n',
    'skills.useDoor': '/**\n' +
      '         * Use the door at the given position.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @param {Vec3} door_pos, the position of the door to use. If null, the nearest door will be used.\n' +
      '         * @returns {Promise<boolean>} true if the door was used, false otherwise.\n' +
      '         * @example\n' +
      '         * let door = world.getNearestBlock(bot, "oak_door", 16).position;\n' +
      '         * await skills.useDoor(bot, door);\n' +
      '         **/\n',
    'skills.viewChest': '/**\n' +
      '         * View the contents of the nearest chest.\n' +
      '         * @param {MinecraftBot} bot, reference to the minecraft bot.\n' +
      '         * @returns {Promise<boolean>} true if the chest was viewed, false otherwise.\n' +
      '         * @example\n' +
      '         * await skills.viewChest(bot);\n' +
      '         * **/\n'
  },
  world: {
    'world.getBiomeName': '/**\n' +
      '     * Get the name of the biome the bot is in.\n' +
      '     * @param {Bot} bot - The bot to get the biome for.\n' +
      '     * @returns {string} - The name of the biome.\n' +
      '     * @example\n' +
      '     * let biome = world.getBiomeName(bot);\n' +
      '     **/\n',
    'world.getCraftableItems': '/**\n' +
      "     * Get a list of all items that can be crafted with the bot's current inventory.\n" +
      '     * @param {Bot} bot - The bot to get the craftable items for.\n' +
      '     * @returns {string[]} - A list of all items that can be crafted.\n' +
      '     * @example\n' +
      '     * let craftableItems = world.getCraftableItems(bot);\n' +
      '     **/\n',
    'world.getInventoryCounts': '/**\n' +
      "     * Get an object representing the bot's inventory.\n" +
      '     * @param {Bot} bot - The bot to get the inventory for.\n' +
      '     * @returns {object} - An object with item names as keys and counts as values.\n' +
      '     * @example\n' +
      '     * let inventory = world.getInventoryCounts(bot);\n' +
      "     * let oakLogCount = inventory['oak_log'];\n" +
      "     * let hasWoodenPickaxe = inventory['wooden_pickaxe'] > 0;\n" +
      '     **/\n',
    'world.getNearbyBlockTypes': '/**\n' +
      '     * Get a list of all nearby block names.\n' +
      '     * @param {Bot} bot - The bot to get nearby blocks for.\n' +
      '     * @param {number} distance - The maximum distance to search, default 16.\n' +
      '     * @returns {string[]} - A list of all nearby blocks.\n' +
      '     * @example\n' +
      '     * let blocks = world.getNearbyBlockTypes(bot);\n' +
      '     **/\n',
    'world.getNearbyEntityTypes': '/**\n' +
      '     * Get a list of all nearby mob types.\n' +
      '     * @param {Bot} bot - The bot to get nearby mobs for.\n' +
      '     * @returns {string[]} - A list of all nearby mobs.\n' +
      '     * @example\n' +
      '     * let mobs = world.getNearbyEntityTypes(bot);\n' +
      '     **/\n',
    'world.getNearbyPlayerNames': '/**\n' +
      '     * Get a list of all nearby player names.\n' +
      '     * @param {Bot} bot - The bot to get nearby players for.\n' +
      '     * @returns {string[]} - A list of all nearby players.\n' +
      '     * @example\n' +
      '     * let players = world.getNearbyPlayerNames(bot);\n' +
      '     **/\n',
    'world.getNearestBlock': '/**\n' +
      '     * Get the nearest block of the given type.\n' +
      '     * @param {Bot} bot - The bot to get the nearest block for.\n' +
      '     * @param {string} block_type - The name of the block to search for.\n' +
      '     * @param {number} distance - The maximum distance to search, default 16.\n' +
      '     * @returns {Block} - The nearest block of the given type.\n' +
      '     * @example\n' +
      "     * let coalBlock = world.getNearestBlock(bot, 'coal_ore', 16);\n" +
      '     **/\n',
    'world.getNearestBlocks': '/**\n' +
      '     * Get a list of the nearest blocks of the given types.\n' +
      '     * @param {Bot} bot - The bot to get the nearest block for.\n' +
      '     * @param {string[]} block_types - The names of the blocks to search for.\n' +
      '     * @param {number} distance - The maximum distance to search, default 16.\n' +
      '     * @param {number} count - The maximum number of blocks to find, default 10000.\n' +
      '     * @returns {Block[]} - The nearest blocks of the given type.\n' +
      '     * @example\n' +
      "     * let woodBlocks = world.getNearestBlocks(bot, ['oak_log', 'birch_log'], 16, 1);\n" +
      '     **/\n',
    'world.getNearestFreeSpace': '/**\n' +
      '     * Get the nearest empty space with solid blocks beneath it of the given size.\n' +
      '     * @param {Bot} bot - The bot to get the nearest free space for.\n' +
      '     * @param {number} size - The (size x size) of the space to find, default 1.\n' +
      '     * @param {number} distance - The maximum distance to search, default 8.\n' +
      '     * @returns {Vec3} - The south west corner position of the nearest free space.\n' +
      '     * @example\n' +
      '     * let position = world.getNearestFreeSpace(bot, 1, 8);\n' +
      '     **/\n',
    'world.getPosition': '/**\n' +
      '     * Get your position in the world (Note that y is vertical).\n' +
      '     * @param {Bot} bot - The bot to get the position for.\n' +
      '     * @returns {Vec3} - An object with x, y, and x attributes representing the position of the bot.\n' +
      '     * @example\n' +
      '     * let position = world.getPosition(bot);\n' +
      '     * let x = position.x;\n' +
      '     **/\n',
    'world.isClearPath': '/**\n' +
      '         * Check if there is a path to the target that requires no digging or placing blocks.\n' +
      '         * @param {Bot} bot - The bot to get the path for.\n' +
      '         * @param {Entity} target - The target to path to.\n' +
      '         * @returns {boolean} - True if there is a clear path, false otherwise.\n' +
      '         **/\n'
  }
}
