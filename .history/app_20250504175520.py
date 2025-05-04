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

def get_repurpose_data_file():
    """获取repurpose_data文件夹的路径"""
    repurpose_dir = 'repurpose_data'
    if not os.path.exists(repurpose_dir):
        os.makedirs(repurpose_dir)
    return os.path.join(repurpose_dir, 'repurposed_vqa.json')

def get_repurposed_indices_file():
    """获取repurposed indices文件的路径"""
    repurpose_dir = 'repurpose_data'
    if not os.path.exists(repurpose_dir):
        os.makedirs(repurpose_dir)
    return os.path.join(repurpose_dir, 'repurposed_indices.json')

def load_repurposed_data():
    """加载repurposed数据"""
    file_path = get_repurpose_data_file()
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_repurposed_indices():
    """加载repurposed indices数据"""
    file_path = get_repurposed_indices_file()
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_repurposed_data(data):
    """保存repurposed数据"""
    file_path = get_repurpose_data_file()
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def save_repurposed_indices(data):
    """保存repurposed indices数据"""
    file_path = get_repurposed_indices_file()
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_selected_data_file():
    """获取selected_data文件夹的路径"""
    selected_dir = 'selected_data'
    if not os.path.exists(selected_dir):
        os.makedirs(selected_dir)
    return os.path.join(selected_dir, 'selected_vqa.json')

def load_selected_data():
    """加载selected数据"""
    file_path = get_selected_data_file()
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_selected_data(data):
    """保存selected数据"""
    file_path = get_selected_data_file()
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    datasets = get_available_datasets()
    return render_template('index.html', datasets=list(datasets.keys()))

@app.route('/error_samples')
def error_samples():
    datasets = get_available_datasets()
    return render_template('error_samples.html', datasets=list(datasets.keys()))

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

    # 加载现有的标注
    annotations = load_error_annotations(error_type)
    
    # 更新标注
    if is_checked:
        if dataset not in annotations:
            annotations[dataset] = []
        # 将sample_id转换为整数索引
        try:
            index = int(sample_id.split('_')[-1]) if isinstance(sample_id, str) else sample_id
            if index not in annotations[dataset]:
                annotations[dataset].append(index)
                annotations[dataset].sort()  # 保持索引有序
        except (ValueError, IndexError):
            return jsonify({'success': False, 'error': 'Invalid sample index'}), 400
    else:
        if dataset in annotations:
            try:
                index = int(sample_id.split('_')[-1]) if isinstance(sample_id, str) else sample_id
                if index in annotations[dataset]:
                    annotations[dataset].remove(index)
                    if not annotations[dataset]:  # 如果数据集为空，删除数据集键
                        del annotations[dataset]
            except (ValueError, IndexError):
                return jsonify({'success': False, 'error': 'Invalid sample index'}), 400

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

    error_types = []
    for error_type in ['Misalignment', 'Wrong', 'Single Frame Bias', 'Others']:
        annotations = load_error_annotations(error_type)
        if dataset in annotations:
            try:
                index = int(sample_id.split('_')[-1]) if isinstance(sample_id, str) else sample_id
                if index in annotations[dataset]:
                    error_types.append(error_type)
            except (ValueError, IndexError):
                continue

    return jsonify({'error_types': error_types})

@app.route('/get_error_samples', methods=['POST'])
def get_error_samples():
    data = request.json
    dataset = data.get('dataset')
    error_type = data.get('error_type')

    if not all([dataset, error_type]):
        return jsonify({'error': 'Missing required parameters'}), 400

    # 加载错误类型标注
    annotations = load_error_annotations(error_type)
    if dataset not in annotations:
        return jsonify({'samples': []})

    # 加载数据集
    dataset_data = load_dataset(dataset)
    if not dataset_data:
        return jsonify({'error': 'Dataset not found'}), 404

    # 获取标注的样本
    error_samples = []
    for index in annotations[dataset]:
        if index < len(dataset_data):
            error_samples.append(dataset_data[index])

    return jsonify({'samples': error_samples})

