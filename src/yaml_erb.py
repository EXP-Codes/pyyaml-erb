#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# -----------------------------------------------

import os
import re
import numbers
import yaml


def load(stream) :
    '''
    对 yaml 的 safe_load 进行二次封装
    :param stream: yaml 文件读取流，例如 file.read()
    :return: yaml 配置字典
    '''
    settings = yaml.safe_load(stream)
    return _analyse_dict(settings)



def _analyse_dict(conf_dict) :
    '''
    递归解析字典值中的表达式
    :param conf_dict: 原始配置字典
    :return: 解析表达式后的配置字典
    '''
    result_dict = {}
    for key, val in conf_dict.items() :
        if isinstance(val, dict) :
            result_dict[key] = _analyse_dict(val)

        elif isinstance(val, list) :
            result_list = []
            for v in val :
                result_list.append(_analyse_expression(v))
            result_dict[key] = result_list

        else:
            result_dict[key] = _analyse_expression(val)
    return result_dict



def _analyse_expression(expression) :
    '''
    解析表达式
    :param expression: 表达式，格式形如 <%= ENV['JAVA_OME'] || 'default' %>
    :return: 解析表达式后的值
    '''
    if expression is None or isinstance(expression, numbers.Number) :
        return expression

    value = None
    mth = re.search(r'^<%=(.+)%>$', expression.strip())
    if mth :
        vals = re.split(r' \|\| | or ', mth.group(1))
        for val in vals :
            val = val.strip()
            mth = re.search(r'^ENV\[(.+)\]$', val)
            if mth :
                value = value or _analyse_environment(mth.group(1))
            else :
                value = value or _analyse_text(val)
    else :
        value = _analyse_text(expression)
    return value



def _analyse_environment(variable) :
    '''
    解析环境变量
    :param variable: 环境变量
    :return: 环境变量的值
    '''
    env_key = _remove_quotes(variable)
    return os.getenv(env_key)



def _analyse_text(text) :
    '''
    解析文本（若是数字类型会自动转换）
    :param text: 文本
    :return: 文本值
    '''
    mth = re.search(r'^(\d+\.\d+)$', text)
    if mth :
        val = float(mth.group(1))
    else :
        mth = re.search(r'^(\d+)$', text)
        if mth :
            val = int(mth.group(1))
        else :
            val = _remove_quotes(text)

    if val is not None and isinstance(val, str) :
        val = None if (val.lower() == 'none' or val.lower() == 'null' or val.lower() == 'nil') else val
    return val



def _remove_quotes(text) :
    '''
    移除文本两端的引号（双引号或单引号）
    :param text: 文本
    :return: 文本
    '''
    if text == '""' or text == "''" :
        text = ''
    else :
        mth = re.search(r'^[\'"](.+)["\']$', text)
        if mth :
            text = mth.group(1)
    return text


