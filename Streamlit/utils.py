import streamlit as st
# from PIL import Image

from streamlit_extras.app_logo import add_logo

# im = Image.open("logo.png")
# im1 = im.resize(([100,100]))

def logo():
    add_logo("Streamlit/logo120.png",height=80)
    
def Title():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "Co-Creator";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

import os
import shutil
import tempfile
import cv2
import json
from datetime import datetime
# Constants
FRAME_EXTRACTION_DIRECTORY = "./pages/content/frames"
FRAME_PREFIX = "_frame"

# Function to create or cleanup the frame extraction directory
def create_frame_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        
# Function to extract frames from video (1 frame/second for demonstration)
def extract_frame_from_video(upload_file):
    create_frame_output_dir(FRAME_EXTRACTION_DIRECTORY)
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
      temp_file.write(upload_file.read())
      file_path = temp_file.name
    #bytes_data = upload_file.read()
    vidcap = cv2.VideoCapture(file_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_duration = 1 / fps
    output_file_prefix = os.path.basename(upload_file.name).replace('.', '_')
    frame_count = 0
    count = 0
    while vidcap.isOpened():
      success, frame = vidcap.read()
      if not success:
        break
      if int(count / fps) == frame_count:
        min = frame_count // 60
        sec = frame_count % 60
        time_string = f"{min:02d}:{sec:02d}"
        image_name = f"{output_file_prefix}{FRAME_PREFIX}{time_string}.jpg"
        output_filename = os.path.join(FRAME_EXTRACTION_DIRECTORY, image_name)
        cv2.imwrite(output_filename, frame)
        frame_count += 1
      count += 1
    vidcap.release()
    print(f"Completed video frame extraction!\n\nExtracted: {frame_count} frames")
    
class File:
      def __init__(self, file_path: str, display_name: str = None):
        self.file_path = file_path
        if display_name:
          self.display_name = display_name
        self.timestamp = get_timestamp(file_path)
    
      def set_file_response(self, response):
        self.response = response

def get_timestamp(filename):
    parts = filename.split(FRAME_PREFIX)
    if len(parts) != 2:
        return None  # Indicates the filename might be incorrectly formatted
    return parts[1].split('.')[0]

# Make GenerateContent request with the structure described above.
def make_request(prompt, files):
    request = [prompt]
    for file in files:
        request.append(file.timestamp)
        request.append(file.response)
    return request

# Download directory for results
DOWNLOAD_DIR_VIDEO = "cocreater/draft_video_feedback"
DOWNLOAD_DIR_SCRIPT = "cocreater/video_script_feedback"
# Function to download dictionary results to a json file
def download_dict(data, filename, download_dir):
  os.makedirs(download_dir, exist_ok=True)  # Create directory if it doesn't exist
  filepath = os.path.join(download_dir, f'{filename}_{datetime.now().strftime("%b_%d_%Y")}')
  with open(filepath, "w") as f:
    json.dump(data, f, indent=4)
  st.success(f"Downloaded results to: {filepath}")
# Function to load json files
def load_feedback_files(download_dir):
  feedback_files = []
  for filename in os.listdir(download_dir):
    if filename.endswith(".json"):
      filepath = os.path.join(download_dir, filename)
      with open(filepath, "r") as f:
        data = json.load(f)
      feedback_files.append(data)
  return feedback_files
