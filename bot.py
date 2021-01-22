from pathlib import Path

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init()


driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
app = nonebot.get_asgi()



# 添加额外的配置
config = nonebot.get_driver().config
config.home_dir_path = Path().resolve()
# 插件数据目录
config.data_dir_path = config.home_dir_path / "data"

# 自定义 logger
from nonebot.log import default_format, logger


logger.add(config.data_dir_path / "logs" / "error.log",
           rotation="00:00",
           retention='1 day',
           diagnose=False,
           level="ERROR",
           format=default_format,
           encoding='utf-8'
)

# 加载外部插件
nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_plugin('haruka_bot')


# 加载开发环境插件
if config.debug:
    nonebot.load_plugin("nonebot_plugin_test")
# 加载自己的插件
nonebot.load_plugins("src/plugins")

if __name__ == "__main__":
    nonebot.run(app="bot:app")