@app.route('/add_new_vqa', methods=['POST'])
def add_new_vqa():
    data = request.json
    dataset = data.get('dataset')
    sample_index = data.get('sample_index')
    new_question = data.get('new_question')
    new_options = data.get('new_options')
    new_answer = data.get('new_answer')

    if not all([dataset, sample_index is not None, new_question, new_options, new_answer]):
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400

    # 加载原始数据集
    dataset_data = load_dataset(dataset)
    if not dataset_data:
        return jsonify({'success': False, 'error': 'Dataset not found'}), 404

    if sample_index < 0 or sample_index >= len(dataset_data):
        return jsonify({'success': False, 'error': 'Sample index out of range'}), 400

    # 获取原始样本
    original_sample = dataset_data[sample_index]

    # 创建新的repurposed数据项
    repurposed_item = {
        'original_dataset': dataset,
        'original_index': sample_index,
        'video_url': original_sample.get('video_url', ''),
        'new_question': new_question,
        'new_options': new_options,
        'new_answer': new_answer
    }

    # 加载现有的repurposed数据
    repurposed_data = load_repurposed_data()

    # 检查是否已存在相同的repurposed数据
    for item in repurposed_data:
        if (item['original_dataset'] == dataset and 
            item['original_index'] == sample_index and 
            item['new_question'] == new_question and 
            item['new_options'] == new_options and 
            item['new_answer'] == new_answer):
            return jsonify({'success': False, 'error': 'This repurposed VQA already exists'}), 400

    # 添加新的repurposed数据
    repurposed_data.append(repurposed_item)

    # 保存更新后的repurposed数据
    save_repurposed_data(repurposed_data)

    # 更新repurposed indices
    repurposed_indices = load_repurposed_indices()
    if dataset not in repurposed_indices:
        repurposed_indices[dataset] = []
    if sample_index not in repurposed_indices[dataset]:
        repurposed_indices[dataset].append(sample_index)
        repurposed_indices[dataset].sort()  # 保持索引有序
        save_repurposed_indices(repurposed_indices)

    return jsonify({'success': True})

@app.route('/get_repurposed_vqas', methods=['POST'])
def get_repurposed_vqas():
    data = request.json
    dataset = data.get('dataset')
    sample_index = data.get('sample_index')

    if not all([dataset, sample_index is not None]):
        return jsonify({'error': 'Missing required parameters'}), 400

    # 加载repurposed数据
    repurposed_data = load_repurposed_data()

    # 筛选出当前数据集和样本索引的repurposed数据
    filtered_vqas = [
        vqa for vqa in repurposed_data
        if vqa['original_dataset'] == dataset and vqa['original_index'] == sample_index
    ]

    return jsonify({'repurposed_vqas': filtered_vqas})

@app.route('/delete_repurposed_vqa', methods=['POST'])
def delete_repurposed_vqa():
    data = request.json
    dataset = data.get('dataset')
    sample_index = data.get('sample_index')
    vqa_index = data.get('vqa_index')

    if not all([dataset, sample_index is not None, vqa_index is not None]):
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400

    # 加载repurposed数据
    repurposed_data = load_repurposed_data()

    # 筛选出当前数据集和样本索引的repurposed数据
    filtered_vqas = [
        (i, vqa) for i, vqa in enumerate(repurposed_data)
        if vqa['original_dataset'] == dataset and vqa['original_index'] == sample_index
    ]

    if vqa_index >= len(filtered_vqas):
        return jsonify({'success': False, 'error': 'Invalid VQA index'}), 400

    # 获取要删除的VQA的原始索引
    original_index = filtered_vqas[vqa_index][0]

    # 删除VQA
    del repurposed_data[original_index]

    # 保存更新后的repurposed数据
    save_repurposed_data(repurposed_data)

    # 更新repurposed indices
    repurposed_indices = load_repurposed_indices()
    if dataset in repurposed_indices:
        # 检查是否还有其他repurposed数据
        remaining_vqas = [
            vqa for vqa in repurposed_data
            if vqa['original_dataset'] == dataset and vqa['original_index'] == sample_index
        ]
        if not remaining_vqas:
            # 如果没有其他repurposed数据，从indices中移除
            repurposed_indices[dataset].remove(sample_index)
            if not repurposed_indices[dataset]:  # 如果数据集为空，删除数据集键
                del repurposed_indices[dataset]
            save_repurposed_indices(repurposed_indices)

    return jsonify({'success': True})

@app.route('/repurposed_samples')
def repurposed_samples():
    datasets = get_available_datasets()
    return render_template('repurposed_samples.html', datasets=list(datasets.keys()))

