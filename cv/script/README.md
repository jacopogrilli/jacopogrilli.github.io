# CV generation

The CV is a **backbone + generated includes**:

- `cv/jgrilli_cv.tex` — backbone. Hand-written sections (Vita, Editor, Reviewer,
  Teaching, Supervision, Grants, Scientific visits, …) live here. The five
  data-backed sections instead `\input{tex/<name>.tex}`.
- `cv/tex/*.tex` — auto-generated partials (do not edit by hand):
  `published.tex`, `preprint.tex`, `seminars.tex`, `meetings.tex`, `organized.tex`.

## Regenerate + build

```bash
cd cv && bash compile.sh        # runs generate_cv.py, then pdflatex x3
```

`script/generate_cv.py` reads `../../_data/{publist,talks}.yml` and rewrites the
partials. Routing:

| source field                        | → section / file |
|-------------------------------------|------------------|
| `publist.yml` `preprint: 0`         | `published.tex`  |
| `publist.yml` `preprint: 1`         | `preprint.tex`   |
| `talks.yml` `what: 1` / org. types  | `organized.tex`  |
| `talks.yml` type contains "seminar" | `seminars.tex`   |
| other talks                         | `meetings.tex`   |

## One-shot refactor

`script/build_backbone.py` converted the original monolithic CV into the backbone
(original saved as `script/jgrilli_cv_monolithic_backup.tex`). It is **not** part of
the normal build — only rerun it if you want to re-derive the backbone from scratch.

Known fidelity note: `talks.yml` has no "leading organizer" flag, so the `$\star$`
markers from the old hand-written *Organized* section are not reproduced.
