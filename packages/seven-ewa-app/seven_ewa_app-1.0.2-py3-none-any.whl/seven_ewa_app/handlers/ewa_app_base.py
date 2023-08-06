# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-01-05 17:16:17
@LastEditTime: 2021-04-21 09:33:51
@LastEditors: SunYiTan
@Description: 
"""
from jwt import ExpiredSignatureError
from seven_framework.web_tornado.base_handler.base_api_handler import *

from seven_ewa_app.models.enum import AppBaseRedisKeyType
from seven_ewa_app.utils.json_util import JsonUtil
from seven_ewa_app.utils.jwt_util import JwtUtil
from seven_ewa_app.utils.redis_util import RedisUtil


class EwaAppBaseHandler(BaseApiHandler):
    """
    :description: 客户端基类
    """

    def options_async(self):
        self.reponse_json_success()

    def check_xsrf_cookie(self):
        return

    def set_default_headers(self):
        allow_origin_list = config.get_value("allow_origin_list")
        origin = self.request.headers.get("Origin")
        if origin in allow_origin_list:
            self.set_header("Access-Control-Allow-Origin", origin)

        self.set_header("Access-Control-Allow-Headers",
                        "Origin,X-Requested-With,Content-Type,Accept,User-Token,Manage-ProductID,Manage-PageID,PYCKET_ID")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")
        self.set_header("Access-Control-Allow-Credentials", "true")

    def prepare_ext(self):
        """
        置于任何请求方法前被调用扩展
        :return:
        :last_editors: SunYiTan
        """
        http_log = config.get_value("http_log")
        if http_log and http_log is True:
            if "Content-Type" in self.request.headers and self.request.headers["Content-type"].lower().find(
                    "application/json") >= 0 and self.request.body:
                request_params = json.loads(self.request.body)
            else:
                request_params = self.request.arguments

            self.logging_link_info(
                f"--- request: {self.request.path} ---:\n{JsonUtil.dumps(request_params)}")

    def write_error(self, status_code, **kwargs):
        """
        :Description: 重写全局异常事件捕捉
        :last_editors: ChenXiaolei
        """
        self.logger_error.error(
            traceback.format_exc(),
            extra={"extra": {
                "request_code": self.request_code
            }})

        self.set_status(200)
        return self.reponse_json_error("SystemError", "对不起，系统发生错误")

    def http_reponse(self, content, log_extra_dict=None):
        """
        :description: 将字符串返回给客户端
        :param content: 内容字符串
        :param log_extra_dict:
        :return: 将字符串返回给客户端
        :last_editors: SunYiTan
        """
        http_log = config.get_value("http_log")
        if http_log and http_log is True:
            self.logging_link_info(f"--- response: {self.request.path} ---:\n{content}")

        super().http_reponse(content, log_extra_dict)

    def reponse_json_success(self, data=None, desc='调用成功'):
        """
        :description: 通用成功返回json结构
        :param data: 返回结果对象，即为数组，字典
        :param desc: 字符串，服务端返回的错误信息
        :return: 将dumps后的数据字符串返回给客户端
        :last_editors: HuangJingCan
        """
        self.reponse_common("0", desc, data)

    def reponse_json_error(self, error_code="", error_message="", data=None, log_type=0):
        """
        :description: 通用错误返回json结构
        :param error_code: 字符串，调用失败（success为false）时，服务端返回的错误码
        :param error_message: 字符串，调用失败（success为false）时，服务端返回的错误信息
        :param data: 返回结果对象，即为数组，字典
        :param log_type: 日志记录类型（0-不记录，1-info，2-error）
        :return: 将dumps后的数据字符串返回给客户端
        :last_editors: HuangJianYi
        """
        if log_type == 1:
            self.logging_link_info(f"{error_code}\n{error_message}\n{data}\n{self.request}")
        elif log_type == 2:
            self.logging_link_error(f"{error_code}\n{error_message}\n{data}\n{self.request}")

        self.reponse_common(error_code, error_message, data)

    def reponse_common(self, result, desc, data=None, log_extra_dict=None):
        """
        :Description: 输出公共json模型
        :param result: 返回结果标识
        :param desc: 返回结果描述
        :param data: 返回结果对象，即为数组，字典
        :param log_extra_dict:
        :return: 将dumps后的数据字符串返回给客户端
        :last_editors: SunYiTan
        """
        template_value = {
            'result': result,
            'desc': desc,
            'data': data}

        self.http_reponse(JsonUtil.dumps(template_value), log_extra_dict)

    def get_param(self, param_name, default="", strip=True):
        """
        :Description: 二次封装获取参数
        :param param_name: 参数名
        :param default: 如果无此参数，则返回默认值
        :param strip:
        :return: 参数值
        :last_editors: SunYiTan
        """
        param_ret = ""

        try:
            if "Content-Type" in self.request.headers and \
                    self.request.headers["Content-type"].lower().find("application/json") >= 0 and \
                    self.request.body:
                json_params = json.loads(self.request.body)
                param_ret = json_params.get(param_name, default)
            else:
                param_ret = self.get_argument(param_name, default, strip=strip)

        except Exception as e:
            self.logging_link_error(traceback.format_exc())

        if param_ret == "":
            param_ret = default

        return param_ret

    def get_int_param(self, param_name, default="", strip=True):
        """
        二次封装获取参数，转换成int类型
        :param param_name: 参数名
        :param default: 如果无此参数，则返回默认值
        :param strip:
        :return: 参数值
        :last_editors: SunYiTan
        """
        param_ret = self.get_param(param_name, default, strip)
        try:
            return int(param_ret)
        except ValueError:
            pass

        return 0

    @staticmethod
    def get_condition_by_id_list(primary_key, id_list=None):
        """
        :description: 根据id_list返回查询条件
        :param primary_key：主键
        :param id_list：id：列表
        :return: 查询条件字符串
        :last_editors: HuangJingCan
        """
        if not id_list:
            return ""
        id_list_str = str(id_list).strip('[').strip(']')
        return f"{primary_key} IN({id_list_str})"

    @staticmethod
    def create_user_token(user_id: int, third_auth_id: int):
        """
        生成token
        :param user_id:
        :param third_auth_id:
        :return:
        """
        jwt_secret = config.get_value("jwt_secret")
        jwt_expire = config.get_value("jwt_expire")

        user_info = {
            "user_id": user_id,
            "third_auth_id": third_auth_id
        }

        token = JwtUtil.create_token(JsonUtil.dumps(user_info), jwt_secret, jwt_expire)

        # 刷新缓存
        if user_id > 0:
            key = AppBaseRedisKeyType.UserToken.value + str(user_id)
            RedisUtil().set(key, token, jwt_expire * 24 * 60 * 60)
        else:
            key = AppBaseRedisKeyType.ThirdToken.value + str(third_auth_id)
            RedisUtil().set(key, token, jwt_expire * 24 * 60 * 60)

        return token

    def request_header_token(self):
        header_token = {}
        if "User-Token" in self.request.headers:
            req_info_list = str.split(self.request.headers["User-Token"], ";")
            for info in req_info_list:
                kv = str.split(info, "=")
                header_token[kv[0]] = kv[1]
        return header_token

    def get_user_info(self):
        """
        获取请求的玩家信息
        :return:
        """
        header_token = self.request_header_token()
        user_token = header_token.get("UserToken", "")
        jwt_secret = config.get_value("jwt_secret")

        if not user_token:
            return {"user_id": 0, "third_auth_id": 0}

        user_info = JwtUtil.get_user_info_from_token(user_token, jwt_secret)
        return json.loads(user_info)


def login_filter(is_check_bind=True):
    """
    :description: 头部过滤装饰器 仅限handler使用
    :param is_check_bind: 是否开启手机号绑定校验
    :last_editors: SunYiTan
    """

    def wrapper(handler):
        def _wrapper(self, **kwargs):
            try:
                header_token = self.request_header_token()
                user_token = header_token.get("UserToken", "")
                jwt_secret = config.get_value("jwt_secret")

                if not user_token:
                    self.logging_link_error(f"--- 头部验证信息为空: {self.request.path} : {self.request.headers}")
                    return self.reponse_json_error("TokenEmpty", "对不起，获取验证信息失败")

                user_info = JwtUtil.get_user_info_from_token(user_token, jwt_secret)
                user_info = json.loads(user_info)
                user_id = user_info.get("user_id", 0)
                third_auth_id = user_info.get("third_auth_id", 0)

                if is_check_bind is True and user_id <= 0:
                    return self.reponse_json_error("UnboundTelephone", "对不起，请先绑定手机号")

                if user_id > 0:
                    key = AppBaseRedisKeyType.UserToken.value + str(user_id)
                    old_token = RedisUtil().get(key)
                else:
                    key = AppBaseRedisKeyType.ThirdToken.value + str(third_auth_id)
                    old_token = RedisUtil().get(key)
                if not old_token or old_token != user_token:
                    return self.reponse_json_error("LoginOther", "对不起，账号在其他地方登录")

            except ExpiredSignatureError as ex:
                self.logging_link_error(str(ex) + "【登录超时】")
                return self.reponse_json_error("ExpiredSignatureError", "登录已过期，请重新进入小程序")

            except Exception as ex:
                self.logging_link_error(traceback.format_exc())
                return self.reponse_json_error("Error", "服务端错误")

            return handler(self, **kwargs)

        return _wrapper

    return wrapper
