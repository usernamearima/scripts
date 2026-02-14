# UAC RunAsInvoker Script

This repository contains a simple Windows batch script that uses the
`__COMPAT_LAYER=runasinvoker` compatibility layer.

## What it does
The script forces an application to run **without requesting administrator privileges**,
even if it is marked to require elevation.

## Use cases
- Testing application behavior without admin rights
- Avoiding automatic UAC prompts
- Educational purposes

## Disclaimer
This project is intended for educational and testing purposes only.
Use only on systems you own or have permission to manage.
