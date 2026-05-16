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
