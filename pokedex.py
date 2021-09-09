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
    pokemon = Pokemon(request.form["pokemon"].lower(), "", "", "", "", "", "", "")
    try:
        req = json.loads(requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon.nome}/').text)
        if request.form.get('shiny'):
            pokemon.foto = req['sprites']['front_shiny']
            pokemon.foto2 = req['sprites']['back_shiny']
        else:
            pokemon.foto = req['sprites']['front_default']
            pokemon.foto2 = req['sprites']['back_default']

        if len(req["types"]) == 2:
            pokemon.tipo1 = req['types'][0]['type']['name']
            pokemon.tipo2 = req['types'][1]['type']['name']
        else:
            pokemon.tipo1 = req['types'][0]['type']['name']

        res = req['height']
        pokemon.altura = dot_hight(res)

        res = req['weight']
        pokemon.peso = dot_weight(res)

        golpes = []
        level = []
        level_golpe = []
        for i in range(0, len(req['moves'])):
            golpes.append(req['moves'][i]['move']['name'])
            level.append(req['moves'][i]['version_group_details'][0]['level_learned_at'])
            result = '{} : {}'.format(level[i], golpes[i])
            level_golpe.append(result)
        pokemon.golpes = sorted(level_golpe)
        #ipdb.set_trace()
    except:
        return 'Pokemon nao encontrado'
    return render_template("index.html",
                           nome=pokemon.nome.upper(),
                           foto=pokemon.foto,
                           foto2=pokemon.foto2,
                           tipo1=pokemon.tipo1.upper(),
                           tipo2=pokemon.tipo2.upper(),
                           altura=pokemon.altura,
                           peso=pokemon.peso,
                           golpes=pokemon.golpes)


def dot_hight(num):
    u = num // 1 % 10
    resto = num // 10
    return '{}.{}m'.format(resto, u)


def dot_weight(num):
    u = num // 1 % 10
    resto = num // 10
    return '{}.{}kg'.format(resto, u)


if __name__ == '__main__':
    app.run(debug=True)
