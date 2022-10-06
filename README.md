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

### Python CLI
```shell
python3 main.py checkin --id={your-hiworks-id} --passwd={your-hiworks-password}

python3 main.py checkout --id={your-hiworks-id} --passwd={your-hiworks-password}
```

### Shell Script
```shell
sh ./startup.sh
# or
./startup.sh
```