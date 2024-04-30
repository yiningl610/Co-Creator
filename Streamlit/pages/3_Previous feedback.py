from utils import *
st.markdown("# Previous Feedback")
st.write(
    """This page will reload historical downloaded feedback files from default folder cocreater.
       Or you can upload from other path.
    """
)
# Load json file from cocreater/draft_video_feedback
feedback_files = load_feedback_files(DOWNLOAD_DIR_VIDEO)
# Subpage navigation (if there are feedback files)
if feedback_files:
  for file in feedback_files:
    # Get subpage name from filename (excluding extension)
    page_name = file['filename'].split(".")[0] 
    data = file['data']
    # Create subpages
    with st.expander(page_name):
      st.subheader(f'Feedback from: {page_name}')
      # Display the content of the selected feedback file on the subpage
      show_video_feedback(data)

# Informative message if there are no feedback files
else:
  st.info("No local feedback files found yet. Download some results to view them here.")
  st.write("Please upload a JSON file containing the feedback dictionary.")

  # File upload functionality
  uploaded_file = st.file_uploader("Upload JSON File", type="json")

  # Process uploaded file (if any)
  if uploaded_file is not None:
    try:
      # Read the uploaded file content
      data = json.load(uploaded_file)
      st.success("File uploaded successfully!")

      # Display the uploaded data (optional)
      show_video_feedback(data)
    except json.JSONDecodeError as e:
      st.error("Error: Invalid JSON file. Please upload a valid JSON file.")
  else:
    st.info("No file uploaded yet.")