class StateManager:

    def __init__(self):

        self.states = {}
        self.current_state = None

    def register(
        self,
        name,
        state
    ):

        self.states[name] = state

    def change(
        self,
        name
    ):

        self.current_state = self.states[name]

    def handle_event(
        self,
        event
    ):

        if self.current_state:

            self.current_state.handle_event(
                event
            )

    def update(self):

        if self.current_state:

            self.current_state.update()

    def draw(
        self,
        surface
    ):

        if self.current_state:

            self.current_state.draw(
                surface
            )