from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# Sample constellation data
constellations = [
    {'id': 1, 'name': 'Orion', 'hemisphere': 'Northern', 'main_stars': ['Betelgeuse', 'Rigel', 'Bellatrix'], 'area': 594, 'origin': 'Greek'},
    {'id': 2, 'name': 'Scorpius', 'hemisphere': 'Southern', 'main_stars': ['Antares', 'Shaula', 'Sargas'], 'area': 497, 'origin': 'Greek'},
    {'id': 3, 'name': 'Ursa Major', 'hemisphere': 'Northern', 'main_stars': ['Dubhe', 'Merak', 'Phecda'], 'area': 1280, 'origin': 'Greek'},
    {'id': 4, 'name': 'Cassiopeia', 'hemisphere': 'Northern', 'main_stars': ['Schedar', 'Caph', 'Ruchbah'], 'area': 598, 'origin': 'Greek'},
    {'id': 5, 'name': 'Crux', 'hemisphere': 'Southern', 'main_stars': ['Acrux', 'Mimosa', 'Gacrux'], 'area': 68, 'origin': 'Latin'},
    {'id': 6, 'name': 'Lyra', 'hemisphere': 'Northern', 'main_stars': ['Vega', 'Sheliak', 'Sulafat'], 'area': 286, 'origin': 'Greek'},
    {'id': 7, 'name': 'Aquarius', 'hemisphere': 'Southern', 'main_stars': ['Sadalsuud', 'Sadalmelik', 'Sadachbia'], 'area': 980, 'origin': 'Babylonian'},
    {'id': 8, 'name': 'Andromeda', 'hemisphere': 'Northern', 'main_stars': ['Alpheratz', 'Mirach', 'Almach'], 'area': 722, 'origin': 'Greek'},
    {'id': 9, 'name': 'Pegasus', 'hemisphere': 'Northern', 'main_stars': ['Markab', 'Scheat', 'Algenib'], 'area': 1121, 'origin': 'Greek'},
    {'id': 10, 'name': 'Sagittarius', 'hemisphere': 'Southern', 'main_stars': ['Kaus Australis', 'Nunki', 'Ascella'], 'area': 867, 'origin': 'Greek'}
]


# 1. View all constellations
@app.route('/constellations', methods=['GET'])
def get_all_constellations():
    hemisphere = request.args.get('hemisphere')
    if hemisphere:
        filtered = [c for c in constellations if c['hemisphere'].lower() == hemisphere.lower()]
        if not filtered:
            return redirect("https://http.cat/404", code=404)
        return jsonify(filtered), 200
    return jsonify(constellations), 200

# 2. View a specific constellation by name
@app.route('/constellations/<name>', methods=['GET'])
def get_constellation(name):
    constellation = next((c for c in constellations if c['name'].lower() == name.lower()), None)
    if not constellation:
        return redirect("https://http.cat/404", code=404)
    return jsonify(constellation), 200

# 3. Add a new constellation
@app.route('/constellations', methods=['POST'])
def add_constellation():
    data = request.get_json()
    if not data or 'name' not in data or 'hemisphere' not in data or 'main_stars' not in data or 'area' not in data or 'origin' not in data:
        return redirect("https://http.cat/400", code=400)
    new_id = max(c['id'] for c in constellations) + 1
    new_constellation = {
        'id': new_id,
        'name': data['name'],
        'hemisphere': data['hemisphere'],
        'main_stars': data['main_stars'],
        'area': data['area'],
        'origin': data['origin']
    }
    constellations.append(new_constellation)
    return jsonify(new_constellation), 201

# 4. Delete a constellation
@app.route('/constellations/<name>', methods=['DELETE'])
def delete_constellation(name):
    constellation = next((c for c in constellations if c['name'].lower() == name.lower()), None)
    if not constellation:
        return redirect("https://http.cat/404", code=404)
    constellations.remove(constellation)
    return jsonify({"message": "Constellation deleted successfully"}), 200

# 5. Filter constellations by hemisphere and area
@app.route('/constellations/filter', methods=['GET'])
def filter_constellations():
    hemisphere = request.args.get('hemisphere')
    area = request.args.get('area')

    try:
        area = int(area) if area else None
    except ValueError:
        return redirect("https://http.cat/400", code=400)

    filtered = [c for c in constellations if
                (hemisphere is None or c['hemisphere'].lower() == hemisphere.lower()) and
                (area is None or c['area'] <= area)]
    if not filtered:
        return redirect("https://http.cat/404", code=404)
    return jsonify(filtered), 200

# 6. View the main stars of a constellation
@app.route('/constellations/<name>/stars', methods=['GET'])
def get_main_stars(name):
    constellation = next((c for c in constellations if c['name'].lower() == name.lower()), None)
    if not constellation:
        return redirect("https://http.cat/404", code=404)
    return jsonify(constellation['main_stars']), 200

# 7. Partially update a constellation
@app.route('/constellations/<name>', methods=['PATCH'])
def update_constellation(name):
    updates = request.get_json()
    constellation = next((c for c in constellations if c['name'].lower() == name.lower()), None)
    if not constellation:
        return redirect("https://http.cat/404", code=404)
    for key, value in updates.items():
        if key in constellation:
            constellation[key] = value
    return jsonify(constellation), 200

# 9. Add your own custom endpoint
@app.route('/constellations/count', methods=['GET'])
def get_constellation_count():
    return jsonify({'count': len(constellations)})

# 10. Double check that all the endpoints return the appropriate status codes.
# Error handling
@app.errorhandler(404)
def handle_404(e):
    return redirect("https://http.cat/404", code=404)

@app.errorhandler(400)
def handle_400(e):
    return redirect("https://http.cat/400", code=400)

if __name__ == '__main__':
    app.run(debug=True)
