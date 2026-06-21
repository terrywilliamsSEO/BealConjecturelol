# Sage Environment Report

- Execution mode: `docker`.
- Detected version: `Docker version 28.0.4, build b8034c0`.
- Native Sage: `False`.
- WSL Sage: `False`.
- Docker available: `True`.
- CI mode: `True`.
- WSL launched: `False`.
- WSL Sage binary found: `False`.
- WSL timeout seconds: `5`.

## Commands Tested

- `/usr/bin/docker --version`

## WSL Diagnosis

- Command attempted: `none`
- Recommended manual command: `wsl sh -lc 'command -v sage && sage --version'`

## Interpretation

Use native Sage first, then WSL Sage, then Docker. If all are unavailable, generated jobs remain queued and candidates stay at `needs_external_sage_check`.
