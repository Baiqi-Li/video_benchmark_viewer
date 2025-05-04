from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# 模拟数据集
DATASETS = {
    'dataset1': 'data/dataset1.json',
    'dataset2': 'data/dataset2.json'
}

def load_dataset(dataset_name):
    """加载指定数据集"""
    if dataset_name not in DATASETS:
        return None
    
    file_path = DATASETS[dataset_name]
    if not os.path.exists(file_path):
        return None
        
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html', datasets=list(DATASETS.keys()))

@app.route('/get_sample/<dataset_name>/<int:sample_index>')
def get_sample(dataset_name, sample_index):
    dataset = load_dataset(dataset_name)
    if not dataset:
        return jsonify({'error': 'Dataset not found'}), 404
    
    if sample_index < 0 or sample_index >= len(dataset):
        return jsonify({'error': 'Sample index out of range'}), 400
    
    return jsonify(dataset[sample_index])

@app.route('/get_dataset_info/<dataset_name>')
def get_dataset_info(dataset_name):
    dataset = load_dataset(dataset_name)
    if not dataset:
        return jsonify({'error': 'Dataset not found'}), 404
    
    return jsonify({
        'total_samples': len(dataset),
        'samples': dataset
    })

if __name__ == '__main__':
    app.run(debug=True) 