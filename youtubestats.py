from googleapiclient.discovery import build  # - helps us connect to youtube API
import pandas as pd # - for data manipulations
from dateutil import parser # - for parsing dates
import isodate
from IPython.display import JSON

def get_channel_stats(youtube,channel_ids):
    '''Get channel statistics: title, subscriber count, view count, video count, upload playlist
    Params:
    
    youtube: the build object from googleapiclient.discovery - - needed for API request
    channels_ids: list of channel IDs we want to search
    
    Returns:
    all variables under "get channel statistics" as dataframe for all channels in the provided list
    
    '''
    all_data = []
    
    request = youtube.channels().list(
        part = "snippet,contentDetails,statistics",
        id = ''.join(channel_ids)
    )
    response = request.execute()
    
    # Loop through the items
    for item in response['items']:
        data = {
            'channelName' : item['snippet']['title'],
            'subscribers' : item['statistics']['subscriberCount'],
            'views': item['statistics']['viewCount'],
            'totalVideos': item['statistics']['videoCount'],
            'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
        }
        
        all_data.append(data)
    
    return pd.DataFrame(all_data)
    

def get_video_id(youtube,playlist_id):
    """
    Get list of video IDs of all videos in the given playlist
    Params:
    
    youtube: the build object from googleapiclient.discovery - needed for API request
    playlist_id: playlist ID of the channel
    
    """
    videoIds = []
    
    
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults = 50
    )
    
    response = request.execute()
        
    for item in response['items']:
        videoIds.append(item['contentDetails']['videoId'])
    
    return videoIds


    '''
    Incase we want more than 50 results we can include the below to accomodate which will gets next page of results 
    till we have no more.
    
    next_pagetoken = response.get('nextPageToken')
    while next_pagetoken is not None:
    request = youtube.playlistItems().list(
    part="snippet,contentDetails",
    playlistId="UUoSxzVDrViaWSTBa5DJDfVg",
    maxResults = 50
    )

    for item in response['items']:
    videoIds.append(item['contentDetails']['videoId'])
    '''
def get_video_info(youtube, video_ids):
    """
    Get video statistics of all videos with given IDs
    Params:
    
    youtube: the build object from googleapiclient.discovery - needed for API request 
    video_ids: list of video IDs

    """
    all_video_info = []
    
    for i in range(0, len(video_ids),50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id = ','.join(video_ids[i:i+50])
        )
        response = request.execute()

    for video in response['items']:
        stats_to_keep = {'snippet':['channelTitle','title','description','tags','publishedAt'],
                         'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                         'contentDetails':['duration','definition','caption']
                        }
        video_info = {}
        video_info['video_id'] = video['id']
        for k in stats_to_keep.keys():
            for v in stats_to_keep[k]:
                try:
                    video_info[v] = video[k][v]
                except:
                    video_info[v] = None

        all_video_info.append(video_info)
    return pd.DataFrame(all_video_info)    

