import json
import re
from cat.mad_hatter.decorators import hook
from cat.log import log
from typing import Dict


@hook(priority=10)
def before_cat_reads_message(user_message_json: Dict, cat) -> Dict:
    # Detection tags

    settings = cat.mad_hatter.get_plugin().load_settings()

    tag1 = "@" + settings["tag_1"]
    tag2 = "@" + settings["tag_2"]
    tag3 = "@" + settings["tag_3"]

    query = user_message_json.text
    try:
        tag = re.search(r"^(@?\w+)", query).group(1)
    except Exception:
        tag = "|_|"

    if tag == tag1:
        cat.working_memory.tag = 1
        user_message_json.text = re.sub(r"^@(\w+)\s+", "", user_message_json.text)
    elif tag == tag2:
        cat.working_memory.tag = 2
        user_message_json.text = re.sub(r"^@(\w+)\s+", "", user_message_json.text)
    elif tag == tag3:
        cat.working_memory.tag = 3
        user_message_json.text = re.sub(r"^@(\w+)\s+", "", user_message_json.text)
    else:
        cat.working_memory.tag = 0

    log.info(f"Detected tag: {cat.working_memory.tag}")
    log.info(f"User message: {user_message_json.text}")

    # Detection user's message language

    language_selected = settings["language"]

    if language_selected == "AI detection":
        prompt_language = f"""Accurately determine the language of this given human message: '{user_message_json.text}'.
        Output the results only with the structure: {{"language":"detected_language"}} - example: {{"language":"English"}}."""
        language = cat.llm(prompt=prompt_language)

        try:
            cat.working_memory.language = json.loads(language)["language"]
            log.info(f"Detected language: {cat.working_memory.language}")
        except json.JSONDecodeError:
            cat.working_memory.language = "English"
            log.error(f"Error: Unable to detect language {language}")

    else:
        cat.working_memory.update({"language": language_selected})

    return user_message_json


@hook(priority=10)
def agent_prompt_prefix(prefix: str, cat) -> str:
    # Select the right prompt

    settings = cat.mad_hatter.get_plugin().load_settings()

    personality = settings["personality"]
    prompt1 = settings["prompt_1"]
    prompt2 = settings["prompt_2"]
    prompt3 = settings["prompt_3"]

    if cat.working_memory.tag == 1:
        prefix = f"""{prompt1}
        Answer the human with a focus on the following Context in {cat.working_memory.language} language."""

    if cat.working_memory.tag == 2:
        prefix = f"""{prompt2}
        Answer the human with a focus on the following Context in {cat.working_memory.language} language."""

    if cat.working_memory.tag == 3:
        prefix = f"""{prompt3}
        Answer the human with a focus on the following Context in {cat.working_memory.language} language."""

    if cat.working_memory.tag == 0:
        prefix = f"""{personality}
        Keep a balanced and smooth conversation with the human.
        If you need clarification to answer satisfactorily, ask a question to the human.
        Answer the human with a focus on the following Context in {cat.working_memory.language} language."""

    return prefix
