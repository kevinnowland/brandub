# Brandub

A python package to play brandub.


## Installation

```bash
pip install brandub
```

## Play a game

To play via the command line, simply run the `brandub` command.

To play a game in a python terminal or ipython terminal, 
instantiate a `BrandubGame` object and use the `run()` method.

```python
> from brandub import BrandubGame
> game = BrandubGame()
> game.run()
```

To exit either version, simply ctrl+c and enter 'y'.

## Rules

We use the rules on [this  website](http://tafl.cyningstan.com/page/171/brandub).
But here's a rundown:

Brandub is played on a 7x7 board. The monarch sits in the center surrounded
to the left, right, above, and below by defensive pawns. There are eight
attacking pawns, two each placed side by side next to the defensive pawsn
such that all pieces form a plus sign.
The goal for the defending team is to escort the monarch to any of the
corners. The goal for the attacking team is to capture the monarch.

All pieces can move horizontally or vertically any number of spaces, 
except that no piece can land on another piece nor can a piece move
past a piece in its way. Only the monarch can land in the corners of
the board -- the "forests" --
and no piece may land in the central square -- the "castle" -- once it
has been abandoned by the monarch, although any piece may continue moving
past it.

The pawns are captured if they are trapped by two opposing pieces
either to the left and right or above and below. Additionaly, pawns
can be trapped by the empty castle or by the forests. (Attacking
pawns can be trapped by the occupied castle since the only possible
occupant is the monarch.)

If inside the castle, the Monarch is only captured if surrounded by
four attacking pawns, one above, one below, one right, one left. If
the monarch is immediately next to the castle (not diagonally) then
the monarch is trapped by three attacking pawns and the empty castle.
Elsewhere, the monarch is trapped just like pawns, including being
trapped by a forest and attacking pawn.

The attackers move first. The game ends in a draw if a board position
is repeated.
