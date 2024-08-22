from langchain_community.chat_message_histories import PostgresChatMessageHistory

history = PostgresChatMessageHistory(
    connection_string="postgresql://user:password@localhost:5432/db",
    session_id="session_id",
)