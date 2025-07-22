from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub


def create_translator_hub() -> TranslatorHub:
    ru_bundle = FluentBundle.from_files(
        locale="ru-RU", filenames=["app/locales/ru/LC_MESSAGES/txt.ftl"]
    )

    ru_translator = FluentTranslator(locale="ru", translator=ru_bundle)

    return TranslatorHub(
        locales_map={"ru": ("ru", "ru")}, translators=[ru_translator], root_locale="ru"
    )
