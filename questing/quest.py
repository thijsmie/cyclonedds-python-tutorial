from dataclasses import dataclass, field
from typing import List, Dict, Callable, Any
from IPython.display import display, Markdown
from .exc import _StopExecution


class Quest:
    """
    _name: str
    _prompt: str
    _hints: List[str]
    _solution: str
    _seed: int
    _journal: object
    _started: bool
    _solved: bool
    _checkers: Dict[str, Callable[[Any], None]]
    _checked: List[bool]
    """

    def __init__(self, journal, seed, name, prompt, hints, solution):
        self._journal = journal
        self._seed = seed
        self._name = name
        self._prompt = prompt
        self._hints = hints
        self._solution = solution
        self._checkers = {}
        self._started = False
        self._solved = False
        self._checked = None

    def start(self):
        self._started = True
        self._solved = False
        self._checked = {k: False for k in self._checkers.keys()}

    def finish(self, no_out=False):
        self._started = False
        self._solved = all(self._checked.values())

        if self._solved:
            if hasattr(self, "pre_finish"):
                try:
                    self._pre_finish()
                except:
                    self._solved = False

        if no_out:
            return

        if self._solved:
            display(Markdown(f"<span style=\"color:green\">Quest {self._name} completed.</span>"))
        else:
            display(Markdown(f"<span style=\"color:red\">Quest {self._name} is incomplete.</span>"))

    def check(self, task, item):
        if not self._started:
            return

        if task not in self._checkers:
            display(Markdown("<span style=\"color:red\">No such quest task!</span>"))
        try:
            self._checkers[task](item)
            self._checked[task] = True
        except:
            if self.journal._debug_mode:
                import traceback
                traceback.print_exc()
            display(Markdown(f"<span style=\"color:red\">Check {task} did not succeed.</span>"))
            self._started = False
            self.finish(True)
            raise _StopExecution()

    def hint(self, index=0):
        if type(index) != int or index < 0 or index >= len(self._hints):
            display(Markdown(f"<span style=\"color:red\">No hint at index {index}.</span>"))
            return

        txt = f"> Hint {index}: " + self._hints[index]
        if len(self._hints) > 1:
            txt += f"\n\nThere are {len(self._hints)} in total, use `quest.hint(index)` to display other ones"
        display(Markdown(txt))

    def solution(self):
        display(Markdown("```python\n" + self._solution + "\n```\n"))

    def prompt(self):
        display(Markdown("---\n" + self._prompt + "\n---\n"))

    def __str__(self):
        return f"{self._name} quest"

    __repr__ = __str__
