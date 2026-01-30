import logging
from enum import Enum, auto

logger = logging.getLogger(__name__)


class State(Enum):
    FIND_RED_ICONS = auto()
    CLICK_RED_ICON = auto()
    CHECK_UNLOCK = auto()
    SEARCH_UPGRADE_STATION = auto()
    HOLD_UPGRADE_STATION = auto()
    OPEN_BOXES = auto()
    UPGRADE_STATS = auto()
    SCROLL = auto()
    CHECK_NEW_LEVEL = auto()
    TRANSITION_LEVEL = auto()
    WAIT_FOR_UNLOCK = auto()


class StateMachine:
    def __init__(self, initial_state=State.FIND_RED_ICONS):
        self.current_state = initial_state
        self.previous_state = None
        self.state_handlers = {}
        self.priority_resolver = None
        logger.info(f"State machine initialized in state: {initial_state.name}")
    
    def register_handler(self, state, handler):
        self.state_handlers[state] = handler
        logger.debug(f"Registered handler for state: {state.name}")

    def set_priority_resolver(self, resolver):
        self.priority_resolver = resolver
        logger.debug("Priority resolver registered")
    
    def transition(self, new_state):
        if new_state != self.current_state:
            logger.info(f"State transition: {self.current_state.name} -> {new_state.name}")
            self.previous_state = self.current_state
            self.current_state = new_state
    
    def update(self):
        if self.priority_resolver is not None:
            try:
                priority_state = self.priority_resolver(self.current_state)
            except Exception:
                logger.exception("Priority resolver failed")
                priority_state = None

            if priority_state is not None and isinstance(priority_state, State):
                self.transition(priority_state)

        if self.current_state in self.state_handlers:
            handler = self.state_handlers[self.current_state]
            next_state = handler(self.current_state)
            
            if next_state is not None and isinstance(next_state, State):
                self.transition(next_state)
            
            return True
        else:
            logger.warning(f"No handler registered for state: {self.current_state.name}")
            return False
    
    def get_state(self):
        return self.current_state
    
    def get_state_name(self):
        return self.current_state.name
