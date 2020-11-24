import pickle

for fn in ["easy", "normal", "hard", "insane", "extra"]:
    pickle.dump([], open(f"scores/{fn}.pkl", "wb"))
