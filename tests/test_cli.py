"""Tests for ForgeKit CLI."""

import subprocess

from forgekit.cli import get_forgekit_root


def test_get_forgekit_root():
    """get_forgekit_root() returns the repo root (contains pyproject.toml)."""
    root = get_forgekit_root()
    assert root.is_dir()
    assert (root / "pyproject.toml").exists()
    assert (root / "skills").is_dir()
    assert (root / "commands").is_dir()


def test_cli_help():
    """forgekit --help exits 0 and shows usage."""
    result = subprocess.run(
        ["uv", "run", "forgekit", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "ForgeKit" in result.stdout


def test_cli_status(capsys):
    """forgekit status runs without error."""
    from forgekit.cli import cmd_status

    class Args:
        pass

    cmd_status(Args())
    captured = capsys.readouterr()
    assert "ForgeKit v" in captured.out


def test_cmd_init_creates_symlinks(tmp_path, monkeypatch):
    """forgekit init creates skills and commands symlinks."""
    monkeypatch.chdir(tmp_path)

    from forgekit.cli import cmd_init

    class Args:
        pass

    cmd_init(Args())

    claude_dir = tmp_path / ".claude"
    assert claude_dir.is_dir()
    assert (claude_dir / "skills").is_symlink()
    assert (claude_dir / "commands").is_symlink()

    # Symlinks point to real directories with content
    assert (claude_dir / "skills").is_dir()
    assert (claude_dir / "commands").is_dir()

    # Marker file created
    marker = tmp_path / ".forgekit"
    assert marker.exists()
    content = marker.read_text()
    assert "version=0.1.0" in content


def test_cmd_uninstall_removes_symlinks(tmp_path, monkeypatch):
    """forgekit uninstall removes symlinks and marker."""
    monkeypatch.chdir(tmp_path)

    from forgekit.cli import cmd_init, cmd_uninstall

    class Args:
        pass

    # First init, then uninstall
    cmd_init(Args())
    cmd_uninstall(Args())

    claude_dir = tmp_path / ".claude"
    assert not (claude_dir / "skills").exists()
    assert not (claude_dir / "commands").exists()
    assert not (tmp_path / ".forgekit").exists()


def test_cmd_init_replaces_existing_symlink(tmp_path, monkeypatch):
    """forgekit init replaces an existing symlink without error."""
    monkeypatch.chdir(tmp_path)

    from forgekit.cli import cmd_init

    class Args:
        pass

    # Init twice — second call should replace symlinks
    cmd_init(Args())
    cmd_init(Args())

    claude_dir = tmp_path / ".claude"
    assert (claude_dir / "skills").is_symlink()
    assert (claude_dir / "commands").is_symlink()
