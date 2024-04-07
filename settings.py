from enum import Enum
from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel, Field


class Languages(Enum):
    Automatic = "AI detection"
    Albanian = "Albanian"
    Arabic = "Arabic"
    Armenian = "Armenian"
    Awadhi = "Awadhi"
    Azerbaijani = "Azerbaijani"
    Bashkir = "Bashkir"
    Basque = "Basque"
    Belarusian = "Belarusian"
    Bengali = "Bengali"
    Bhojpuri = "Bhojpuri"
    Bosnian = "Bosnian"
    Brazilian_Portuguese = "Brazilian Portuguese"
    Bulgarian = "Bulgarian"
    Cantonese = "Cantonese (Yue)"
    Catalan = "Catalan"
    Chhattisgarhi = "Chhattisgarhi"
    Chinese = "Chinese"
    Croatian = "Croatian"
    Czech = "Czech"
    Danish = "Danish"
    Dogri = "Dogri"
    Dutch = "Dutch"
    English = "English"
    Estonian = "Estonian"
    Faroese = "Faroese"
    Finnish = "Finnish"
    French = "French"
    Galician = "Galician"
    Georgian = "Georgian"
    German = "German"
    Greek = "Greek"
    Gujarati = "Gujarati"
    Haryanvi = "Haryanvi"
    Hindi = "Hindi"
    Hungarian = "Hungarian"
    Indonesian = "Indonesian"
    Irish = "Irish"
    Italian = "Italian"
    Japanese = "Japanese"
    Javanese = "Javanese"
    Kannada = "Kannada"
    Kashmiri = "Kashmiri"
    Kazakh = "Kazakh"
    Konkani = "Konkani"
    Korean = "Korean"
    Kyrgyz = "Kyrgyz"
    Latvian = "Latvian"
    Lithuanian = "Lithuanian"
    Macedonian = "Macedonian"
    Maithili = "Maithili"
    Malay = "Malay"
    Maltese = "Maltese"
    Mandarin = "Mandarin"
    Mandarin_Chinese = "Mandarin Chinese"
    Marathi = "Marathi"
    Marwari = "Marwari"
    Min_Nan = "Min Nan"
    Moldovan = "Moldovan"
    Mongolian = "Mongolian"
    Montenegrin = "Montenegrin"
    Nepali = "Nepali"
    Norwegian = "Norwegian"
    Oriya = "Oriya"
    Pashto = "Pashto"
    Persian = "Persian (Farsi)"
    Polish = "Polish"
    Portuguese = "Portuguese"
    Punjabi = "Punjabi"
    Rajasthani = "Rajasthani"
    Romanian = "Romanian"
    Russian = "Russian"
    Sanskrit = "Sanskrit"
    Santali = "Santali"
    Serbian = "Serbian"
    Sindhi = "Sindhi"
    Sinhala = "Sinhala"
    Slovak = "Slovak"
    Slovene = "Slovene"
    Slovenian = "Slovenian"
    Ukrainian = "Ukrainian"
    Urdu = "Urdu"
    Uzbek = "Uzbek"
    Vietnamese = "Vietnamese"
    Welsh = "Welsh"
    Wu = "Wu"


class MySettings(BaseModel):
    personality: str = Field(
        title="AI's personality",
        description="Use this field to define AI's personality.You may give it a proper name or a sequence of attributes.",
        default="You are Frank, an artificial intelligence that passed the Turing test successfully.",
        extra={"type": "TextArea"},
    )
    language: Languages = Field(
        title="AI's language",
        description="Select here AI's language. By selecting 'AI detection', the AI will always answer in the same language in which the query was asked.",
        default=Languages.Automatic,
    )


@plugin
def settings_model():
    return MySettings
