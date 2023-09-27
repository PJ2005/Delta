'''
import googletrans
translator = googletrans.Translator()
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/translate/<word>")
def translate(word):
    translation = translator.translate(word)
    out = [{"source-text": word}, {"translated-text-in-english": translation.text}]
    return jsonify(out)

@app.route("/detect/<word>")
def detect(word):
    source = (translator.detect(word)).lang
    op = [{"detected-lang": googletrans.LANGUAGES[source]}]
    return jsonify(op)
app.run()
'''

from flask import Flask, request, jsonify
import googletrans
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    sentence = data['sentence']
    dest_lang = data['dest_lang']
    translation = translator.translate(sentence, dest=dest_lang)
    out = [{"source-text": sentence}, {f"translated-text-in-{googletrans.LANGUAGES[translator.detect(sentence).lang]}": translation.text}]
    return jsonify(out)

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    sentence = data['sentence']
    detected_language = translator.detect(sentence).lang
    op = [{"detected-lang": googletrans.LANGUAGES[detected_language]}]
    return jsonify(op)

app.run()
