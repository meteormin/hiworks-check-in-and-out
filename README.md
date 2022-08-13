# automatic aiworks checkin and out

## Install

### requirements

- python3.8
- pip 22.2.2

```shell
git clone https://github.com/smyoo-testworks/hiworks-check-in-and-out.git

pip3 install -r requirements.txt
```

## Usage

```shell
python3 main.py checkin --id={your-hiworks-id} --passwd={your-hiworks-password}

python3 main.py checkout --id={your-hiworks-id} --passwd={your-hiworks-password}
```