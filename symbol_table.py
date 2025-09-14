# --- Super simple symbol table demo ---

class Env:
    def __init__(self, outer=None):
        self.outer = outer
        self.table = {}

    def put(self, name, typ):
        self.table[name] = typ

    def get(self, name):
        return self.table.get(name) or (self.outer.get(name) if self.outer else None)

# --- Tiny parser ---
def parse(tokens, env=None):
    if env is None:
        env = Env()

    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == "{":
            inner_env = Env(env)
            i += 1
            inner_tokens = []
            count = 1
            while count > 0:
                if tokens[i] == "{": count += 1
                if tokens[i] == "}": count -= 1
                if count > 0: inner_tokens.append(tokens[i])
                i += 1
            parse(inner_tokens, inner_env)
        elif isinstance(t, tuple):  # declaration: (type, name)
            typ, name = t
            env.put(name, typ)
            i += 1
        else:  # identifier usage
            typ = env.get(t) or "???"
            print(f"{t}: {typ}", end="; ")
            i += 1
    return env

# --- Demo ---
tokens = [
    ("int","x"), "x",
    "{", ("float","x"), "x", "}",
    "x"
]

parse(tokens)
