import os
from typing import List, Any, Union
from apiclient.discovery import build
import pandas as pd

# Replace with your own API key
# You set it up with instructions here: https://developers.google.com/youtube/v3/quickstart/python
DEVELOPER_KEY = "AIzaSyC-eXn8oS9Ry9hSipgyelk_01KlMxr-ozE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
# Limit for number of request you make for comment pages --> 5 gets you 500 comments
# There is a limit because Youtube has a quota on number of pulls / data actions you can have per day
LIMIT = 5

# Max results is the number of search results you want it to iterate through
def youtube_search(q, max_results=5, order="relevance", token=None, location=None, location_radius=None):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=q + " Trailer",
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",  # Part signifies the different types of data you want
        maxResults=max_results,
        location=location,
        locationRadius=location_radius).execute()

    search_data: List[List[Union[Union[str, List[Any]], Any]]] = []

    for search_result in search_response.get("items", []):

        title = ""
        channelTitle = ""
        viewCount = ""
        likeCount = ""
        dislikeCount = ""
        favoriteCount = ""
        tags = []
        comments = []
        comments_date = []
        upload = ""
        description = ""

        if search_result["id"]["kind"] == "youtube#video":
            title = (search_result['snippet']['title'])

            response = youtube.videos().list(
                part='statistics, snippet',
                id=search_result['id']['videoId']).execute()

            channelTitle = response['items'][0]['snippet']['channelTitle']
            favoriteCount = response['items'][0]['statistics']['favoriteCount']
            viewCount = response['items'][0]['statistics']['viewCount']
            likeCount = response['items'][0]['statistics']['likeCount']
            dislikeCount = response['items'][0]['statistics']['dislikeCount']
            upload = response['items'][0]['snippet']['publishedAt']
            description = response['items'][0]['snippet']['description']

            if 'commentCount' in response['items'][0]['statistics'].keys():
                commentCount = response['items'][0]['statistics']['commentCount']
            else:
                commentCount = ""

            if 'tags' in response['items'][0]['snippet'].keys():
                tags = response['items'][0]['snippet']['tags']

            comments_list = youtube.commentThreads().list(
                textFormat="plainText",
                part='snippet, replies',
                videoId=search_result['id']['videoId'],
                maxResults=100).execute()
            count = 1
            while True and count <= LIMIT:
                for comment in comments_list['items']:
                    comments.append(comment['snippet']['topLevelComment']['snippet']['textDisplay'])
                    comments_date.append(comment['snippet']['topLevelComment']['snippet']['publishedAt'])
                try:
                    nextPageToken = comments_list['nextPageToken']
                    comments_list = youtube.commentThreads().list(
                        textFormat="plainText",
                        part='snippet, replies',
                        videoId=search_result['id']['videoId'],
                        maxResults=100,
                        pageToken=nextPageToken).execute()
                    count += 1
                except:
                    break

        data_point = [q, title, upload, description, tags, viewCount, likeCount,
                      dislikeCount, favoriteCount, commentCount, comments, comments_date, channelTitle]
        search_data.append(data_point)

    print("Done: {}".format(q))
    return search_data


data = []
# This list is where you write your movie titles
search_terms = ["Joker", "Mulan", "Parasite"]

for search_term in search_terms:
    entries = youtube_search(search_term)
    for entry in entries:
        data.append(entry)

df = pd.DataFrame(data,
                  columns=["Movie", "Title", "Upload", "Description", "Tags", "ViewCount", "LikeCount", "DislikeCount",
                           "FavoriteCount", "CommentCount", "Comments", "CommentDates", "ChannelTitle"])

# If file doesn't exist yet, make the file with headers, else, append to existing file
if os.path.isfile('./YoutubeAPI.csv'):
    df.to_csv('YoutubeAPI.csv', encoding="UTF-8", mode='a', header=False, index=False)
else:
    df.to_csv('YoutubeAPI.csv', encoding="UTF-8", index=False)
