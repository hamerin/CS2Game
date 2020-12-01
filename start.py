from src import init, game, result

displaysurf, clock = init()
diff, diff_color, score = game(displaysurf, clock)  # 게임
result(displaysurf, clock, diff, diff_color, score)
