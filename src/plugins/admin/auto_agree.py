from nonebot.log import logger
from nonebot import on_request
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import SUPERUSER, PRIVATE_FRIEND


friend_req = on_request(priority=5)


@friend_req.handle()
async def _(bot: Bot, event: Event, state: dict):
    if event.detail_type == "friend":
        logger.info("同意好友请求")
        # if event.detail_type == 'friend' and event.user_id in bot.config.superusers:
        await bot.set_friend_add_request(flag=event.id, approve=True)


group_invite = on_request(priority=5)


@group_invite.handle()
async def _(bot: Bot, event: Event, state: dict):
    if event.detail_type == "group" and event.sub_type == "invite":
        # if event.detail_type == 'group' and event.sub_type == 'invite' and event.user_id in bot.config.superusers:
        logger.info("同意加群请求")
        await bot.set_group_add_request(
            flag=event.raw_event["flag"], sub_type="invite", approve=True
        )

