import random

from utils import checks


class ReactionHandler:
    def __init__(self, reactions):
        self.eightball = reactions["eightball"]
        self.full_content_reactions = reactions["full_content_reactions"]

    async def handle_message(self, message):
        content = message.content.lower()

        if (content.startswith("racu ") or content.startswith("racu, ")) and content.endswith("?"):
            if await checks.eightball(message):
                response = random.choice(self.eightball)
                await message.reply(content=response)

        for trigger, response in self.full_content_reactions.items():
            if trigger.lower() == content:
                await message.reply(response)
