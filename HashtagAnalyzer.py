def HastagAnalyzer():
    import pandas as pd
    import SentimentAnalyzer as SA
    import re

    df = pd.read_csv('tweets.csv')
    clean_text1 = df['Tweets'].tolist()

    clean_text2 = []

    for sentence in clean_text1:
        clean_text2.append(SA.remove_emojis(sentence))

    clean_text3 = []

    for sentence in clean_text2:
        clean_text3.append(SA.removehtml(sentence))

    clean_text4 = []

    for sentence in clean_text3:
        clean_text4.append(re.sub(r'[^\w\s]', '', sentence))

    clean_text5 = []

    for sentence in clean_text4:
        clean_text5.append(SA.to_low(sentence))

    clean_text6 = []

    for sentence in clean_text5:
        clean_text6.append(SA.predict(sentence))

    return clean_text6
