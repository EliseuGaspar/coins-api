import asyncio

from src.log import logg
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
    [BAI, SOL, BFA, BCI, BCA, BIR, BPC, BNI, Keve, CaixaAngola, StandardBank]
)


def run_bot():
    # print("Starting BOTScrappy...")
    logg.info_message("Starting BOTScrappy...")
    asyncio.run(bot.run_scrapy())


if __name__ == '__main__':
    asyncio.run(bot.run_scrapy())
