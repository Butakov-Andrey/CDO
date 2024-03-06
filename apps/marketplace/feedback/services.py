import json
import time

import config
import models
import openai
from loguru import logger

openai.api_key = config.settings.VSEGPT_API_KEY
openai.api_base = config.settings.VSEGPT_BASE_URL


def generate_text(
    model: str,
    system_prompt: str = "",
    prompt: str = "",
    answer_prompt: str = "",
):

    s_prompt = [{"role": "system", "content": system_prompt}]
    u_prompt = [{"role": "user", "content": prompt}]
    a_prompt = [{"role": "system", "content": answer_prompt}]

    messages = s_prompt + u_prompt + a_prompt

    for attempt in range(3):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=config.gpt_settings.TEMPERATURE,
                n=config.gpt_settings.N,
                max_tokens=config.gpt_settings.MAX_TOKENS,
            )
            text = response["choices"][0]["message"]["content"]
            return text, True

        except Exception as e:
            if "430" in str(e):
                logger.warning(
                    f"Error 430 occurred on attempt {attempt}. Retrying after 2 second..."
                )
                time.sleep(2)
            elif "429" in str(e):
                logger.warning(
                    f"Error 429 occurred on attempt {attempt}. Retrying after 2 second..."
                )
                time.sleep(2)
            else:
                logger.error(e)
                time.sleep(2)
    else:
        return "Attempts are over.", False


def get_sentiment_for_feedback(text: str):
    start_index = text.find("{")
    end_index = text.rfind("}")
    sentiment = text[start_index : end_index + 1]
    json_sentiment = json.loads(sentiment)
    return json_sentiment


def check_sentiment(text: str):
    answer, success = generate_text(
        model=config.gpt_settings.MODEL,
        system_prompt=config.prompts.SYSTEM_PROMPT,
        prompt=text,
        answer_prompt=config.prompts.ANSWER_PROMPT,
    )
    if success:
        sentiment_value = get_sentiment_for_feedback(answer).get("sentiment")
        if sentiment_value and hasattr(models.Sentiments, sentiment_value.upper()):
            sentiment = getattr(models.Sentiments, sentiment_value.upper())
            return sentiment
    return models.Sentiments.NEUTRAL
