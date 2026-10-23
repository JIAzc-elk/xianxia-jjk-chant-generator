#!/usr/bin/env python3
"""Copy the portable skill to a native discovery directory. Python 3.9+."""

import argparse
import shutil
import sys
from pathlib import Path

NAME = "xianxia-jjk-chant-generator"
SOURCE = Path(__file__).resolve().parents[1] / "skills" / NAME
USER_DIRS = {
    "codex": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
    "opencode": Path(".config/opencode/skills"),
}
PROJECT_DIRS = {
    "codex": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
    "opencode": Path(".opencode/skills"),
}


def same_tree(left, right):
    """Compare all file bytes; preserve any locally added or modified file."""
    if not right.is_dir() or right.is_symlink():
        return False
    left_files = {p.relative_to(left) for p in left.rglob("*") if p.is_file()}
    right_files = {p.relative_to(right) for p in right.rglob("*") if p.is_file()}
    if left_files != right_files:
        return False
    return all(
        not (right / item).is_symlink()
        and (left / item).read_bytes() == (right / item).read_bytes()
        for item in left_files
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=[*USER_DIRS, "all"], required=True)
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--project", type=Path, help="Existing project directory")
    parser.add_argument("--home", type=Path, help="Alternate home for portable/test profiles")
    parser.add_argument("--dry-run", action="store_true", help="Show paths without writing")
    args = parser.parse_args(argv)
    if args.scope == "project":
        if args.home:
            parser.error("--home is only valid with --scope user")
        if args.project is None:
            parser.error("--scope project requires --project")
        root, directories = args.project.expanduser().resolve(), PROJECT_DIRS
        if not root.is_dir():
            parser.error("--project must be an existing directory")
    else:
        if args.project:
            parser.error("--project requires --scope project")
        root = (args.home or Path.home()).expanduser().resolve()
        directories = USER_DIRS
    if not (SOURCE / "SKILL.md").is_file():
        parser.error("Skill source missing; keep scripts/ and skills/ in the same repository")

    selected = list(directories) if args.tool == "all" else [args.tool]
    plan = [(tool, root / directories[tool] / NAME) for tool in selected]
    conflicts = [
        path for _, path in plan
        if (path.exists() or path.is_symlink()) and not same_tree(SOURCE, path)
    ]
    if conflicts:
        for path in conflicts:
            print(f"CONFLICT: {path}", file=sys.stderr)
        print("Nothing installed. Back up and rename the existing skill before retrying.", file=sys.stderr)
        return 1

    for tool, path in plan:
        if path.exists():
            print(f"UNCHANGED [{tool}]: {path}")
        elif args.dry_run:
            print(f"WOULD INSTALL [{tool}]: {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(SOURCE, path)
            if not same_tree(SOURCE, path):
                raise OSError(f"Copy verification failed: {path}")
            print(f"INSTALLED [{tool}]: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
