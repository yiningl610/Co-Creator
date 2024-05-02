import asyncio
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

async def generate_content_async(model,prompt,bar):
    
    # 生成内容的请求选项
    request_options = {"timeout": 600}
    
    # 异步生成内容
    async def generate_content():
        for progress in range(101):
            yield progress
            await asyncio.sleep(0.1)  # 模拟生成内容的过程

    async for progress in generate_content():
        # 更新进度条的值
        bar.progress(progress)

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
    #frame_duration = 1 / fps
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

# generates a dictionary to a text file
def generate_text_from_dict(data):
  """Converts a dictionary to a string representation suitable for a text file."""
  text = ""
  for key, value in data.items():
    text += f"#{key}:\n {value}\n"  # Add newline after each key-value pair
  return text
# allows users to choose the download location
# and then downloads the file on button press:
def download_file(file_data, file_name):
  """Downloads the provided data as a file with the given name at the specified path."""
  download_path = get_download_path()
  complete_path = os.path.join(download_path, file_name)
  with open(complete_path, "w") as f:
    f.write(file_data)
  st.success(f"File downloaded to: {complete_path}")

def get_download_path():
  """Prompts the user to select a download location."""
  with st.sidebar.expander("Choose Download Location"):
    download_path = st.text_input("Enter download path (or leave blank for default)", "")
  return download_path if download_path else os.getcwd()

# Download directory for results
# DOWNLOAD_DIR_VIDEO = "cocreater/draft_video_feedback"
# DOWNLOAD_DIR_SCRIPT = "cocreater/video_script_feedback"
# Function to download dictionary results to a json file
# def download_dict(data, filename, download_dir):
#   os.makedirs(download_dir, exist_ok=True)  # Create directory if it doesn't exist
#   filepath = os.path.join(download_dir, f'{filename}_{datetime.now().strftime("%b_%d_%Y")}')
#   with open(filepath, "w") as f:
#     json.dump(data, f, indent=4)
#   st.success(f"Downloaded results to: {filepath}")
# Function to load json files
# def load_feedback_files(download_dir):
#   feedback_files = []
#   if os.path.exists(download_dir):
#     for filename in os.listdir(download_dir):
#       if filename.endswith(".json"):
#         filepath = os.path.join(download_dir, filename)
#         with open(filepath, "r") as f:
#           data = json.load(f)
#         feedback_files.append({"filename": filename, "data": data})
#   return feedback_files

# # Function to show Feedback in streamlit by using tabs
# def show_feedback(data): 
#   """
#   Displays a dictionary in Streamlit tabs.
#   Args:
#       data (dict): The dictionary to display.
#   """
#   videos = []
#   # Loop through each key-value pair in the dictionary
#   for key, value in data.items():
#     # Check existance of Related Video
#     if key.lower()=='relatedvideo':
#       videos = value
#     else:
#       # Create a tab with the key as the title
#       with st.expander(key):
#         # Display the value of the key (can be another dictionary, list, or any data)
#         st.write(value)
#     if videos:
#        st.expander("Related Videos")
#        for video in videos:
#           st.write('Title: ',video['title'])
#           st.write(f"Video URL: https://www.youtube.com/watch?v={video['id']}")
