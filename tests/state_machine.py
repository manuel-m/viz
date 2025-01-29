from enum import Enum


class Event(Enum):
    REACH = 0
    UNREACH = 1
    SYNC = 2
    UNSYNC = 3


transition_matrix = {
    #        REACH   UNREACH  SYNC   UNSYNC
    "_1_1": ("R1_1", "U1U1", "R1S1", "_1U1"), ###
    "U1_1": ("R1_1", "U1U1", "R0S1", "U1U1"),
    "U1U1": ("R1U1", "U1U1", "R0S1", "U1U1"),
    "_1U1": ("R1U1", "U1U1", "R1S1", "_1U1"),
    "R1_1": ("R1_1", "U1U1", "R1S1", "R1U1"),
    "R1U1": ("R1U1", "U1U1", "R1S1", "R1U1"),
    "R0S1": ("R1S1", "U1U1", "R1S1", "R0U1"),
    "R1S1": ("R1S1", "U1U1", "R1S1", "R1U1"), ###
}


def get_next_state(current: str, event: Event) -> str:
    """Returns the next state based on the current state and triggered event."""
    if current in transition_matrix:
        return transition_matrix[current][event.value]  # Use Enum index
    else:
        raise ValueError(f"Unknown state: {current}")


current = "U1U1"
event = Event.SYNC  

next_state = get_next_state(current, event)
print(f"After event {event.name}, the next state is: {next_state}")
