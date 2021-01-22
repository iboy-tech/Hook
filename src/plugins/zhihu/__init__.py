from nonebot import on_command

from nonebot.adapters.cqhttp import Message

# from nonebot.rule import to_me

from nonebot.typing import Bot, Event
import httpx

zhihu = on_command("zhihu", aliases=set(["知乎", "知乎日报"]), block=True)


@zhihu.handle()
async def handle(bot: Bot, event: Event, state: dict):
    STORY_URL_FORMAT = "https://daily.zhihu.com/story/{}"
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://news-at.zhihu.com/api/4/news/latest")
        data = resp.json()
        stories = data.get("stories")
        if not stories:
            await zhihu.send(Message("暂时没有数据，或者服务无法访问"))
            return
        reply = ""
        for story in stories:
            url = STORY_URL_FORMAT.format(story["id"])
            title = story.get("title", "未知内容")
            reply += f"\n{title}\n{url}\n"
        await zhihu.send(Message(reply.strip()))