@app.route('/get_repurposed_samples', methods=['POST'])
def get_repurposed_samples():
    data = request.json
    dataset = data.get('dataset')

    if not dataset:
        return jsonify({'error': 'Missing required parameters'}), 400

    # 加载repurposed indices
    repurposed_indices = load_repurposed_indices()
    if dataset not in repurposed_indices:
        return jsonify({'samples': []})

    # 加载原始数据集
    dataset_data = load_dataset(dataset)
    if not dataset_data:
        return jsonify({'error': 'Dataset not found'}), 404

    # 加载repurposed数据
    repurposed_data = load_repurposed_data()

    # 获取有repurposed数据的样本
    samples = []
    for index in repurposed_indices[dataset]:
        if index < len(dataset_data):
            sample = dataset_data[index].copy()
            # 添加原始索引
            sample['original_index'] = index
            # 添加repurposed VQAs
            sample['repurposed_vqas'] = [
                vqa for vqa in repurposed_data
                if vqa['original_dataset'] == dataset and vqa['original_index'] == index
            ]
            samples.append(sample)

    return jsonify({'samples': samples})

@app.route('/update_repurposed_vqa', methods=['POST'])
def update_repurposed_vqa():
    data = request.json
    dataset = data.get('dataset')
    sample_index = data.get('sample_index')
    vqa_index = data.get('vqa_index')
    new_question = data.get('new_question')
    new_options = data.get('new_options')
    new_answer = data.get('new_answer')

    if not all([dataset, sample_index is not None, vqa_index is not None]):
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400

    # 加载repurposed数据
    repurposed_data = load_repurposed_data()

    # 筛选出当前数据集和样本索引的repurposed数据
    filtered_vqas = [
        (i, vqa) for i, vqa in enumerate(repurposed_data)
        if vqa['original_dataset'] == dataset and vqa['original_index'] == sample_index
    ]

    if vqa_index >= len(filtered_vqas):
        return jsonify({'success': False, 'error': 'Invalid VQA index'}), 400

    # 获取要更新的VQA的原始索引
    original_index = filtered_vqas[vqa_index][0]

    # 更新VQA
    repurposed_data[original_index].update({
        'new_question': new_question,
        'new_options': new_options,
        'new_answer': new_answer
    })

    # 保存更新后的repurposed数据
    save_repurposed_data(repurposed_data)

    return jsonify({'success': True})

@app.route('/update_original_vqa_selection', methods=['POST'])
def update_original_vqa_selection():
    data = request.json
    dataset = data.get('dataset')
    sample_index = data.get('sample_index')
    is_selected = data.get('is_selected')

    if not all([dataset, sample_index is not None, is_selected is not None]):
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400

    # 加载原始数据集
    dataset_data = load_dataset(dataset)
    if not dataset_data:
        return jsonify({'success': False, 'error': 'Dataset not found'}), 404

    if sample_index < 0 or sample_index >= len(dataset_data):
        return jsonify({'success': False, 'error': 'Sample index out of range'}), 400

    # 获取原始样本
    original_sample = dataset_data[sample_index]

    # 加载现有的selected数据
    selected_data = load_selected_data()

    if is_selected:
        # 检查是否已存在相同的selected数据
        for item in selected_data:
            if (item['dataset'] == dataset and 
                item['sample_index'] == sample_index):
                return jsonify({'success': True})

        # 创建新的selected数据项
        selected_item = {
            'dataset': dataset,
            'sample_index': sample_index,
            'video_url': original_sample.get('video_url', ''),
            'question': original_sample.get('question', ''),
            'options': original_sample.get('options', ''),
            'answer': original_sample.get('answer', '')
        }

        # 添加新的selected数据
        selected_data.append(selected_item)
    else:
        # 移除selected数据
        selected_data = [
            item for item in selected_data
            if not (item['dataset'] == dataset and item['sample_index'] == sample_index)
        ]

    # 保存更新后的selected数据
    save_selected_data(selected_data)

    return jsonify({'success': True})

@app.route('/get_original_vqa_selection', methods=['POST'])
def get_original_vqa_selection():
    data = request.json
    dataset = data.get('dataset')
    sample_index = data.get('sample_index')

    if not all([dataset, sample_index is not None]):
        return jsonify({'error': 'Missing required parameters'}), 400

    # 加载selected数据
    selected_data = load_selected_data()

    # 检查当前样本是否在selected数据中
    is_selected = any(
        item['dataset'] == dataset and item['sample_index'] == sample_index
        for item in selected_data
    )

    return jsonify({'is_selected': is_selected})

if __name__ == '__main__':
    app.run(debug=True) 