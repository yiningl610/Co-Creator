import streamlit as st
import os
import google.generativeai as genai
from youtube_search import YoutubeSearch
from utils import *

st.set_page_config(page_title="Video",
                   layout="wide",
                   page_icon="🎞️")

logo()
#Title()

genai.configure(api_key=st.secrets['videoAPI'])

st.markdown("### This page will help you analyze your draft video")
st.write(
    """Give you some suggestions on video title, description, thumbnail, tags.  
       Tell you whether the video content is relevant to your topic, target audience, and tone.  
       To make your video more attractive.  
    """
)

topic = None
target = None
tone = None
aim = None
output = {"Title": None,"Description": None,"Thumbnail": None,"Tag": None,"Relevance": None,"RelatedVideo": []}
topic = st.text_input("Enter your topic here:")
target = st.text_input("Enter your target audience here:")
tone = st.text_input("Enter your desired tone here:")
uploaded_file = st.file_uploader("Upload your video", type=['mp4'])
AnalyzeButton = st.button('Analyze')

aim = "".join(['topic:',topic, 'target audience:', target, 'video tone:', tone])
if AnalyzeButton:
  if topic and target and tone and uploaded_file:
    # Extract frames from uploaded video
    extract_frame_from_video(uploaded_file)
    # Process each frame in the output directory
    files = os.listdir(FRAME_EXTRACTION_DIRECTORY)
    files = sorted(files)
    files_to_upload = []
    for file in files:
      files_to_upload.append(
          File(file_path=os.path.join(FRAME_EXTRACTION_DIRECTORY, file)))
    
    # Upload the files to the API
    # Only upload a 10 second slice of files to reduce upload time.
    # Change full_video to True to upload the whole video.
    full_video = True
    uploaded_files = []
    st.info(f'Uploading {len(files_to_upload) if full_video else 10} files. This might take a bit...')
    
    for file in files_to_upload if full_video else files_to_upload[:10]:
        print(f'Uploading: {file.file_path}...')
        response = genai.upload_file(path=file.file_path)
        file.set_file_response(response)
        uploaded_files.append(file)
    
    st.info(f"Completed file uploads!\n\nUploaded: {len(uploaded_files)} files")
  # Description generation (placeholder using user input)
    # Create the prompt.
    promptTitle = f"Brainstorm some click-worthy titles for this YouTube video! Based on the video topic {topic}, and the target audience {target}, and the feeling it evokes. Focus on the benefits viewers will get."
    #promptTitleTag = f"Brainstorm some click-worthy titles for this YouTube video! Based on the video topic {topic}, and the target audience {target}, and the feeling it evokes. Focus on the benefits viewers will get. And create a list of 5 relevant hashtags for this YouTube video. Include a mix of high-volume and low-volume hashtags, targeting the specific features {aim} and niche of the video."
    promptDescription = "Craft a captivating description under 150 words, weaving vivid language, intriguing questions, and a clear call to action for the YouTube video mentioned above. Think about the video's core theme, target audience, and desired emotional response (curiosity, excitement, etc.). Include specific keywords if relevant. Remember, the key is to make the video stand out as a hidden gem, enticing viewers to click play and delve deeper! Give me just 3 descriptions with no sub-categories or tips."
    promptThumbnail = "Give me suggestions on how to make the thumbnail for this video idea attractive."
    promptTags = f"Create a list of 5 relevant hashtags for this YouTube video. Include a mix of high-volume and low-volume hashtags, targeting the specific features {aim} and niche of the video."
    promptKeywords = "Give me 5 keywords of the video in format string and seperate each one by |, do not end with \n"
    promptRelevant = f"Analyze the provided video for its target audience effectiveness, the target audience are {aim['target audience']}. And is the tone appropriately coincides with {aim['video tone']}."
    # Set the model to Gemini 1.5 Pro.
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    # Make the LLM request.
    requestTitle = make_request(promptTitle, uploaded_files)
    responseTitle = model.generate_content(requestTitle, request_options={"timeout": 600})
    # requestTitleTag = make_request(promptTitleTag, uploaded_files)
    # responseTitleTag = model.generate_content(requestTitleTag, request_options={"timeout": 600})
    requestDescription = make_request(promptDescription, uploaded_files)
    responseDescription = model.generate_content(requestDescription, request_options={"timeout": 600})

    requestThumbnail = make_request(promptThumbnail, uploaded_files)
    responseThumbnail = model.generate_content(requestThumbnail,request_options={"timeout": 600})

    requestTags = make_request(promptTags, uploaded_files)
    responseTags = model.generate_content(requestTags)

    requestKeywords = make_request(promptKeywords, uploaded_files)
    responseKeywords = model.generate_content(requestKeywords)
    
    # Perform the search
    related_videos = YoutubeSearch(responseKeywords.text, max_results=10).to_dict()
    
    requestRelevant = make_request(promptRelevant, uploaded_files)
    responseRelevant = model.generate_content(requestRelevant)
    #store results into dict
    output = {"Title": responseTitle.text,
              "Description": responseDescription.text,
              "Thumbnail": responseThumbnail.text,
              "Tag": responseTags.text,
              "Relevance": responseRelevant.text,
              "RelatedVideo": related_videos #an array of dict, where includes id, thumbnails, title, long_desc, channel, duration, views, publish_time, url_suffix.
              }
    # delete frame folder
    shutil.rmtree(FRAME_EXTRACTION_DIRECTORY)
  else:
     st.info("Please present your topic and press Analyze button.")


# show in streamlit
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Titles", "Descriptions", "Thumbnails", "Tags", "Topic Relevance","Related Videos"])
with tab1:
  if output["Title"]:
    st.write(output["Title"])
with tab2:
  if output["Description"]:
    st.write(output["Description"])
with tab3:
  if output["Thumbnail"]:
    st.write(output["Thumbnail"])
with tab4:
  if output["Tag"]:
    st.write(output["Tag"])
with tab4:
  if output["Relevance"]:
    st.write(output["Relevance"])
with tab5:
  if output["RelatedVideo"]:
    for result in output["RelatedVideo"]:
      st.write('Title: ',result['title'])
      st.write(f"Video URL: https://www.youtube.com/watch?v={result['id']}")

if output['Title']:
  DownloadButton = st.button('Download Feedback')
  if DownloadButton:
    download_dict(output,uploaded_file.name,DOWNLOAD_DIR_VIDEO)
  else:
    st.info('Please press Analyze Button to get feedback.')

