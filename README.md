# automatic hiworks checkin and out

## Install

### requirements

- python ^3.10 (하위 버전 호환 X)
- pip ^22.2.2

**Packages**

```requirements.txt
click~=8.1.3
selenium==4.6.0
webdriver-manager~=3.8.4
pytimekr~=0.1.0
packaging~=21.3
pandas~=1.5.1
APScheduler~=3.9.1.post1
git+https://github.com/miniyus/dfquery.git
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

**~~use Crontab~~**

```shell
# 09시 정각 checkin
00 09 * * 1-5 cd /{your-path}/hiworks-check-in-and-out && sh hiworks-checker.sh checkin >> /{your-path}/hiworks-check-in-and-out/cron.log 2>&1

# 18시 정각 checkout
00 18 * * 1-5 cd /{your-path}/hiworks-check-in-and-out && sh hiworks-checker.sh checkout >> /{your-path}/hiworks-check-in-and-out/cron.log 2>&1

# 08 ~ 22시까지 10분마다 실행
*/10 08-22 * * 1-5 cd /{your-path}/hiworks-check-in-and-out && sh hiworks-checker.sh check-and-alert >> /{your-path}/hiworks-check-in-and-out/cron.log 2>&1

```

**schedule command**
> schedule 커맨드를 통해 크론 없이 스케줄링이 가능합니다.

```shell

sh ./hiworks-checker.sh schedule

```

schedule configuration
> [scheduler.json](./hciao/config/scheduler.json)

```json
{
  "test": {
    "command": "test(command-name)",
    "args": [
      "argument1",
      "argument2"
    ],
    "hour": "*",
    "minute": "*",
    "second": "10",
    "day_of_week": "*"
  }
}
```

- command: CLI 명령에 등록 되어 있는 명령어 이름을 전달 합니다.
    - 단, '-'이 포함된 명령은 '-' 대신 '_'(으)로 표기 해야 합니다.
- args: CLI 명령에 등록 되어 있는 명령어의 옵션 및 인수를 전달 합니다.
- hour: 등록할 주기의 시간 입니다.
- minute: 등록할 주기의 분 입니다.
- second: 등록할 주기의 초 입니다.
- day_of_week: 등록할 주기의 요일 입니다.
- hour, minute, second, day_of_week은 crontab의 표현식을 사용합니다.
    - 좀 더 자세한 표현식 참조
      - Cron 위키 피디아: https://en.wikipedia.org/wiki/Cron#CRON_expression 
      - APScheduler 공식 문서: https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html

### For Windows batch

```shell
./hiworks-checker.bat {command-name} {arguments} {--options}
```