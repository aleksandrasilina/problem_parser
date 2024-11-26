from aiogram.types import Chat, User

TEST_USER = User(
    id=123, is_bot=False, first_name="Test", last_name="Bot", username="testbot"
)
TEST_USER_CHAT = Chat(
    id=12,
    type="private",
    first_name=TEST_USER.first_name,
    last_name=TEST_USER.last_name,
    username=TEST_USER.username,
)
