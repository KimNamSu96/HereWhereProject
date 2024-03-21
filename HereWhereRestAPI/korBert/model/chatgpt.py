from openai import OpenAI
import os
import time


class Assistant():
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('OPEN_API_KEY')
        print(self.api_key)
        self.client = OpenAI(api_key=self.api_key)
        self.thread_id = None
        self.assistant_id = "asst_uc6NtiHSVwYVCBFmG82EGWSk"  # 챗봇 Assistant ID 설정

    def send_message(self, prompt):
        # 스레드 ID가 없이 새로운 스레드 생성
        thread = self.client.beta.threads.create()
        thread_id = thread.id

        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt
        )

        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
        )

        while run.status != "completed":
            time.sleep(1)
            run = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        messages = self.client.beta.threads.messages.list(thread_id=thread_id).data
        response = None
        for msg in reversed(messages):
            if msg.role == "assistant":
                response = msg.content[0].text.value
                break

        if response is None:
            response = "챗봇으로부터 응답이 없습니다."

        print("챗봇 응답:", response)

        return response

class AssistantSingleton:
    _instance = None
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Assistant()
        return cls._instance