"""Fail when rules/01_scope_and_limits.md and llm/SYSTEM_PROMPT.md state a shared boundary differently."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = REPO_ROOT / "rules" / "01_scope_and_limits.md"
SYSTEM_PROMPT_PATH = REPO_ROOT / "llm" / "SYSTEM_PROMPT.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# The shared-boundary table.
#
# Both rules/01_scope_and_limits.md and llm/SYSTEM_PROMPT.md write out the
# same set of hard boundaries, once each, in their own prose. Nothing but
# this test compares the two. Each row below names one boundary both files
# must state, and a check (a regex or a small function) that must match in
# EACH file independently, so wording may differ but the permission or
# prohibition it grants must not.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Boundary:
    name: str
    rules_check: Callable[[str], bool]
    prompt_check: Callable[[str], bool]
    description: str


def _matches(pattern: str, flags: int = re.IGNORECASE) -> Callable[[str], bool]:
    compiled = re.compile(pattern, flags)
    return lambda text: compiled.search(text) is not None


def _not_matches(pattern: str, flags: int = re.IGNORECASE) -> Callable[[str], bool]:
    compiled = re.compile(pattern, flags)
    return lambda text: compiled.search(text) is None


BOUNDARIES: list[Boundary] = [
    Boundary(
        name="not the client's lawyer",
        rules_check=_matches(r"not the client's lawyer"),
        prompt_check=_matches(r"not their lawyer"),
        description="Both files must say the assistant is not the client's/their lawyer.",
    ),
    Boundary(
        name="no legal conclusions",
        rules_check=_matches(r"legal conclusion"),
        prompt_check=_matches(r"legal conclusion"),
        description="Both files must restrict the assistant from rendering a legal conclusion as certainty.",
    ),
    Boundary(
        name="never quote rule text into anything the client/user sends",
        rules_check=_matches(r"never quote rule text.*will send"),
        prompt_check=_matches(r"never quote the text of a rule.*will send"),
        description="Both files must forbid quoting rule text into anything the reader will send.",
    ),
    Boundary(
        name="never estimate or predict a recovery amount",
        rules_check=_matches(r"never estimate what a client will recover"),
        prompt_check=_matches(r"never predict an outcome or a recovery amount"),
        description="Both files must forbid estimating or predicting what the client will recover.",
    ),
    Boundary(
        name="deadline: named-section permission",
        rules_check=_matches(r"specific program section that names it"),
        prompt_check=_matches(r"specific program section that names it"),
        description=(
            "Both files must permit stating a deadline, limitation period, or filing "
            'window when it comes from "the specific program section that names it", '
            "not only from a fixed list of section numbers. This is the exact permission "
            "commit 82fe1b1 restored to rules/01_scope_and_limits.md to match "
            "llm/SYSTEM_PROMPT.md."
        ),
    ),
    Boundary(
        name="deadline: not limited to a fixed list of section numbers",
        # The pre-82fe1b1 drift text read "...appears in section 5 or section 7 of the
        # reader's own `references/state_XX.md`...", barring any deadline from any other
        # section (fee arbitration windows live in section 3 of most packs). Neither file
        # may go back to enumerating a fixed list of section numbers for this permission.
        rules_check=_not_matches(r"section \d+ or section \d+"),
        prompt_check=_not_matches(r"section \d+ or section \d+"),
        description=(
            "Neither file may limit a stated deadline to a fixed list of pack section "
            'numbers (e.g. "section 5 or section 7"); this is the exact shape of the '
            "drift fixed in commit 82fe1b1."
        ),
    ),
]


def check_layer_parity(rules_text: str, prompt_text: str) -> list[str]:
    """Return a list of failure messages, one per boundary not satisfied by both texts."""
    failures = []
    for boundary in BOUNDARIES:
        rules_ok = boundary.rules_check(rules_text)
        prompt_ok = boundary.prompt_check(prompt_text)
        if not rules_ok or not prompt_ok:
            failures.append(
                f"{boundary.name}: rules/01_scope_and_limits.md {'OK' if rules_ok else 'FAILED'}, "
                f"llm/SYSTEM_PROMPT.md {'OK' if prompt_ok else 'FAILED'} -- {boundary.description}"
            )
    return failures


def test_rules_and_system_prompt_state_the_same_boundaries() -> None:
    rules_text = _read(RULES_PATH)
    prompt_text = _read(SYSTEM_PROMPT_PATH)
    failures = check_layer_parity(rules_text, prompt_text)
    assert not failures, "rules/01_scope_and_limits.md and llm/SYSTEM_PROMPT.md disagree on a shared boundary:\n" + "\n".join(
        f"- {f}" for f in failures
    )
