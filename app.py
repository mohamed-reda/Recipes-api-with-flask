from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

recipes = [
    {
        'id': 1,
        'name': 'Egg Salad',
        'description': 'This is a lovely egg salad recipe.'
    },
    {
        'id': 2,
        'name': 'Tomato Pasta',
        'description': 'This is a lovely tomato pasta recipe.'
    }
]


@app.route('/', methods=['GET'])
def get_hello():
    return 'Hello Crocodile'


@app.route('/recipes', methods=['GET'])
def get_recipes():
    # jsonify converts objects (such as a list) to JSON format.
    return jsonify({'data': recipes})


@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    # recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)
    recipe = {}
    for one_recipe in recipes:
        if one_recipe['id'] == recipe_id:
            recipe = one_recipe
            break
    else:
        recipe = None

    if recipe:
        return jsonify(recipe)

    return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND


@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')

    recipe = {
        'id': len(recipes) + 1,
        'name': name,
        'description': description
    }

    recipes.append(recipe)

    return jsonify(recipe), HTTPStatus.CREATED


@app.route('/morerecipes', methods=['POST'])
def create_more_recipes():
    data = request.get_json()
    recipe = {}
    for i in data:
        name = i.get('name')
        description = i.get('description')
        recipe = {
            'id': len(recipes) + 1,
            'name': name,
            'description': description
        }
        recipes.append(recipe)

    return jsonify(data), HTTPStatus.CREATED


@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
# The last recipe_id should have the same name of the next parameter
def update_recipe(recipe_id):
    
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)

    if not recipe:
        return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

    data = request.get_json()

    recipe.update(
        {
            'name': data.get('name'),
            'description': data.get('description')
        }
    )

    return jsonify(recipe)


if __name__ == '__main__':
    app.run()
