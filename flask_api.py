
from flask import Flask, request, jsonify
import pandas as pd
import os
from update_dataset_with_images import add_fallback_images_if_needed

app = Flask(__name__)
DATASET_PATH = 'description.csv'
IMAGE_FOLDER = 'images'

def load_dataset():
    df = pd.read_csv(DATASET_PATH)
    df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
    return df

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    df['item_name'] = df['item_name'].astype(str).str.lower()
    item_name = item_name.lower()
    filtered = df[df['item_name'] == item_name]

    color = data.get('color', 'any').strip().lower()

    df = load_dataset()
    filtered = df[df['item_name'].astype(str).str.lower() == item_name]
    if color != 'any':
        filtered = filtered[filtered['color'].str.lower() == color]

    if filtered.empty:
        add_fallback_images_if_needed(item_name, color)
        df = load_dataset()
        filtered = df[df['item_name'].str.lower() == item_name]
        if color != 'any':
            filtered = filtered[filtered['color'].str.lower() == color]

    if filtered.empty:
        return jsonify({'recommendations': [], 'message': 'No outfits found.'})

    results = filtered.sample(min(5, len(filtered))).to_dict(orient='records')
    return jsonify({'recommendations': results})

if __name__ == '__main__':
    app.run(debug=True)
