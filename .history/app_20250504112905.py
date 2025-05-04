from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# 基础视频URL
BASE_VIDEO_URL = "https://huggingface.co/datasets/BaiqiL/public_videos/resolve/main/tempcompass/videos/"

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

def process_video_url(video_url):
    """处理视频URL，确保返回完整的Hugging Face视频URL"""
    if video_url.startswith('http'):
        return video_url
    else:
        # 确保视频ID正确拼接
        video_id = video_url.strip()
        if not video_id.endswith('.mp4'):
            video_id += '.mp4'
        return BASE_VIDEO_URL + video_id

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
    # 处理视频URL
    sample['video_url'] = process_video_url(sample['video_url'])
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