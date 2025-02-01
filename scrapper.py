from TikTokApi import TikTokApi
import asyncio
import json

# TikTok session token
ms_token = "Wc1nuhaCw23HoVKwkFp2vanvAbKTHvEYkclI34gDN2hihsaLLoP7Xdo42heYbr1KNWn0WfIPE634HZVRtDhhBD957btjVDdtPNoFZB_8-PGRfGb8G7ldLonuaIuUDLPcb__mjXfNHtkoonjlkG08fttO"

# Fetch high-engagement TikTok videos
async def get_high_engagement_videos():
    async with TikTokApi() as api:
        # Initialize session with TikTok API
        await api.create_sessions(
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=3,
            browser="chromium",  # Adjust browser type if needed
            headless=False       # Set to True for headless mode
        )

        # Define hashtag
        hashtag_name = "text"
        tag = api.hashtag(name=hashtag_name)

        video_data_list = []  # List to store video metadata

        try:
            # Fetch videos for the hashtag
            async for video in tag.videos(count=50):  # Adjust count as needed
                video_data = video.as_dict
                if video_data:
                    # Extract engagement metrics
                    likes = video_data.get("stats", {}).get("diggCount", 0)
                    comments = video_data.get("stats", {}).get("commentCount", 0)
                    shares = video_data.get("stats", {}).get("shareCount", 0)
                    engagement_score = likes + comments + shares

                    # Extract video link (or reconstruct if missing)
                    share_url = video_data.get("share_url")
                    author = video_data.get("author", {}).get("uniqueId", "Unknown")
                    video_id = video_data.get("id")
                    if not share_url and author != "Unknown":
                        share_url = f"https://www.tiktok.com/@{author}/video/{video_id}"

                    # Append video details to the list
                    video_data_list.append({
                        "id": video_id,
                        "description": video_data.get("desc", ""),
                        "likes": likes,
                        "comments": comments,
                        "shares": shares,
                        "engagement_score": engagement_score,
                        "share_url": share_url,
                        "region": video_data.get("region", "Unknown"),
                        "language": video_data.get("lang", "Unknown"),
                    })

            # Sort videos by engagement score in descending order
            video_data_list.sort(key=lambda x: x["engagement_score"], reverse=True)

            # Save videos to a JSON file
            with open("high_engagement_videos.json", "w") as json_file:
                json.dump(video_data_list, json_file, indent=4)

            # Save shareable links to a text file
            with open("video_links.txt", "w") as txt_file:
                for video in video_data_list:
                    if video["share_url"]:
                        txt_file.write(video["share_url"] + "\n")

            # Print top 5 videos for quick review
            for video in video_data_list[:5]:
                print(f"Video URL: {video['share_url']}, Engagement Score: {video['engagement_score']}")

            print("High engagement videos saved to high_engagement_videos.json")
            print("Video links saved to video_links.txt")

        except Exception as e:
            print(f"Error occurred while fetching videos: {e}")

# Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(get_high_engagement_videos())
