# automatic aiworks checkin and out

## Install

### requirements

- python3.8
- pip 22.2.2
- chromedriver
  - https://chromedriver.chromium.org/downloads

```shell
git clone https://github.com/smyoo-testworks/hiworks-check-in-and-out.git

pip3 install -r requirements.txt
```

## Usage

### hiworks.ini
```ini
[default]
url=https://office.hiworks.com/testworks.onhiworks.com/
id=your-id
password=your-password
```

### Python CLI
```shell
python3 cli.py checkin --id={your-hiworks-id} --passwd={your-hiworks-password}

python3 cli.py checkout --id={your-hiworks-id} --passwd={your-hiworks-password}
```

### Shell Script
```shell
sh ./startup.sh {checkin or checkout}
# or
./startup.sh {checkin or checkout}
```