# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : __init__.py.py
@Time    : 2021/1/7 15:18
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description :
@Software: PyCharm
"""
""" 翻译
"""
from nonebot import on_command
from nonebot.typing import Bot, Event
import  requests 
import  re

translate_cmd= on_command("translate", aliases={"翻译","中译英"}, block=True)
translate_cmd.__doc__ = """
translate 翻译
"""


@translate_cmd.handle()
async def _(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()
    if args:
        state["content"] = args


@translate_cmd.got("content", prompt="您想翻译成英文的语句是？")
async def _(bot: Bot, event: Event, state: dict):
    args = state["content"]
    print("要翻译的句子", args)
    translate_res = await get_translate(args) #将待翻译的语句传给翻译函数
    await translate_cmd.finish(translate_res)
 
async def get_translate(message): #异步的翻译函数
	translate_sentence = get_content(message)
	return translate_sentence

def get_content(message): #翻译功能
	url = 'http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i='+message #有道的免费api
	res = requests.get(url) #爬取json格式的网页
	text = res.text 
	result = re.findall('"tgt":.*"',text)[0].split('"')[3] #用正则表达式提取翻译后的语句
	return result

@translate_cmd.args_parser
async def _(bot: Bot, event: Event, state: dict):
    args = str(event.message).strip()
    if not args:
        await translate_cmd.reject("要翻译的不能为空呢，请重新输入")
    state[state["_current_key"]] = args
