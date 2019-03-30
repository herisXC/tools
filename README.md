# Tools

## Backlight changer
Service that change screen backlight in Dell Vastro laptops.

#### Installation
```bash
sudo chmod a+x backlight-changer.sh
sudo cp backlight-changer.sh /usr/sbin/
sudo cp backlight.service /etc/systemd/system/
```
#### Enable on system startup
```bash
systemctl enable backlight.service
systemctl start backlight.service
```

---

## Photo renamer
Change photo file names based on date when the photo has been taken. File name format: `YYYY-MM-DD_HH.MM.SS`

#### Usage
```bash
rename-photos.sh <photos_dir>
```
`photos_dir` directory with photo files. Files will be overwritten in this directory.
