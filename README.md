# Spatial-Temporal Reasoning Analyzer

A comprehensive web-based tool for analyzing, annotating, and repurposing video datasets for spatial-temporal reasoning research. This application provides an intuitive interface for researchers to work with video question-answering (VQA) datasets, perform error analysis, and create new training data.

## Features

### 🎯 Main Interface
- **Dataset Browser**: Browse through available datasets stored in the `data/` folder
- **Sample Navigation**: Navigate through video samples with associated questions, options, and answers
- **Video Preview**: View video content directly in the browser
- **Progress Tracking**: Automatically track viewing progress across datasets

### 🔍 Error Analysis & Annotation
- **Multi-Type Error Classification**: Annotate samples with various error types:
  - **Misalignment**: Content doesn't match the question/answer
  - **Wrong**: Incorrect answers or information
  - **Single Frame Bias**: Analysis based on single frame instead of temporal reasoning
  - **Language Bias**: Bias towards certain language patterns
  - **Poor Video Quality**: Technical issues affecting analysis
  - **Post Edited**: Videos that appear to be edited after recording
  - **Cannot Answer by Vision**: Questions that cannot be answered through visual information alone
  - **Others**: Additional error types not covered above

- **Batch Error Management**: View and manage all samples marked with specific error types
- **Quick Error Lookup**: Check which error types are associated with any sample

### 🔄 Data Repurposing
- **VQA Repurposing**: Create new question-answer pairs for existing videos
  - Add new questions with custom options and answers
  - Edit existing repurposed VQAs
  - Delete unwanted repurposed content
- **Caption Management**: Add, edit, and delete custom captions for video samples
- **Original Data Selection**: Mark original VQA samples for inclusion in new datasets

### 📊 Data Management
- **Progress Tracking**: Keep track of annotation progress across different datasets
- **Abandoned Data Tracking**: Mark samples as abandoned to exclude from final datasets
- **Export Ready**: All annotations and repurposed data are saved in JSON format for easy export

## Getting Started

### Prerequisites
- Python 3.7+
- Flask
- Modern web browser

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. **Prepare your datasets**: Place JSON dataset files in the `data/` folder
2. **Start the application**:
   ```bash
   python app.py
   ```
3. **Access the interface**: Open your browser and navigate to `http://localhost:5000`

### Dataset Format
Your dataset JSON files should contain arrays of objects with the following structure:
```json
{
  "video_url": "path/to/video.mp4",
  "question": "What happens in the video?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "answer": "Option A",
  "caption": "Optional video caption"
}
```

## Interface Guide

### Main Navigation
- **Home** (`/`): Browse and view dataset samples
- **Error Samples** (`/error_samples`): Annotate samples with error types
- **Repurposed Samples** (`/repurposed_samples`): Manage repurposed VQA data

### Workflow Recommendations
1. **Initial Review**: Use the main interface to browse through datasets and get familiar with the content
2. **Error Annotation**: Use the error samples interface to systematically identify and classify problematic samples
3. **Data Repurposing**: Create new VQA pairs from existing video content using the repurposed samples interface
4. **Quality Control**: Review and refine annotations before finalizing your dataset

## Data Storage

The application organizes data in the following structure:
- `data/`: Original dataset files
- `error_annotation/`: Error type annotations (separate JSON file per error type)
- `repurpose_data/`: Repurposed VQA data and caption modifications
- `selected_data/`: Selected samples, progress tracking, and abandoned data

## API Endpoints

The application provides RESTful API endpoints for:
- Sample retrieval and dataset information
- Error annotation management
- VQA repurposing operations
- Progress tracking
- Data selection and abandonment

## Contributing

This tool is designed for research purposes in spatial-temporal reasoning. Feel free to extend the functionality by:
- Adding new error types
- Implementing additional annotation features
- Enhancing the user interface
- Adding export formats

## License

[Add your license information here]

## Citation

If you use this tool in your research, please cite:
[Add citation information here] 