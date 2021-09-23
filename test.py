from deep_translator import GoogleTranslator



to_translate = '有趣的休息室'
translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
# translated = GoogleTranslator(source='auto', target='de').translate(to_translate)
print(translated)