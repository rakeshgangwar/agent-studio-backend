from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
from app.services.supabase_service import supabase_service


class SupabaseChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str):
        self.session_id = session_id

    def add_message(self, message: BaseMessage) -> None:
        supabase_service.client.table('chat_sessions').update({
            'messages': supabase_service.client.table('chat_sessions')
                        .select('messages')
                        .eq('id', self.session_id)
                        .single()
                        .execute()
                        .data['messages'] + [message_to_dict(message)]
        }).eq('id', self.session_id).execute()

    def clear(self) -> None:
        supabase_service.client.table('chat_sessions').update({
            'messages': []
        }).eq('id', self.session_id).execute()

    @property
    def messages(self) -> List[BaseMessage]:
        result = supabase_service.client.table('chat_sessions').select('messages').eq('id',
                                                                                      self.session_id).single().execute()
        return messages_from_dict(result.data['messages'])
