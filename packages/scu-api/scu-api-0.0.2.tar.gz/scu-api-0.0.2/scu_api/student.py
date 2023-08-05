# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from typing import Callable, Optional, NoReturn
from .constant import API_ReturnType


class SCUStudent(metaclass=ABCMeta):
    @abstractmethod
    def session_valid_required(func: Callable):
        '''
        装饰器，用于确保session有效
        '''

    @abstractmethod
    def set_baseinfo(self, stid: str, passwd: str, hashed: Optional[bool] = False) -> NoReturn:
        '''
        @brief 设置学生的基本信息，用于登陆
        @param[in] stid(str)    学号
        @param[in] passwd(str)  密码
        @param[in] hashed(Optional[bool]) 密码是否已经过md5加密，默认False
        '''

    @abstractmethod
    def session_valid(self) -> bool:
        '''
        @brief 返回网站会话是否有效，在有效的情况下才可以获取个人信息
               如果session过期，则需要获取验证码重新登陆
        @param[out] valid(bool)  网站会话是否有效
        '''

    @abstractmethod
    def get_captcha(self, filepath: Optional[str] = None) -> API_ReturnType:
        '''
        @brief 获取验证码(base64编码字符串)
        @param[in]  filepath(str)  [可选的] 存储验证码图像的全路径，使用**.jpg**格式
        @param[out] _(API_ReturnType)
        '''

    @abstractmethod
    def login(self, catpcha: str, remember_me: Optional[bool] = True) -> API_ReturnType:
        '''
        @brief 模拟登陆
        @param[in] captcha(str) 通过get_captcha获取的验证码识别后的字符串
        @param[in] remember_me(Optional[bool]) [可选的]是否开启两周内快速登录，默认True
        @param[out] _(API_ReturnType) 
        '''

    @session_valid_required
    @abstractmethod
    def get_student_name(self) -> API_ReturnType:
        '''
        @brief 获取学生姓名
        @param[out] _(API_ReturnType)
        '''

    @session_valid_required
    @abstractmethod
    def get_student_pic(self, filepath: Optional[str] = None) -> API_ReturnType:
        '''
        @brief 获取学生照片(base64编码字符串)
        @param[in]  filepath(Optinal[str]) [可选的]存储图片的全路径，使用**.jpg**格式
        @param[out] _(API_ReturnType)
        '''
    
    @session_valid_required
    @abstractmethod
    def get_all_term_scores(self, pagesize: Optional[int] = -1) -> API_ReturnType:
        '''
        @brief 获取学生所有学期的成绩
        @param[in]  pagesize(Optional[int]) 最近多少门课的成绩，默认-1为取全部课成绩
        @param[out] _(API_ReturnType)
        '''
