## OS pour AML-S905X-CC (Le Potato)

- J'ai utilisé Armbian Hirsute.
- `sudo armbian-config` pour activer les uart, le clavier FR, le wifi, etc.
- `hoel	ALL=(ALL:ALL) NOPASSWD: ALL` dans `sudo nano /etc/sudoers`
- changer le mdp du login `passwd`
- `sudo adduser hoel`
- `sudo usermod -aG adm,dialout,cdrom,sudo,audio,video,plugdev,input,netdev hoel`
- pensez a désactiver le ssh pour root, et le ssh par mot de pass

## GPIO pour AML-S905X-CC (Le Potato)

Don't trust https://docs.google.com/spreadsheets/d/1U3z0Gb8HUEfCIMkvqzmhMpJfzRqjPXq7mFLC-hvbKlE/edit#gid=0 too much, trust `sudo cat /sys/kernel/debug/gpio`: there is one GPIO chip with an offset of 500 (not 0) and a second chip with an offset of 400 (not 10), event for sysfs.
For ioctl use `gpiodetect` and `gpioinfo gpiochip1`.
