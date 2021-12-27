from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
# from sklearn.linear_model import LinearRegression
import pickle
# import pickle5 as pickle

# comando para instalar odas as dependencias no ambiante virtual venv usando requirements.txt
########################################
# pip install -r requirements.txt
########################################
colunas = ['tamanho','ano','garagem']
modelo = pickle.load(open('modelo.sav','rb'))


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'ernesto'
app.config['BASIC_AUTH_PASSWORD'] = 'teste'

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return "Minha primeira API."

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to='en')
    polaridade = tb_en.sentiment.polarity
    return f'polaridade: {polaridade}'

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])

app.run(debug=True)