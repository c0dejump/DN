# DN
Drupal Node checker


## Usage
```
> $ python3 drupal_node.py -u https://www.groupe-pomona.fr/ -h                                         
usage: drupal_node.py [-h] [-u URL] [-r RANGES] [-t TYPE_]

optional arguments:
  -h, --help  show this help message and exit
  -u URL      URL login to test [required]
  -r RANGES   range (Ex: 0-1000); Default: 0-1000
  -t TYPE_    type of scan (taxonomy or node)
```

![alt tag](https://github.com/c0dejump/DN/blob/main/static/dn.png)


## Features

- Check node by ranges
- Check:
  - node/x/revisions
  - node?_format=hal_json
  - If PATCH/DELETE/PUT method are authorized on node
