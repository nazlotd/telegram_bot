# Deploy Notes

Data promo yang admin update melalui bot disimpan dalam JSON.

Untuk elak data hilang selepas redeploy, set environment variable `DATA_DIR`
kepada folder persistent storage di hosting.

Contoh:

```text
DATA_DIR=/var/data
```

Fail yang akan disimpan dalam folder itu:

```text
data.json
users.json
```

Jika `DATA_DIR` tidak diset, bot akan guna folder local project:

```text
data/
```

Folder local ini sesuai untuk development, tapi biasanya tidak selamat untuk
data runtime di platform deploy yang rebuild/redeploy dari Git.

## Intro Bergerak

Bot akan cari intro mengikut susunan ini:

```text
data/intro.mp4
data/intro.gif
data/intro.jpeg
```

Untuk intro bergerak, letak fail `intro.mp4` atau `intro.gif` dalam folder
`data/`. Fail `intro.mp4` lebih digalakkan kerana biasanya lebih kecil dan
lebih lancar di Telegram.

Jika mahu guna path lain semasa deploy, set environment variable:

```text
INTRO_ANIMATION_FILE=/path/intro.mp4
INTRO_GIF_FILE=/path/intro.gif
INTRO_FILE=/path/intro.jpeg
```
