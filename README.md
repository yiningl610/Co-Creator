# Co-Creator
An App help youtuber to achieve best views for the uploading video for Gemini Hackathon

## Inspiration
Many aspiring YouTubers struggle with the non-video aspects of content creation, such as scriptwriting, title development, and video descriptions. This project aims to address these challenges by providing an AI-powered tool that assists creators throughout the process.

## What it does
There are three main functionality in Co-creator, which can work individually or in combination.  
- Script Maker - Users input the video type and desired content, and Co-Creator generates a detailed script for the video.
- Style Advisor - Based on a finished script, target audience, and desired video tone, Co-Creator suggests music, color palettes, and editing techniques to achieve the user's vision.
- Upload Helper - This feature automates the pre-upload tasks by generating video titles, descriptions, and relevant hashtags. It even provides similar existing videos for reference.

## How we built it
Co-Creator is built using Streamlit, an open-source Python framework for creating interactive applications. Python serves as the primary programming language.

## Challenges we ran into
The primary challenge involved ensuring the generated outputs align precisely with user expectations. To address this, the team conducted extensive testing with various prompt wordings and implemented limitations to refine the results.

## Accomplishments that we're proud of
While primarily known for text analysis, Co-Creator successfully incorporates video processing through OpenCV, allowing it to analyze video content captured from frames.

## What's next for Co-Creator
Co-Creator currently faces limitations in file size (200MB) and video analysis runtime. Expanding the file size limit and optimizing video processing speed are key priorities for future development.

## Built With
python
streamlit
youtubesearch
# Try it out
co-creator.streamlit.app
