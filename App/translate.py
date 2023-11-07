from deep_translator import GoogleTranslator

def translate(language, text):
    translator = GoogleTranslator(source='auto', target=language)
    translation = translator.translate(text=text)
    return translation