# scu-api
提供与四川大学相关的信息接口

## Install

```bash
pip install scu-api
```

国内用户

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple scu-api
```

## API Format


Api返回类型：`API_Status`
```python
OK = 0
ERROR = 1
WARNING = 2
UNKNOWN = 3
```

通用Api返回类型：`API_ReturnType`
```python
{
    "status": API_Status,
    "result": Any  # API返回的有效内容，如果status不为OK，则返回内容为报错内容
}
```

使用示例：

```python
resp = some_api_method()

resp['status']        # 获取状态码(API_Status类型)，同resp.status
resp['status'].value  # 获取状态码对应的数字(int)，同resp.status.value
resp['result']        # 获取API返回的有效内容，同resp.result

resp.is_ok()          # 判断API返回状态是否正确(bool)
```


## Usage

获取本科生用户`U_Student`实例:

```python
import scu_api

# 默认为本科生
my_student = scu_api.get_student()

# 或指定本科生种类，目前只支持本科生一种
from scu_api.Student_Type import UNDERGRADUATE
my_student = scu_api.get_student(UNDERGRADUATE)
```

`U_Student`内置方法(目前为止)：
```python
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
    @brief 获取验证码
    @param[in]  filepath(str)  [可选的] 存储验证码图像的全路径，使用**.jpg**格式
    @param[out] _(API_ReturnType) 
        {
            'status': API_Status,
            'result': str # 验证码的base64编码字符串
        }
    '''

@abstractmethod
def login(self, catpcha: str, remember_me: Optional[bool] = True) -> API_ReturnType:
    '''
    @brief 模拟登陆
    @param[in] captcha(str) 通过get_captcha获取的验证码识别后的字符串
    @param[in] remember_me(Optional[bool]) [可选的]是否开启两周内快速登录，默认True
    @param[out] _(API_ReturnType) 
        {
            'status': API_Status,
            'result': None
        }
    '''

@session_valid_required
@abstractmethod
def get_student_name(self) -> API_ReturnType:
    '''
    @brief 获取学生姓名
    @param[out] _(API_ReturnType)
        {
            'status': API_Status,
            'result': str # 学生的姓名
        }
    '''

@session_valid_required
@abstractmethod
def get_student_pic(self, filepath: Optional[str] = None) -> API_ReturnType:
    '''
    @brief 获取学生照片
    @param[in]  filepath(Optinal[str]) [可选的]存储图片的全路径，使用**.jpg**格式
    @param[out] _(API_ReturnType)
        {
            'status': API_Status,
            'result': str # 学生照片的base64编码字符串
        }
    '''

@session_valid_required
@abstractmethod
def get_all_term_scores(self, pagesize: Optional[int] = -1) -> API_ReturnType:
    '''
    @brief 获取学生所有学期的成绩
    @param[in]  pagesize(Optional[int]) 最近多少门课的成绩，默认-1为取全部课成绩
    @param[out] _(API_ReturnType)
        {
            'status': API_Status,
            'result': dict # 教务处的学生成绩的原始json数据
        }
    '''
```

## Example

```python
# -*- coding: utf-8 -*-
import scu_api

bot = scu_api.get_student(scu_api.Student_Type.UNDERGRADUATE)

print('尝试请求', bot.get_student_name())

# 设置基础信息
bot.set_baseinfo('student_id', 'password')

# 获取验证码
resp = bot.get_captcha(filepath='captcha.jpg')
print('验证码请求', resp.is_ok())
captcha = input('输入验证码: ')

# 模拟登录
resp = bot.login(captcha, True)
print('登录', resp.is_ok())

resp = bot.get_student_name()
print('姓名', resp.result)

resp = bot.get_student_pic('student.jpg')
print('头像请求', resp.is_ok())

resp = bot.get_all_term_scores()
print('成绩请求', resp.is_ok())
print(resp.result)
```