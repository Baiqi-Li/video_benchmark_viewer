# Spatial Temporal Reasoning Analyzer

A web-based tool for analyzing and annotating video datasets, specifically designed for spatial-temporal reasoning research. This application provides a comprehensive interface for video sample review, error annotation, and data curation.

## Features

### 🎥 Video Sample Viewer
- **Multi-format Support**: Supports both regular video files and YouTube videos
- **Precise Navigation**: Browse through dataset samples with frame-level and time-based controls
- **Progress Tracking**: Automatically saves your progress across sessions
- **Multiple Dataset Support**: Switch between different datasets seamlessly

### 🏷️ Error Annotation System
- **8 Error Categories**: Comprehensive error classification system
  - **Ambiguous**: Questions or answers that are unclear or ambiguous
  - **Wrong**: Incorrect answers or flawed questions
  - **Single Frame Bias**: Problems that can be solved with just one frame
  - **Language Bias**: Issues related to language understanding rather than visual reasoning
  - **Poor Video Quality**: Technical issues affecting video clarity
  - **Post Edited**: Videos that have been artificially modified
  - **Cannot Answer by Vision**: Questions that cannot be answered through visual information alone
  - **Others**: Any other types of errors not covered above

### 📝 Content Management
- **Caption Management**: Add, edit, and delete video captions
- **VQA (Visual Question Answering) Management**: Create and manage repurposed questions and answers
- **Data Selection**: Mark samples for inclusion in curated datasets
- **Abandonment Tracking**: Flag samples that should be excluded

### 📊 Data Organization
- **Selected Data**: Curated collection of high-quality samples
- **Error Samples**: Organized by error type for quality control
- **Repurposed Content**: Modified questions, answers, and captions
- **Progress Tracking**: Resume work from where you left off

## Installation

### Prerequisites
- Python 3.7+
- Web browser with JavaScript support

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd spatial_temporal_reasoning_analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your datasets**
   - Place your dataset JSON files in the `data/` directory
   - Ensure each dataset follows the expected JSON structure (see Data Format section)

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## Data Format

### Expected JSON Structure
Each dataset should be a JSON array with objects containing:

```json
{
  "id": "unique_identifier",
  "video_url": "path/to/video/or/youtube/url",
  "question": "What is happening in the video?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "answer": "Option A",
  "caption": "Video description",
  "start_time": 0.0,
  "end_time": 10.0,
  "start_frame": 0,
  "end_frame": 300,
  "total_frames": 300,
  "type": "temporal_reasoning",
  "reasoning": "Explanation of the answer"
}
```

### Required Fields
- `video_url`: Path to video file or YouTube URL
- `question`: The question to be answered
- `options`: Array of possible answers
- `answer`: The correct answer

### Optional Fields
- `caption`: Video description
- `start_time`/`end_time`: Time segment in seconds
- `start_frame`/`end_frame`: Frame segment
- `total_frames`: Total number of frames
- `type`: Category of the question
- `reasoning`: Explanation for the answer

## User Guide

### 1. Main Interface (Video Sample Viewer)

#### Getting Started
1. **Select Dataset**: Choose from available datasets in the dropdown
2. **Navigate Samples**: Use Previous/Next buttons or enter specific sample index
3. **View Progress**: Track your current position and total samples

#### Video Controls
- **Time-based Playback**: Enter start and end times to play specific segments
- **Frame-based Playback**: Use frame numbers for precise control
- **YouTube Support**: Seamlessly handle YouTube video URLs

#### Error Annotation
1. **Review Content**: Watch video and read question/answer
2. **Select Error Types**: Check applicable error categories
3. **Automatic Saving**: Annotations are saved immediately

#### Content Management
1. **Add Captions**: Create new video descriptions
2. **Create VQAs**: Add new question-answer pairs
3. **Select Data**: Mark samples for inclusion in final dataset
4. **Abandon Samples**: Flag problematic samples for exclusion

### 2. Error Samples Interface

#### Viewing Error Samples
1. **Select Dataset**: Choose the dataset to review
2. **Filter by Error Type**: Select specific error category
3. **Review Samples**: Click on samples to view details
4. **Manage Annotations**: Remove error annotations as needed

#### Bulk Operations
- **Delete Annotations**: Remove error labels from samples
- **Review Repurposed Content**: See related repurposed VQAs

### 3. Repurposed Samples Interface

#### Managing Repurposed Content
1. **Browse Samples**: View all samples with repurposed content
2. **Edit VQAs**: Modify repurposed questions and answers
3. **Manage Captions**: Edit or delete repurposed captions
4. **Quality Control**: Review and refine repurposed content

## File Structure

```
spatial_temporal_reasoning_analyzer/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── data/                 # Dataset JSON files
├── error_annotation/     # Error type annotations
├── repurpose_data/       # Repurposed VQAs and captions
├── selected_data/        # Curated dataset and progress
└── templates/            # HTML templates
    ├── index.html           # Main interface
    ├── error_samples.html   # Error samples viewer
    └── repurposed_samples.html  # Repurposed content viewer
```

## Data Output

The application generates several types of output files:

### Error Annotations (`error_annotation/`)
- `{ErrorType}.json`: Lists of samples annotated with each error type
- Organized by dataset and sample index

### Repurposed Data (`repurpose_data/`)
- `repurposed_vqa.json`: New questions and answers created from original samples
- `repurposed_caption.json`: New captions for videos
- `repurposed_indices.json`: Index mapping for repurposed content

### Selected Data (`selected_data/`)
- `selected_data.json`: Curated list of high-quality samples
- `selected_captions.json`: Selected captions
- `abandoned_data.json`: Samples marked for exclusion
- `progress.json`: Session progress tracking

## Best Practices

### Data Quality Control
1. **Systematic Review**: Go through samples sequentially
2. **Multi-pass Annotation**: Review error types in separate passes
3. **Consistency Checks**: Regularly review error annotations
4. **Progress Saving**: Let the system track your progress automatically

### Content Creation
1. **Clear Captions**: Write descriptive, accurate captions
2. **Balanced VQAs**: Create diverse question types
3. **Quality over Quantity**: Focus on high-quality repurposed content
4. **Regular Backups**: Export your work regularly

### Navigation Tips
1. **Use Keyboard Shortcuts**: Arrow keys for sample navigation
2. **Bookmark Progress**: Note your current position for reference
3. **Filter Views**: Use error type filters for focused review
4. **Time Management**: Use progress tracking to plan work sessions

## Technical Notes

### Video Support
- **Local Files**: Supports common video formats (MP4, AVI, MOV, etc.)
- **YouTube Integration**: Direct YouTube URL support with API integration
- **Frame-level Control**: Precise navigation for detailed analysis

### Data Persistence
- **Automatic Saving**: All annotations and selections are saved immediately
- **Session Recovery**: Resume work from previous sessions
- **Data Integrity**: Robust error handling and data validation

### Performance Considerations
- **Lazy Loading**: Samples loaded on demand
- **Client-side Caching**: Efficient data handling
- **Progress Optimization**: Minimal server requests for smooth operation

## Troubleshooting

### Common Issues

1. **Video Not Loading**
   - Check video URL format
   - Verify file permissions for local videos
   - Ensure YouTube API is properly loaded

2. **Annotations Not Saving**
   - Check write permissions for annotation directories
   - Verify JSON file format integrity
   - Restart application if persistent issues

3. **Performance Issues**
   - Close unused browser tabs
   - Clear browser cache
   - Restart application for memory cleanup

### Support
For technical support or feature requests, please create an issue in the project repository.

## License

This project is licensed under the MIT License. See the LICENSE file for details. 