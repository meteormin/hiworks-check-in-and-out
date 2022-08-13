class LoginElement:
    input_id: str = '#office_id'
    input_pass: str = '#office_passwd'
    login_btn: str = '.int_jogin'


class Check:
    wrap_class: str = '.today-status'
    open_div_btn: str = '.hw-button'
    detail: str = '.today-detail'

    check_btn: str = 'button'
    check_text_div: str = '.check-btn'
    check_text_content: str = ''


class Checkin(Check):
    check_text_content: str = '출근하기'


class Checkout(Check):
    check_text_content: str = '퇴근하기'
