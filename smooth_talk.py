import json
from cat.mad_hatter.decorators import hook
from cat.log import log
from typing import Dict


@hook(priority=10)
def before_cat_reads_message(user_message_json: Dict, cat) -> Dict:
    # Detection user's message language

    settings = cat.mad_hatter.get_plugin().load_settings()
    language_selected = settings["language"]

    if language_selected == "AI detection":
        prompt_language = f"""Accurately determine the language of this given human message: '{user_message_json['text']}'.
        Output the results only in the standardized JSON format, with the structure: {{"language":"detected_language"}} - example {{"language":"English"}}."""
        language = cat.llm(prompt=prompt_language)

        try:
            cat.working_memory.update(json.loads(language))
            log.info(f"Detected language: {cat.working_memory['language']}")
        except json.JSONDecodeError:
            cat.working_memory.update({"language": "English"})
            log.error(f"Error: Unable to detect language {language}")

    else:
        cat.working_memory.update({"language": language_selected})

    return user_message_json


@hook(priority=10)
def agent_prompt_prefix(prefix: str, cat) -> str:
    # Main prompt

    settings = cat.mad_hatter.get_plugin().load_settings()
    personality = settings["personality"]

    prefix = f"""{personality}
    Keep a balanced and smooth conversation with the human.
    If you need clarification to answer satisfactorily, ask a question to the human.
    Answer the human with a focus on the following Context in {cat.working_memory['language']} language."""
    return prefix
