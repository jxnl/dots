---
name: dotfiles-check
description: Verify a dotfiles change before installing it on a real home directory.
---

Read the installer and identify which shell, editor or agent files the change affects.
Run the installer tests. Use a temporary home to exercise the changed install path
twice. Check that the second run preserves unrelated files and backs up changed
destinations when backups are enabled.

For an editor change, open the affected editor headlessly and exercise the changed
mapping or command. For a shell change, compare the first interactive prompt and
verify the commands or version selection that the optimization touches.

Report what you ran and which checks still require the user's environment.
