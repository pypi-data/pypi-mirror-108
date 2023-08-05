# -*- coding: utf-8 -*-

import functools
from .student import *
from .utils import *
from .spider import Spider
from .constant import API_Status, Client_Status


class U_Student(SCUStudent):
    '''
    A Fake Undergraduate student with SCU Api method
    '''

    def __init__(self):
        self.spider = Spider()
        self.student_id = None
        self.passwd_hash = None
        self.status = Client_Status.INIT

    def session_valid_required(func: Callable):
        @functools.wraps(func)
        def wrapper(self, *args, **kw):
            if not self.session_valid():
                return API_ReturnType(API_Status.ERROR, "session invalid [login required]")
            return func(self, *args, **kw)
        return wrapper

    def set_baseinfo(self, stid: str, passwd: str, hashed: Optional[bool] = False) -> NoReturn:
        self.student_id = stid
        self.passwd_hash = passwd
        if not hashed:
            self.passwd_hash = password_encryption(passwd)
        self.status = Client_Status.OFFLINE  # 更换信息后强制下线

    def get_captcha(self, filepath: Optional[str] = None) -> API_ReturnType:
        return self.spider.fetch_captcha(filepath)

    def login(self, captcha: str, remember_me: Optional[bool] = True) -> API_ReturnType:
        if self.status == Client_Status.INIT:
            return False
        _ = self.spider.login(
            self.student_id, self.passwd_hash, captcha, remember_me)
        self.status = [Client_Status.OFFLINE, Client_Status.ONLINE][_.is_ok()]
        return _

    def session_valid(self) -> bool:
        if self.status == Client_Status.ONLINE:
            return True  # for test
        return False

    @session_valid_required
    def get_student_name(self) -> API_ReturnType:
        return self.spider.fetch_student_name()

    @session_valid_required
    def get_student_pic(self, filepath: Optional[str] = None) -> API_ReturnType:
        return self.spider.fetch_student_pic(filepath)

    @session_valid_required
    def get_all_term_scores(self, pagesize: Optional[int] = -1) -> API_ReturnType:
        return self.spider.fetch_all_term_scores(pagesize)
