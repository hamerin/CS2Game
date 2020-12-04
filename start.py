from src import init, prompt_difficulty, game, result

displaysurf, clock = init()
diff, diff_color = prompt_difficulty(displaysurf, clock)
score = game(displaysurf, clock, diff, diff_color)
result(displaysurf, clock, diff, diff_color, score)
