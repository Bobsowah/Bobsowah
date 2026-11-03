"""Create a pandoc-friendly copy of the master report .tex.

- strips \\allowbreak (texmath cannot parse it)
- pandoc's LaTeX reader drops \\cite{} without a bibliography engine, so numeric
  citations [n] are resolved here from the thebibliography order, and the
  bibliography is rewritten as plain numbered paragraphs.
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
s = s.replace("\\allowbreak", "")
head, bib = s.split("\\begin{thebibliography}{9}")
bib, tail = bib.split("\\end{thebibliography}")
entries = re.split(r"\\bibitem\{([^}]+)\}", bib)
keys, texts = entries[1::2], entries[2::2]
num = {k: i + 1 for i, k in enumerate(keys)}
def cite(m):
    ks = [k.strip() for k in m.group(2).split(",")]
    body = ", ".join(str(num[k]) for k in ks)
    post = m.group(1)
    return "[" + body + (", " + post if post else "") + "]"
head = re.sub(r"\\cite(?:\[([^\]]*)\])?\{([^}]+)\}", cite, head)
assert "\\cite" not in head
out = ["\\begingroup"]
for i, (k, t) in enumerate(zip(keys, texts), 1):
    out.append("\\noindent [%d]~%s\n" % (i, " ".join(t.split())))
out.append("\\endgroup")
open(dst, "w", encoding="utf-8").write(head + "\n".join(out) + tail)
print("citations resolved; %d references" % len(keys))
