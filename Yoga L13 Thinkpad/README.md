# Yoga L13 Thinkpad

Helpers for the Thinkpad Yoga L13

## Touchscreen control

Script and system service to disable touchscreen if the stylus is in proximity to the screen. After the pen is not close anymore for a certain delay the touch screen is enabled again. This script is uses as a workaround for the not properly working palm recognition with Xournal++.

The logic was written and tested in python3. For systems without python3 there is also a (untested) shellscript converted by ChatGPT.

Ensure `evtest` is installed before:

```bash
sudo apt install evtest
```

The system this was written and tested for:

- Ubuntu 22.04 (Wayland)
