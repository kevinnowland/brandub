from .gamestate import GameState


class GameHistory:
    """ hold n GameState objects and check if the game is over
    via a draw or victory """

    def __init__(self, game_states, max_length=5):

        assert max_length > 0, "max_length must be positive"
        self.__max_length = max_length

        assert type(game_states) == list, "game_states must bve list"
        assert len(game_states) <= self.max_length, \
            "can't have more gamme states than max_length"
        assert len(game_states) > 0, \
            "must have at lesat one initial game state"
        assert all(type(state) == GameState for state in game_states), \
            "all elements of game_states. must be GameState"
        if len(game_states) > 1:
            assert all(not state.has_winner for state in game_states[:-1]), \
                "only final game state can have a winner"

        self.__game_states = game_states

    def __getitem__(self, *args):
        return self.game_states.__getitem__(*args)

    def __len__(self):
        return len(self.game_states)

    @property
    def current_state(self):
        return self[-1]

    @property
    def game_states(self):
        return self.__game_states

    @property
    def attack_victory(self):
        return self.game_states[-1].attack_victory

    @property
    def defense_victory(self):
        return self.game_states[-1].defense_victory

    @property
    def has_winner(self):
        return self.game_states[-1].has_winner

    @property
    def is_draw(self):
        if len(self.game_states) < 2:
            return False
        else:
            return self.__has_draw(self.game_states)

    @property
    def max_length(self):
        return self.__max_length

    @classmethod
    def __has_draw(cls, game_states):
        """ recursively check for equal game states between the
        last element of the game_states list and the other elements.

        WARNING: recursive function """
        assert len(game_states) > 1, "must have at least two games"

        draws = [gs.board == game_states[-1].board for gs in game_states[:-1]]
        has_draw = any(draws)
        if has_draw:
            return has_draw
        elif len(game_states) > 2:
            return cls.__has_draw(game_states[:-1])
        else:
            return False
