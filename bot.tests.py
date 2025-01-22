import asyncio

from src.scrappy.bot import BOTScrapy
from src.scrappy.sites import (
    BAI,
    BCA,
    BCI,
    BFA,
    BIR,
    BNI,
    BPC,
    SOL,
    CaixaAngola,
    Keve,
    StandardBank,
)

bot = BOTScrapy(
    [BAI]
)

if __name__ == '__main__':
    asyncio.run(bot.run_scrapy())
