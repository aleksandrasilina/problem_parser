import pytest
import pytest_asyncio
from aiogram.fsm.storage.memory import MemoryStorage

from tests.test_tg_bot.mocked_bot import MockedBot


@pytest_asyncio.fixture(scope="session")
async def storage():
    tmp_storage = MemoryStorage()
    try:
        yield tmp_storage
    finally:
        await tmp_storage.close()


@pytest.fixture()
def bot():
    return MockedBot()
