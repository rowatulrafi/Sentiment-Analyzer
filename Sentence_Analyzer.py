def SentenceAnalyzer(text):
    import re
    import SentimentAnalyzer as SA

    clean_text1 = SA.remove_emojis(text)
    clean_text2 = SA.removehtml(clean_text1)
    clean_text3 = re.sub(r'[^\w\s]', '', clean_text2)
    clean_text4 = SA.to_low(clean_text3)

    return SA.predict(clean_text4)