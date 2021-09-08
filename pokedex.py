from flask.globals import request
from flask import Flask, render_template
from models.pokemon import Pokemon
import json
import requests
import ipdb


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    pokemon = Pokemon(request.form["pokemon"].lower(), "", "")
    try:
        req = json.loads(requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon.nome}/').text)
        result = req["sprites"]["front_default"]
        result2 = req["sprites"]["front_shiny"]
        pokemon.foto = result
        pokemon.shiny = result2
        #ipdb.set_trace()

    except:
        return "Pokemon nao encontrado"
    return render_template("index.html", nome=pokemon.nome, foto=pokemon.foto, foto2=pokemon.shiny)




if __name__ == '__main__':
    app.run(debug=True)