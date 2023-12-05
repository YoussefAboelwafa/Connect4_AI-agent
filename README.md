# Connect4 Vs AI agent
Play Connect4 against an intelligent AI agent using Minimax Algorithm with and without Pruning

![image](https://storage.googleapis.com/kaggle-media/learn/images/EZKHxyy.png)

## Deployment

To Run Graphical Interface:
 ```bash
  python GUI.py
 ```

## Algorithms Used

### Minimax Algorithm Pseudocode:
  
```python
def minimax(board, depth, maximizingPlayer):
    if the game is over or depth == 0:
        return evaluate the board
    
    if maximizingPlayer:
        maxEval = -infinity
        for each child of board:
            eval = minimax(child, depth - 1, false)
            maxEval = max(maxEval, eval)
        return maxEval
    
    else:  # minimizing player
        minEval = +infinity
        for each child of board:
            eval = minimax(child, depth - 1, true)
            minEval = min(minEval, eval)
        return minEval
 ```

### Minimax Algorithm with Alpha-Beta Pruning Pseudocode:
  
```python
def minimax_alpha_beta(board, depth, alpha, beta, maximizingPlayer):
    if the game is over or depth == 0:
        return evaluate the board
    
    if maximizingPlayer:
        maxEval = -infinity
        for each child of board:
            eval = minimax_alpha_beta(child, depth - 1, alpha, beta, false)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    
    else:  # minimizing player
        minEval = +infinity
        for each child of board:
            eval = minimax_alpha_beta(child, depth - 1, alpha, beta, true)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval
```
![image](https://storage.googleapis.com/kaggle-media/learn/images/BrRe7Bu.png)
<br>
![image](https://storage.googleapis.com/kaggle-media/learn/images/bWezUC3.png)

## Heuristic Function

![image](https://storage.googleapis.com/kaggle-media/learn/images/FBoWr2f.png)

```python
 A = 100000
 B = 5000
 C = 200
 D = -100
 E = -4000
```

## Analysis for Runtime
- The following analysis is done on a random state
- The time is measured in seconds

### Without Pruning:
<table align="center">
  <tr>
    <th>Depth</th>
    <th>States Expanded</th>
    <th>Time Taken</th>

  </tr>
  <tr>
    <td>1</td>
    <td>7</td>
    <td>0.009</td>
  </tr>
  <tr>
    <td>2</td>
    <td>57</td>
    <td>0.043</td>
  </tr>
  <tr>
    <td>3</td>
    <td>400</td>
    <td>0.25</td>
  </tr>
  <tr>
    <td>4</td>
    <td>2775</td>
    <td>1.53</td>
  </tr>
  <tr>
    <td>5</td>
    <td>19608</td>
    <td>6.63</td>
  </tr>
  <tr>
    <td>6</td>
    <td>135885</td>
    <td>9.88</td>
  </tr>

</table>

### With Pruning:

<table align="center">
  <tr>
    <th>Depth</th>
    <th>States Expanded</th>
    <th>Time Taken</th>
  </tr>
  <tr>
    <td>1</td>
    <td>7</td>
    <td>0.009</td>
  </tr>
  <tr>
    <td>2</td>
    <td>27</td>
    <td>0.039</td>
  </tr>
  <tr>
    <td>3</td>
    <td>84</td>
    <td>0.185</td>
  </tr>
  <tr>
    <td>4</td>
    <td>235</td>
    <td>0.65</td>
  </tr>
  <tr>
    <td>5</td>
    <td>1111</td>
    <td>2.8</td>
  </tr>
  <tr>
    <td>6</td>
    <td>25506</td>
    <td>1.6</td>
  </tr>
  <tr>
    <td>7</td>
    <td>142546</td>
    <td>9.86</td>
  </tr>  
  <tr>
    <td>8</td>
    <td>508643</td>
    <td>30.84</td>
  </tr>
</table>