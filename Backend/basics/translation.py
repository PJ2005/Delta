#To implement a language translator
import googletrans
translator = googletrans.Translator()
code = googletrans.LANGUAGES

def translation(n):

    c1 = input("Would you like to enter source language(Y/N): ")

    if c1.lower() == 'y':
        source = input("Enter source language code: ")

    else:
        source = (translator.detect(n)).lang
        print("The sentence is in: ", code[source])

    c2 = input("Any preferred destination language code(Y/N): ")
    if c2.lower() == 'y':
        pref = input("Enter preferred language code(if any): ")
    else:
        pref = 'en'


        t = translator.translate(n, dest = pref, src = source)
        print("The sentence in ", code[pref], "is: ", t.text)

n = input("Enter sentence: ")
(translation(n))