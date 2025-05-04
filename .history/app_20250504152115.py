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

def get_error_annotation_file(error_type):
    """获取错误类型标注文件的路径"""
    error_dir = 'error_annotation'
    if not os.path.exists(error_dir):
        os.makedirs(error_dir)
    return os.path.join(error_dir, f'{error_type}.json')

def load_error_annotations(error_type):
    """加载指定错误类型的标注"""
    file_path = get_error_annotation_file(error_type)
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_error_annotations(error_type, annotations):
    """保存指定错误类型的标注"""
    file_path = get_error_annotation_file(error_type)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(annotations, f, indent=2)

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
    # Ensure video_url is properly formatted
    if 'video_url' in sample:
        sample['video_url'] = sample['video_url'].strip()
    
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

@app.route('/update_error_annotation', methods=['POST'])
def update_error_annotation():
    data = request.json
    dataset = data.get('dataset')
    sample_id = data.get('sample_id')
    error_type = data.get('error_type')
    is_checked = data.get('is_checked')

    if not all([dataset, sample_id, error_type, is_checked is not None]):
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400

    # 加载数据集以获取完整样本数据
    dataset_data = load_dataset(dataset)
    if not dataset_data:
        return jsonify({'success': False, 'error': 'Dataset not found'}), 404

    # 找到对应的样本数据
    sample_data = None
    for sample in dataset_data:
        if str(sample.get('id', '')) == str(sample_id) or f"{dataset}_{dataset_data.index(sample)}" == sample_id:
            sample_data = sample
            break

    if not sample_data:
        return jsonify({'success': False, 'error': 'Sample not found'}), 404

    # 加载现有的标注
    annotations = load_error_annotations(error_type)
    
    # 更新标注
    if is_checked:
        if dataset not in annotations:
            annotations[dataset] = []
        # 检查是否已存在相同的样本数据
        sample_exists = False
        for existing_sample in annotations[dataset]:
            if (existing_sample.get('id') == sample_data.get('id') and 
                existing_sample.get('video_url') == sample_data.get('video_url')):
                sample_exists = True
                break
        if not sample_exists:
            annotations[dataset].append(sample_data)
    else:
        if dataset in annotations:
            # 移除匹配的样本数据
            annotations[dataset] = [s for s in annotations[dataset] 
                                  if not (s.get('id') == sample_data.get('id') and 
                                        s.get('video_url') == sample_data.get('video_url'))]
            if not annotations[dataset]:  # 如果数据集为空，删除数据集键
                del annotations[dataset]

    # 保存更新后的标注
    save_error_annotations(error_type, annotations)
    
    return jsonify({'success': True})

@app.route('/get_error_annotations', methods=['POST'])
def get_error_annotations():
    data = request.json
    dataset = data.get('dataset')
    sample_id = data.get('sample_id')

    if not all([dataset, sample_id]):
        return jsonify({'error': 'Missing required parameters'}), 400

    # 加载数据集以获取完整样本数据
    dataset_data = load_dataset(dataset)
    if not dataset_data:
        return jsonify({'error': 'Dataset not found'}), 404

    # 找到对应的样本数据
    sample_data = None
    for sample in dataset_data:
        if str(sample.get('id', '')) == str(sample_id) or f"{dataset}_{dataset_data.index(sample)}" == sample_id:
            sample_data = sample
            break

    if not sample_data:
        return jsonify({'error': 'Sample not found'}), 404

    error_types = []
    for error_type in ['Misalignment', 'Wrong', 'Single Frame Bias']:
        annotations = load_error_annotations(error_type)
        if dataset in annotations:
            # 检查样本是否在标注中
            for annotated_sample in annotations[dataset]:
                if (annotated_sample.get('id') == sample_data.get('id') and 
                    annotated_sample.get('video_url') == sample_data.get('video_url')):
                    error_types.append(error_type)
                    break

    return jsonify({'error_types': error_types})

if __name__ == '__main__':
    app.run(debug=True) 