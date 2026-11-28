# LeetCode in Python

Optimal Python solutions to LeetCode problems — grouped by pattern. Each solution ships with its complexity analysis, the argument for *why* it is optimal, the edge cases that break naive attempts, and a video walkthrough.

The goal is not "a solution that passes", but the best known asymptotic solution the problem's constraints allow.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for a topic-by-topic study order with curated problem links.

## Structure

```text
solutions/
├── arrays/
│   ├── README.md
│   └── 0001_two_sum.py
├── two-pointers/
├── sliding-window/
├── stack/
├── binary-search/
├── linked-list/
├── trees/
├── tries/
├── heap/
├── backtracking/
├── graphs/
├── 1d-dp/
├── 2d-dp/
├── greedy/
├── intervals/
├── math/
├── bit-manipulation/
├── strings/
└── misc/
```

Files are named `<zero-padded number>_<snake_case_slug>.py` and live in the topic folder that matches the pattern the optimal solution uses (not necessarily the LeetCode tag).

## Verify everything

```bash
python3 verify.py
```

Each solution exposes the same `Solution` class LeetCode expects plus a `_self_test()` function full of asserts. `verify.py` imports every file under `solutions/` and runs its self-test, so one command proves the whole repo still works.

## What each file contains

| Section | Purpose |
| --- | --- |
| `Approach` | The idea in a few sentences |
| `Complexity` | Time and space |
| `Why optimal` | The argument that it cannot be asymptotically beaten |
| `Edge cases` | Inputs that break careless code |
| `Pitfalls` | The mistakes people actually make |
| `Video` | Link once the walkthrough is published |

## Progress

| Topic | Solved | Videos |
| --- | --- | --- |
| Arrays | 1 | 0 |
| Two Pointers | 0 | 0 |
| Sliding Window | 1 | 0 |
| Stack | 1 | 0 |
| Binary Search | 1 | 0 |
| Linked List | 0 | 0 |
| Trees | 0 | 0 |
| Tries | 1 | 0 |
| Heap | 0 | 0 |
| Backtracking | 7 | 0 |
| Graphs | 7 | 0 |
| 1-D DP | 1 | 0 |
| 2-D DP | 0 | 0 |
| Greedy | 0 | 0 |
| Intervals | 0 | 0 |
| Math | 0 | 0 |
| Bit Manipulation | 0 | 0 |
| Strings | 0 | 0 |
| Misc | 0 | 0 |
| **Total** | **20** | **0** |

## Topics

- [Arrays](solutions/arrays/README.md)
- [Two Pointers](solutions/two-pointers/README.md)
- [Sliding Window](solutions/sliding-window/README.md)
- [Stack](solutions/stack/README.md)
- [Binary Search](solutions/binary-search/README.md)
- [Linked List](solutions/linked-list/README.md)
- [Trees](solutions/trees/README.md)
- [Tries](solutions/tries/README.md)
- [Heap](solutions/heap/README.md)
- [Backtracking](solutions/backtracking/README.md)
- [Graphs](solutions/graphs/README.md)
- [1-D DP](solutions/1d-dp/README.md)
- [2-D DP](solutions/2d-dp/README.md)
- [Greedy](solutions/greedy/README.md)
- [Intervals](solutions/intervals/README.md)
- [Math](solutions/math/README.md)
- [Bit Manipulation](solutions/bit-manipulation/README.md)
- [Strings](solutions/strings/README.md)
- [Misc](solutions/misc/README.md)

## License

MIT — see [LICENSE](LICENSE).
