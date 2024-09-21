from .client import client


async def qna(question: str, context: list[str]) -> str | None:

    res = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                你是問答任務的助手。使用以下檢索到的上下文來回答問題。
                如果不知道答案，就說 '不知道'。
                最多使用三個句子並保持答案簡潔。
                """,
            },
            {
                "role": "user",
                "content": f'''
                Context: {'\n'.join(context)}
                Question: {question}
                Answer:
                ''',
            },
        ],
    )

    return res.choices[0].message.content
