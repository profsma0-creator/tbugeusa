# Patch chapters.py: wrap subdict(...) calls in {} so they become positional dicts.
src = open("chapters.py").read()

def wrap_subdict(s):
    out = []
    i = 0
    while True:
        idx = s.find("subdict(", i)
        if idx == -1:
            out.append(s[i:])
            break
        out.append(s[i:idx])
        out.append("subdict({")
        # scan for matching close paren, starting depth=1 after 'subdict('
        depth = 1
        j = idx + len("subdict(")
        n = len(s)
        while j < n and depth > 0:
            c = s[j]
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            j += 1
        # j is one past the matching ')'
        close_paren = j - 1
        out.append(s[idx + len("subdict("):close_paren])
        out.append("})")
        i = j
    return "".join(out)

new = wrap_subdict(src)
open("chapters.py", "w").write(new)
print("done. subdict( count now:", new.count("subdict("))
