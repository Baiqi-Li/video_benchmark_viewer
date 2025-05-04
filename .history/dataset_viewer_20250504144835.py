import json
import tkinter as tk
from tkinter import ttk
import webbrowser

class DatasetViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Dataset Viewer")
        
        # Load dataset
        with open('data/random_200_tempcompass_qa_json.json', 'r', encoding='utf-8') as f:
            self.dataset = json.load(f)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create sample selector
        ttk.Label(main_frame, text="Select Sample:").grid(row=0, column=0, sticky=tk.W)
        self.sample_var = tk.StringVar()
        self.sample_selector = ttk.Combobox(main_frame, textvariable=self.sample_var, state="readonly")
        self.sample_selector['values'] = [f"Sample {i+1}" for i in range(len(self.dataset))]
        self.sample_selector.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.sample_selector.bind('<<ComboboxSelected>>', self.on_sample_selected)
        
        # Create info display
        self.info_text = tk.Text(main_frame, height=15, width=80, wrap=tk.WORD)
        self.info_text.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Create video button
        self.video_button = ttk.Button(main_frame, text="Open Video", command=self.open_video)
        self.video_button.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Create dimension filter
        ttk.Label(main_frame, text="Filter by Dimension:").grid(row=3, column=0, sticky=tk.W)
        self.dim_var = tk.StringVar()
        self.dim_selector = ttk.Combobox(main_frame, textvariable=self.dim_var, state="readonly")
        dimensions = sorted(set(item['meta_data']['dim'] for item in self.dataset))
        self.dim_selector['values'] = ['All'] + dimensions
        self.dim_selector.set('All')
        self.dim_selector.grid(row=3, column=1, sticky=(tk.W, tk.E))
        self.dim_selector.bind('<<ComboboxSelected>>', self.on_dimension_selected)
        
        # Display total count
        total_count = len(self.dataset)
        ttk.Label(main_frame, text=f"Total Samples: {total_count}").grid(row=4, column=0, columnspan=2, pady=5)
        
        # Initialize with first sample
        self.current_sample = 0
        self.update_display()
    
    def on_sample_selected(self, event):
        self.current_sample = self.sample_selector.current()
        self.update_display()
    
    def on_dimension_selected(self, event):
        selected_dim = self.dim_selector.get()
        if selected_dim == 'All':
            self.sample_selector['values'] = [f"Sample {i+1}" for i in range(len(self.dataset))]
        else:
            filtered_indices = [i for i, item in enumerate(self.dataset) 
                              if item['meta_data']['dim'] == selected_dim]
            self.sample_selector['values'] = [f"Sample {i+1}" for i in filtered_indices]
        self.sample_selector.set(self.sample_selector['values'][0])
        self.current_sample = 0
        self.update_display()
    
    def update_display(self):
        sample = self.dataset[self.current_sample]
        info = f"Video ID: {sample['meta_data']['video_id']}\n"
        info += f"Dimension: {sample['meta_data']['dim']}\n\n"
        info += f"Question:\n{sample['question']}\n\n"
        info += f"Answer:\n{sample['answer']}\n"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)
    
    def open_video(self):
        sample = self.dataset[self.current_sample]
        webbrowser.open(sample['video_url'])

if __name__ == "__main__":
    root = tk.Tk()
    app = DatasetViewer(root)
    root.mainloop() 