import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Конфигурация API Yandex GPT
YANDEX_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
YANDEX_API_KEY = "AQVNxY1miD1fgcIvyR5QuB2ruNhyOjUoFe73sRso"  # Замените на ваш API ключ

# Функция для получения ответа от Yandex GPT
def get_response(prompt):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVNxY1miD1fgcIvyR5QuB2ruNhyOjUoFe73sRso"
    }
    try:
        response = requests.post(YANDEX_API_URL, headers=headers, json=prompt)
        response.raise_for_status()  # Проверяем статус ответа
        result = response.json()
        print("Полный JSON-ответ:", result)  # Выводим полный JSON-ответ

        # Проверяем наличие ключей в ответе и получаем текст
        alternatives = result.get('result', {}).get('alternatives', [])
        if alternatives:
            text = alternatives[0].get('message', {}).get('text', 'Ошибка: ответ не содержит текст сообщения.')
            return text
        else:
            return 'Ошибка: ответ не содержит альтернатив.'
    except requests.exceptions.RequestException as e:
        print("Ошибка при отправке запроса:", e)
        return "Произошла ошибка при отправке запроса."
    except KeyError as e:
        print("Ошибка при обработке ответа:", e)
        return "Произошла ошибка при обработке ответа."

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Задайте ваш вопрос в банковской сфере, и я постараюсь ответить.')

# Обработчик сообщений от пользователя
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = update.message.text
    prompt = {
        "modelUri": "ds://bt17b4rdtmmlj7b2813v",
        "completionOptions": {
            "stream": False,
            "temperature": 0.1,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты ассистент помощник, который отвечает на вопросы в банковской сфере. Если вопрос не про банк, то пиши что не знаешь ответ"
            },
            {
                "role": "user",
                "text": question
            }
        ]
    }

    response = get_response(prompt)
    await update.message.reply_text(response)

# Основная функция
def main() -> None:
    # Вставьте сюда ваш токен
    application = Application.builder().token("6875000947:AAE833shKMDVODkJIhGXo-pFRrn7iNIaAEU").build()  # Замените на ваш токен Telegram бота

    # Обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
