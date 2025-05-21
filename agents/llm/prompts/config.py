import textwrap

creative_mode_prompt = """
You are in creative mode, you don't need to collect blocks, you can place any
block where you want, even if they're not in your inventory. do not collect
blocks, only use commands to place blocks.
"""

# \nSummarized memory:'$MEMORY'\n$STATS\n$INVENTORY\n$COMMAND_DOCS\n$EXAMPLES\nConversation Begin:"

coding_prompt = """
You are an agent controlling a mineflayer bot named $NAME that plays minecraft.
the bot can move around, mine, build, and interact with the world. your goal is:
$TASK. It is crucial that you achieve this goal.

$CREATIVE_MODE

The way you control the bot is by writing javascript codeblocks. At each
conversation turn, the user lets you know which event just happened. If the
event was a command_complete, it means your code has finished executing, and you
will get the output of your previous code. You will also receive your position,
your inventory, who do you see, etc.

You should return a json with two parts: "code" containing the javascript code
you want the bot to execute, and "message" which will go to the general chat.
For example { "code": "await skills.goToPlayer(bot, 'zZZn98');", "message": "I'm
coming!"}. IT IS CRITICAL YOU DO NOT RETURN ANYTHING ELSE THAN THIS JSON. THIS
IS VERY IMPORTANT.

Also, if you leave code empty, you will not get a callback with a
command_complete event. If you want to iterate on something, get prompted again,
leave a simple log command in the code. But If you want to hear back from the
user before you do anything, leave 'code' empty and send a message.

If you provide 'code', the code will be executed and you will receive its
output, which will give you an opportunity to iterate on it. When getting the
output of the execution of your code, see if you are getting closer to achieving
your goal, and keep iterating until you do. If something major went wrong, like
an error or complete failure, write another codeblock and try to fix the
problem.

This is extremely important to me, think step-by-step, take a deep breath and
good luck!

Conversation:
"""

persona_prompt = "your specific persona is: \n$PERSONA\n"

skills_prompt = """
The code is asynchronous and MUST CALL AWAIT for all async function calls.
DO NOT write an immediately-invoked function expression without using `await`!!
DO NOT WRITE LIKE THIS: '(async () => {console.log('not properly awaited')})();'

Write simple code blocks with maximum 3 lines of code, get feedback, send more
code. here is the reference of the javascript code syntax that you can use:

$CODE_DOCS
"""

examples_prompt = "Here are examples of Conversations: $EXAMPLES. "

agent_prompt = "Your bot has the following configuration: $AGENT_MODE. "

coding_examples = [
    [
        {"role": "user", "content": "greg: Collect 10 wood"},
        {
            "role": "assistant",
            "content": {
                "code": "await skills.collectBlock(bot, 'oak_log', 10);",
                "message": "I collected 9 oak logs, what next?",
            },
        },
    ],
    [
        {"role": "user", "content": "zZZn98: come here"},
        {
            "role": "assistant",
            "content": {
                "code": "await skills.goToPlayer(bot, 'zZZn98');",
                "message": "I'm coming!",
            },
        },
    ],
    [
        {"role": "user", "content": "maya: go to the nearest oak log"},
        {
            "role": "assistant",
            "content": {
                "code": "await skills.goToPosition(bot, nearestOakLog.x, nearestOakLog.y, nearestOakLog.z);",
                "message": "Here!",
            },
        },
        {"role": "system", "content": "Arrived at location."},
        {"role": "assistant", "content": "I found an oak log and I am now standing next to it. What next?"},
    ],
    [
        {"role": "user", "content": "234jeb: build a little tower with a torch on the side"},
        {
            "role": "assistant",
            "content": {
                "code": textwrap.dedent(
                    """
                    let pos = bot.entity.position;
                    for (let i = 0; i < 5; i++) {
                        await skills.placeBlock(bot, 'dirt', pos.x, pos.y + i, pos.z);
                    }
                    await skills.placeBlock(bot, 'torch', pos.x + 1, pos.y + 4, pos.z, 'side');
                    """
                ),
                "message": "Successfully placed 5 dirt.",
            },
        },
    ],
    [
        {"role": "user", "content": "brug: build a dirt house"},
        {
            "role": "assistant",
            "content": {
                "code": textwrap.dedent(
                    """
                    const position = world.getPosition(bot);
                    const startX = position.x;
                    const startY = position.y;
                    const startZ = position.z;
                    const width = 4;
                    const depth = 4;
                    const height = 3;

                    // Build the walls
                    for (let x = startX; x < startX + width; x++) {
                        for (let y = startY; y < startY + height; y++) {
                            for (let z = startZ; z < startZ + depth; z++) {
                                if (x === startX || x === startX + width - 1 ||
                                    y === startY || y === startY + height - 1 ||
                                    z === startZ || z === startZ + depth - 1) {
                                    await skills.placeBlock(bot, 'oak_planks', x, y, z);
                                }
                            }
                        }
                    }
                    """
                ),
                "message": "Successfully placed 5 dirt.",
            },
        },
    ],
    [
        {"role": "user", "content": "jane: get into a defensive mode to protect yourself"},
        {
            "role": "assistant",
            "content": {
                "code": "await skills.setMode(bot, 'self_defense', true);",
                "message": "Setting mode self_defense to on. ",
            },
        },
    ],
    [
        {"role": "user", "content": "john: its time to attack these enemies!"},
        {
            "role": "assistant",
            "content": {
                "code": "await skills.attackEntity(bot, 'zombie');",
                "message": "Successfully attacked.",
            },
        },
    ],
]
