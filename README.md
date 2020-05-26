# Intro to AI lab3
**`0712245 高魁駿`**
## Environment:
- development tools:
    - IDE: Sublime text, cmd(window,python3)
    - Compile Option: python runner.py
## Task description
- develop a Minesweeper AI based on (propositional) logic agent

## Algorithm & Complexity
- Minesweeper is a special case of SAT. Determining whether a given mine configuration satisfies the board constraints was proven to be NP-complete in 2000

## Implementation
- Given the current state of the board, and a state of knowledge about the board **the knowledge base** the agent uses the following 3 steps to move ahead :
    * Check the list of mine and non-mine variables using basic solver. If any mines and non-mines found, then flag and open them respectively. If nothing can be deduced, proceed to evaluating subsets.*
    * Solve subsets and find non-mines and mines by breaking down the equations.
    *	Click randomly if no subsets can be resolved.

There is one potential risk that is bound to occur in the third phase since the agent opens cells in a quasi-random manner. Although the heuristic reduces the risk, it does not guarantee the opening of a safe cell. Another risk is that in environments with high-mine density the heuristic-method of randomly opening cells would fail.



## Experiment Results

* 9 * 9/10(easy) : 0.5222 (10000 times,random testcases)
* 16 * 16/25(mid) : 0.4803 (10000 times,random testcases)
* 30 * 16/99(hard) : 0.102 (1000 times,random testcases)

