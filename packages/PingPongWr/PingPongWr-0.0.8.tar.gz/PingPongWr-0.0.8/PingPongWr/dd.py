import PingPongWr
import asyncio

Ping = PingPongWr.Connect("https://builder.pingpong.us/api/builder/60bb877ae4b091a94bc7eb3c/integration/v0.2/custom/{sessionId}", "Basic a2V5OjY3ZjA2NTQ1N2VlNzc2ZDMyZGMzZmUxODBmNTI4NjIy")

async def Example(): # 비동기식 함수
    str_text = input("나: ")  # 대화할 말 입력받기
    return_data = await Ping.Pong(session_id = "12312321", text = str_text, dialog=True) # 핑퐁빌더 API에 Post 요청

    print(return_data) # {"text": "안녕안녕입니다", "topic": None, "Image": None}

asyncio.run(Example())  # 비동기로 함수 실행