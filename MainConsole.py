from tkinter import *
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt

#Console Configuration
root = Tk()

root.title("Sentiment Analyzer - Twitter")

p1 = PhotoImage(file='icon.png')
root.iconphoto(False, p1)
root.geometry("600x500")
root.resizable(width=False, height=False)
bg_image = PhotoImage(file='bgimage.PNG')

my_canvas = Canvas(root, width=600, height=500, bd=0, highlightthickness=0)
my_canvas.pack(fill="both", expand=True)
my_canvas.create_image(0, 0, image=bg_image, anchor="nw")

#Console Text
my_canvas.create_text(300, 150, text="Welcome to Sentiment Analysis", font=("Helvetica", 20), fill="black")

#emo image import

angryemo = ImageTk.PhotoImage(Image.open("angry.PNG"))
happyemo = ImageTk.PhotoImage(Image.open("happy.PNG"))
neutralemo = ImageTk.PhotoImage(Image.open("neutral.PNG"))


def TA():
    ta_window = Toplevel(root)
    ta_window.geometry("600x500")
    ta_window.title("Hashtag Analysis")
    ta_window.resizable(width=False, height=False)

    ta_window.iconphoto(False, p1)

    canta = Canvas(ta_window, width=600, height=500, bd=0, highlightthickness=0)
    canta.pack(fill="both", expand=True)
    canta.create_image(0, 0, image=bg_image, anchor="nw")

    canta.create_text(300, 200, text="Enter your hashtag", font=("Helvetica", 20), fill="black", tags="destroy")

    def analyze():
        text = entry.get()
        canta.delete("destroy")
        entry.destroy()
        button.destroy()
        import Twitter_streamer as TS
        TS.twitterStreamer(text)
        import HashtagAnalyzer as HA
        result = HA.HastagAnalyzer()
        plot = []
        for senti in result:
            if senti['label'] == "POSITIVE":
                plot.append('POSITIVE')
            elif senti['label'] == "NEGATIVE":
                plot.append('NEGATIVE')
            else:
                plot.append('NEUTRAL')
        labels, counts = np.unique(plot, return_counts=True)
        ticks = range(len(counts))
        plt.bar(ticks, counts, align='center')
        plt.xticks(ticks, labels)
        plt.show()


    button = Button(ta_window, text="Enter", command=analyze)
    button_window = canta.create_window(275, 300, anchor="nw", window=button)

    entry = Entry(ta_window, font=("Helvetica", 15), width=20, fg="#336d92", bd=0)
    entry_window = canta.create_window(190, 250, anchor="nw", window=entry)
    ta_window.bind('<Return>', lambda event: analyze())


def SA():
    sa_window = Toplevel(root)
    sa_window.geometry("600x500")
    sa_window.title("Sentence Analysis")
    sa_window.resizable(width=False, height=False)

    sa_window.iconphoto(False, p1)

    cansa = Canvas(sa_window, width=600, height=500, bd=0, highlightthickness=0)
    cansa.pack(fill="both", expand=True)
    cansa.create_image(0, 0, image=bg_image, anchor="nw")

    cansa.create_text(300, 200, text="Enter your Sentence", font=("Helvetica", 20), fill="black", tags="destroy")

    def analyze():
        text = entry.get()
        cansa.delete("destroy")
        entry.destroy()
        button.destroy()
        import Sentence_Analyzer
        result = Sentence_Analyzer.SentenceAnalyzer(text)

        cansa.create_text(300, 150, text=result, font=("Helvetica", 15), fill="black")

        if result['label'] == "POSITIVE":
            cansa.create_image(275, 200, image=happyemo, anchor="nw")
        elif result['label'] == "NEGATIVE":
            cansa.create_image(275, 200, image=angryemo, anchor="nw")
        else:
            cansa.create_image(275, 200, image=neutralemo, anchor="nw")


    button = Button(sa_window, text="Enter", command=analyze)
    button_window = cansa.create_window(275, 300, anchor="nw", window=button)

    entry = Entry(sa_window, font=("Helvetica", 15), width=20, fg="#336d92", bd=0)
    entry_window = cansa.create_window(190, 250, anchor="nw", window=entry)
    sa_window.bind('<Return>', lambda event: analyze())

b1 = Button(root, text="Analyze using twitter hashtags", command=TA)
b2 = Button(root, text="Analyze a Sentence", command=SA)

b1_window = my_canvas.create_window(100, 200, anchor="nw", window=b1)
b2_window = my_canvas.create_window(350, 200, anchor="nw", window=b2)

root.mainloop()