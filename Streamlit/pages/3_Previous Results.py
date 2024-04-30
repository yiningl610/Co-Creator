from utils import *

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
      tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Titles", "Descriptions", "Thumbnails", "Tags", "Topic Relevance","Related Videos"])
      with tab1:
         st.write(data["Title"])
      with tab2:
        st.write(data["Description"])
      with tab3:
        st.write(data["Thumbnail"])
      with tab4:
        st.write(data["Tag"])
      with tab5:
        st.write(data["Relevance"])
      with tab6:
        for result in data["RelatedVideo"]:
            st.write('Title: ',result['title'])
            st.write(f"Video URL: https://www.youtube.com/watch?v={result['id']}")

# Informative message if there are no feedback files
else:
  st.info("No feedback files found yet. Download some results to view them here.")