# portfolio-project

**Remember that this project cannot be submitted late.**

Write a class named **ChessVar** for playing an abstract board game that is a variant of chess--atomic chess. The following explanation of the rules assumes some familiarity with the rules of chess - specifically how the pieces move and capture. If you have any questions about those rules, please don't hesitate to ask.

The starting position for the game is the normal starting position for standard chess. You will need to keep track of which player's turn it is. As in standard chess, white moves first. Pieces move and capture the same as in standard chess, except that **there is no check or checkmate, and there is no castling, en passant, or pawn promotion**. As in standard chess, each pawn should be able to move two spaces forward on its first move (but not on subsequent moves). 

If a player's king is captured or blown up, the game ends, and that player loses. 

Locations on the board will be specified using "algebraic notation", with columns labeled a-h and rows labeled 1-8, as shown in this diagram:

![board](starting_position.png "starting position")

Special rules for this variant of chess:

In Atomic Chess, whenever a piece is captured, an "explosion" occurs at the 8 squares immediately surrounding the captured piece in all the directions. This explosion kills all of the pieces in its range except for **pawns**. Different from regular chess, where only the captured piece is taken off the board, in Atomic Chess, every capture is suicidal. Even the capturing piece is affected by the explosion and must be taken off the board. As a result, a pawn can only be removed from the board when directly involved in a capture. If that is the case, both capturing and captured pawns must be removed from the board. Because every capture causes an explosion that affects not only the victim but also the capturing piece itself, **the king is not allowed to make captures**. Also, a player **cannot blow up both kings at the same time**. In other words, the move that would kill both kings in one step is not allowed. Blowing up a king has the same effect as capturing it, which will end the game.
[(https://www.chess.com/terms/atomic-chess#captures-and-explosions)](https://www.chess.com/terms/atomic-chess#captures-and-explosions)

Your ChessVar class must include the following:
* An **init method** that initializes any data members
* A method called **get_game_state** that just returns 'UNFINISHED', 'WHITE_WON', 'BLACK_WON'. 
* A method called **make_move** that takes two parameters - strings that represent the square moved from and the square moved to.  For example, make_move('b2', 'b4').  If the square being moved from does not contain a piece belonging to the player whose turn it is, or if the indicated move is not allowed, or if the game has already been won, then it should **just return False**.  Otherwise it should make the indicated move, remove any captured (explosion) pieces from the board, update the game state (unfinished to who wins) if necessary, update whose turn it is, and return True.

You need to implement a method called **print_board** that outputs the current state of the board. This will be extremely helpful for testing. You can choose any format for displaying the board, provided it is legible to others. If you're uncertain about the acceptability of your format, ask it on the discussion board.

Feel free to add whatever other classes, methods, or data members you want.  All data members of a class must be private.  Every class should have an init method that initializes all of the data members for that class.

Here's a very simple example of how the class could be used:
```
game = ChessVar()
print(game.make_move('d2', 'd4'))  # output True
print(game.make_move('g7', 'g5'))  # output True
print(game.make_move('c1', 'g5'))  # output True
game.print_board()
print(game.get_game_state())  # output UNFINISHED
```
The file must be named: ChessVar.py
