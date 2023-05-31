def change_glob(x, y):
    globals()[x] = y
    return y
def ret_glob():
    return globals()
def get_globes(x):
    if x in globals():
        return globals()[x]
def if_none_default(st, default):
    piece = get_globes(st)
    if piece is None:
        piece = default
    return change_glob(st, piece)
