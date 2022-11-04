# automatic aiworks checkin and out

## Install

### requirements

- python ^3.8
- pip ^22.2.2

**Packages**

```requirements.txt
click>=8.1.3
selenium==4.5.0
webdriver-manager==3.8.4
pytimekr~=0.1.0
packaging~=21.3
```

### install

```shell
git clone https://github.com/smyoo-testworks/hiworks-check-in-and-out.git

python -m venv venv

source ./venv/activate

pip3 install -r requirements.txt
```

## Usage

### Configure

hiworks.ini

```ini
[default]
url = https://office.hiworks.com/testworks.onhiworks.com/
id = your-id
password = your-password
```

mailer.ini

```ini
[outlook]
url = outlook.office365.com
id = your-id
password = your-password
```

### Python CLI

```shell
python3 cli.py {command-name} {arguments} {--options}

python3 cli.py checkin --id={your-hiworks-id} --passwd={your-hiworks-password}

python3 cli.py checkout --id={your-hiworks-id} --passwd={your-hiworks-password}
```

### Shell Script

```shell
# help about commands
./hiworks-checker.sh --help

# checkin and checkout
sh ./hiworks-checker.sh {checkin or checkout}
# or
./hiworks-checker.sh {checkin or checkout}

# check work hour
./hiworks-checker.sh check-work-hour

# check and alert
./hiworks-checker.sh check-and-alert

```

### Scheduler

**use Crontab**

```shell
# 09시 정각 checkin
00 09 * * 1-5 cd /{your-path}/hiworks-check-in-and-out && sh hiworks-checker.sh checkin >> /{your-path}/hiworks-check-in-and-out/cron.log 2>&1

# 18시 정각 checkout
00 18 * * 1-5 cd /{your-path}/hiworks-check-in-and-out && sh hiworks-checker.sh checkout >> /{your-path}/hiworks-check-in-and-out/cron.log 2>&1

# 08 ~ 22시까지 10분마다 실행
*/10 08-22 * * 1-5 cd /{your-path}/hiworks-check-in-and-out && sh hiworks-checker.sh check-and-alert >> /{your-path}/hiworks-check-in-and-out/cron.log 2>&1

```

### For Windows batch

```shell
./hiworks-checker.bat {command-name} {arguments} {--options}
```