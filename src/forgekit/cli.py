"""ForgeKit CLI - AI Engineering Skills Toolkit."""

import argparse
import subprocess
from pathlib import Path


def get_forgekit_root():
    """Get the root of the forgekit installation."""
    return Path(__file__).resolve().parent.parent.parent


def run_git(args, cwd=None):
    """Run a git command and return output."""
    result = subprocess.run(["git"] + args, cwd=cwd or get_forgekit_root(), capture_output=True, text=True)
    return result


def cmd_init(args):
    """Initialize forgekit in the current project."""
    project = Path.cwd()
    claude_dir = project / ".claude"
    claude_dir.mkdir(exist_ok=True)

    fk_root = get_forgekit_root()
    skills_src = fk_root / "skills"
    commands_src = fk_root / "commands"
    skills_dst = claude_dir / "skills"
    commands_dst = claude_dir / "commands"

    for src, dst, name in [(skills_src, skills_dst, "skills"), (commands_src, commands_dst, "commands")]:
        if dst.is_symlink():
            dst.unlink()
            print(f"  Replaced existing {name} symlink")
        elif dst.exists():
            print(f"  WARNING: {dst} exists and is not a symlink. Back it up first.")
            continue
        dst.symlink_to(src)
        print(f"  Linked .claude/{name}/ -> {src}")

    marker = project / ".forgekit"
    marker.write_text(f"version=0.1.0\ninstall_path={fk_root}\n")
    print(f"\nForgeKit initialized in {project}")


def cmd_update(args):
    """Pull latest forgekit from remote."""
    result = run_git(["pull"])
    print(result.stdout or result.stderr)


def cmd_status(args):
    """Show forgekit status."""
    from forgekit import __version__

    fk_root = get_forgekit_root()
    print(f"ForgeKit v{__version__}")
    print(f"Install: {fk_root}")

    result = run_git(["status", "--short"])
    if result.stdout.strip():
        print(f"\nUncommitted changes:\n{result.stdout}")
    else:
        print("Clean (no uncommitted changes)")

    project = Path.cwd()
    skills_link = project / ".claude" / "skills"
    commands_link = project / ".claude" / "commands"
    print(f"\nCurrent project: {project}")
    print(f"  Skills symlink:   {'YES' if skills_link.is_symlink() else 'NO'}")
    print(f"  Commands symlink: {'YES' if commands_link.is_symlink() else 'NO'}")


def cmd_diff(args):
    """Show changes in forgekit repo."""
    result = run_git(["diff"])
    print(result.stdout or "No changes")


def cmd_commit(args):
    """Commit changes in forgekit repo."""
    run_git(["add", "-A"])
    result = run_git(["commit", "-m", args.message])
    print(result.stdout or result.stderr)


def cmd_push(args):
    """Push forgekit to remote."""
    result = run_git(["push"])
    print(result.stdout or result.stderr)


def cmd_uninstall(args):
    """Remove forgekit symlinks from current project."""
    project = Path.cwd()
    for name in ["skills", "commands"]:
        link = project / ".claude" / name
        if link.is_symlink():
            link.unlink()
            print(f"  Removed .claude/{name} symlink")
        else:
            print(f"  .claude/{name} is not a symlink, skipping")
    marker = project / ".forgekit"
    if marker.exists():
        marker.unlink()
    print("ForgeKit uninstalled from this project.")


def main():
    parser = argparse.ArgumentParser(prog="forgekit", description="ForgeKit - AI Engineering Skills Toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Initialize forgekit in current project")
    sub.add_parser("update", help="Pull latest from remote")
    sub.add_parser("status", help="Show forgekit status")
    sub.add_parser("diff", help="Show uncommitted changes")

    p_commit = sub.add_parser("commit", help="Commit forgekit changes")
    p_commit.add_argument("-m", "--message", required=True, help="Commit message")

    sub.add_parser("push", help="Push to remote")
    sub.add_parser("uninstall", help="Remove symlinks from current project")

    args = parser.parse_args()
    commands = {
        "init": cmd_init,
        "update": cmd_update,
        "status": cmd_status,
        "diff": cmd_diff,
        "commit": cmd_commit,
        "push": cmd_push,
        "uninstall": cmd_uninstall,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
