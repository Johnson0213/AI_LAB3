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
