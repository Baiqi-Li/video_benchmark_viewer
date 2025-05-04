from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

def get_available_datasets():
    """获取data文件夹中所有可用的数据集"""
    datasets = {}
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    for file in os.listdir(data_dir):
        if file.endswith('.json'):
            dataset_name = os.path.splitext(file)[0]
            datasets[dataset_name] = os.path.join(data_dir, file)
    
    return datasets

def load_dataset(dataset_name):
    """加载指定数据集"""
    datasets = get_available_datasets()
    if dataset_name not in datasets:
        return None
    
    file_path = datasets[dataset_name]
    if not os.path.exists(file_path):
        return None
        
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_options(options_str):
    """格式化选项字符串为列表"""
    if not options_str:
        return []
    # 如果选项是字符串，尝试按换行符分割
    if isinstance(options_str, str):
        return [opt.strip() for opt in options_str.split('\n') if opt.strip()]
    # 如果已经是列表，直接返回
    return options_str

@app.route('/')
def index():
    datasets = get_available_datasets()
    return render_template('index.html', datasets=list(datasets.keys()))

@app.route('/get_sample/<dataset_name>/<int:sample_index>')
def get_sample(dataset_name, sample_index):
    dataset = load_dataset(dataset_name)
    if not dataset:
        return jsonify({'error': 'Dataset not found'}), 404
    
    if sample_index < 0 or sample_index >= len(dataset):
        return jsonify({'error': 'Sample index out of range'}), 400
    
    sample = dataset[sample_index]
    # 格式化选项
    sample['options'] = format_options(sample.get('options', ''))
    return jsonify(sample)

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