from typing import Any
from kradle import Observation


def format_observation(observation: Observation) -> str:
    """Converts observation object to a string for the LLM prompt."""

    # Let's get everything in our inventory
    inventory_summary = _format_list([f"{count} {name}" for name, count in observation.inventory.items()])

    # Return string with everything the LLM needs to know about the state of the game
    result = [
        f"Event received: {_format_value(observation.event)}",
        f"Command Output:\n{_format_value(observation.output)}",
        f"Position: {_format_value(observation.position)}",
    ]

    if observation.chat_messages:
        result.append(f"Latest Chat: {_format_value(observation.chat_messages)}")

    result.extend(
        [
            f"Visible Players: {_format_list(observation.players)}",
            f"Visible Blocks: {_format_list(observation.blocks)}",
            f"Visible Entities: {_format_list(observation.entities)}",
            f"Inventory: {inventory_summary}",
            f"Health: {observation.health * 100}/100",
        ]
    )

    return "\n\n".join(result)


def _format_value(value: Any) -> Any:
    return value if value else "None"


def _format_list(items: list[str]) -> str:
    return ", ".join(items) if items else "None"