* Our final result is (you can't select a mine in the first step.)

     * 9 * 9/10(easy) : 0.7523 (10000 times,random testcases)

    * 16 * 16/25(mid) : 0.7054 (10000 times,random testcases)

    * 30 * 16/99(hard) : 0.192 (1000 times,random testcases)

* Speed

    * 9 * 9/10(easy) : 0.23s

    * 16 * 16/25(mid) : 6.96s

    * 30 * 16/99(hard) : 48.26s
![](https://i.imgur.com/w9Xuj3K.png)
## Mine Density Discussion
![](https://i.imgur.com/tsVYx5i.png)             ![](https://i.imgur.com/syp3C65.png)
* The agent plays minesweeper on a board of size 16x16 and for each mine-density, we play 10 games. The mine density ranges from 0.01 to 0.5 with a step-size of 0.01. We observe that the results obtained agree with our intuition.
    *  As the mine density increases, the average final score decreases. For the first few mine- densities the number of mines flagged is exactly equal to the total number of mines present giving a score of 1.0. However, with increasing mine-density the difficulty also increases and hence the average score goes down.
    * Similarly, with increased mine-density the average density of mines hit by the agent also increases. This also agrees with our intuition and we see that although the agent opens more number of mines as the density increases, this increase is gradual and not steep.

Based on the above graphs, we see that the game can be called "hard" when the density of mines hit by the agent is 0.10 - the agent hits 10 percentage of the total mines - which occurs at mine-density 0.3.

## Win Rate Discussion
![](https://i.imgur.com/t0wCvLu.png)

## Discussion
* What influences or controls the length of the longest chain of influence when solving a certain board?
    *	The chain of influence can be either deep or wide. If the length of longest chain of influence has to be categorized by how deep it is, then that length can be controlled by how less random cells are opened. In my case, since I open up the cells sequentially, we are creating a deeper chain of influence with minimal branching (since neighborhood of cells are in constraint equations of each other, so are represented by a smaller KB). However, if the length of longest chain of influence has to be categorized by how wide it is, then that length can be controlled by how many random cells are opened. If more random cells are opened, we are looking at constraint equations having no dependency on each other, hence no new cell can be deduced in a deterministic way and we will end up exploring a lot of cells with no definite answer.

* How does the length of the chain of influence influence the efficiency of your solver?
    *	The length of chain of influence has a direct impact on the efficiency of the solver. When there is a thin deep chain of influence, the efficiency of the solver is high because the solver is able to deduce the KB in a deterministic fashion, rather than deducing randomly. While, if the solver chooses random points to open up, its efficiency decreases as it is more unsure about the state of a particular cell. In our program, the thinner deep chain of influence is created by basic solver + subset problem, while more branched chain of influence is induced by the random heuristic step of the solver. Any new constraint equation expands the KB and hence, increases the computing cost. If the solution to the problem is a thinner deeper chain of influence, the constraint equations formed along the way are dependent on each other hence, the KB does not expand as much as it would if independent constraint equations are formed (due to random cell opening).

* How to minimize the length of chains of influence to inform the decisions you make, to try to solve the board more efficiently?
    * If we pick the cells which are more connected to the constraint equations (coming most of the time in a set of equations), we can minimize the length of chains of influence.

* Is solving minesweeper hard?
    * As our agent, it correctly deduces most of the cells based on basic solver + subset solution. However, in the cases when no deduction can be made, the agent uses a heuristic approach based on probabilities to open up a new cell. This can lead to an error that the opened cell is actually a mine. When this kind of scenario arises quite often, we can say that at that point, the size of the board and mine density makes solving the game harder.


## Bonus Discussion

**[Optional / Extra Credits] These are for discussion only; no implementation/experiments required.**
1. How to use first-order logic here?
2. Discuss whether forward chaining or backward chaining applicable to this problem.
3. Propose some ideas about how to improve the success rate of "guessing" when you want to proceed from a "stuck" game.

### Apply first-order logic
* Our knowledge about the minesweeper game is then expressed by the following propositions:
> ∃i ∃j (M(i, j) ∧ (i≠1 ∨ j≠1))
∀i ∀j ∀i' ∀j' (M(i, j) ∧ (i≠i' ∨ j≠j')) → ¬M(i', j')
∀i ∀j ∀i' ∀j' (M(i, j) ∧ (|i − i'| ≤ 1) ∧ (|j − j' | ≤ 1) ∧ ¬(i = i' ∧ j = j')) → A(i', j')
∀i' ∀j' (∀i ∀j (|i − i'| ≤ 1) ∧ (|j − j'| ≤ 1) ∧ ¬(i = i' ∧ j = j') → ¬M(i, j)) → ¬A(i', j')

### forward/backward chaining
* Backward linking may take less time than forward linking than forward linking, because Backward linking is a goal-driver, not a mess like forward chaining.
### Guessinng strategy when stuck
 * Depending the third heuristic-method , I will choose some better heuristic-method CSP problem that can help to click randomly if no subsets can be resolved.


## Appendix Code
> minesweeper.py
``` python
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # if all the cells are mines or none of them are mines
        if self.count == len(self.cells):
            return self.cells

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if all the cells are mines or none of them are mines
        if self.count == 0:
            return self.cells

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if len(self.cells) == 1:
            return
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

        return


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        if len(self.cells) == 1:
            return
        # check if cell in self.cells
        if cell in self.cells:
            self.cells.remove(cell)

        return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        return


    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

        return


    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

        return


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        current_mines = set()
        current_safes = set()

        self.moves_made.add(cell)
        self.mark_safe(cell)

        # gettin current sentence
        current_sentence = Sentence(self.get_neighbors(cell), count)
        _current_sentence_cells = current_sentence.cells.copy()

        # clean sentence,  remove cells that are already safes or mines
        current_mines_ = (cell for cell in _current_sentence_cells
                            if cell in self.mines)
        for mine in current_mines_:
            current_sentence.cells.discard(mine)
            current_sentence.count -= 1

        current_safes_ = (cell for cell in _current_sentence_cells
                            if cell in self.safes)
        for safe in current_safes_:
            current_sentence.cells.discard(safe)

        # check if all cells are either safes or mines
        current_safes.update(current_sentence.known_safes())
        current_mines.update(current_sentence.known_mines())
        # if current_sentence.count == 0:
        #     current_safes.update(current_sentence.cells)
        # elif current_sentence.count == len(current_sentence.cells):
        #     current_mines.update(current_sentence.cells)

        # add sentence to knowledge
        self.knowledge.append(current_sentence)

        # removing subsets from other sentences. Divide and conquer
        for sentence in self.knowledge:
            for other in self.knowledge:
                if sentence == other:
                    pass
                elif sentence.cells.issubset(other.cells) \
                    and len(sentence.cells) < len(other.cells):
                    other.cells = other.cells - sentence.cells
                    other.count -= sentence.count

        # getting new conclussions
        for sentence in self.knowledge:
            known_ = sentence.known_mines()
            if known_:
                current_mines.update(known_)

            known_ = sentence.known_safes()
            if known_:
                current_safes.update(known_)

        # updating mines and safes
        for cell in current_mines:
            self.mark_mine(cell)
        for cell in current_safes:
            self.mark_safe(cell)

        return


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in (cell_ for cell_ in self.safes
                     if cell_ not in self.moves_made):
            return cell

        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        mines_ = 0
        convergence = (self.height * self.width - len(self.mines))
        while mines_ <= convergence:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                return (i, j)

            mines_ += 1

        return


    def get_neighbors(self, cell):
        """
        Returns a set containing all the neighboring cells of cell
        """

        neighbors = set()
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))

        return neighbors
```
> runner.py
```python=
from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 16
WIDTH = 16
MINES = 25
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
while True:
        move = ai.make_safe_move()
        if move is None:
            move = ai.make_random_move()
            if move is None:
                flags = ai.mines.copy()
                print("No moves left to make.")
            else:
                print("No known safe moves, AI making random move.")
        else:
            print("AI making safe move.")

        if move:
            if game.is_mine(move):
                lost = True
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)
```
```
