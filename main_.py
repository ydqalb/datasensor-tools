import json
import re
import beanstalk as b

list_input = []
platforms = []
list_tubes = {
    # keyword
    "sc_youtube_post_keyword_alt_tes_tools": "192.168.150.21",
    "sc_twitter_history_keyword_tes_tools": "192.168.20.175",
    "sc_tiktok_keyword_search_recovery_tes_tools": "192.168.20.175",
    "sc_instagram_post_keyword_tes_tools": "192.168.20.175",
    "sc_helo_apps_keyword_tes_tools": "192.168.20.175",
    # account
    "sc_youtube_post_alt_tes_tools": "192.168.150.21",
    "sc_fb_feed_page_tes_tools": "192.168.150.21",
    "sc_fb_feed_personal_tes_tools": "192.168.150.21",
    "sc_instagram_account_tes_tools": "192.168.20.175",
    "sc_twitter_history_account_tes_tools": "192.168.20.175"
}


def choose_tube():
    for platform in platforms:
        for k, v in list_tubes.items():
            if re.search(r"" + platform, k):
                yield k, v, platform


def job_account(since, until=None, track_comment=None):
    for k, v, p in choose_tube():
        for lines in list_input:
            if p == "instagram_account":
                line = lines.replace("\r\n", "")
                data = {
                    "username": line,
                    "track_comment": track_comment,
                    "setting": {
                        "cache": False,
                        "since": since,
                        "until": until
                    }
                }
            elif p == "twitter_history_account":
                line = lines.replace("\r\n", "")
                data = {
                    "screen_name": line,
                    "since": since,
                    "revisit": True
                }
            elif p == "youtube_post_alt":
                line = lines.replace("\r\n", "")
                data = {
                    "channel_id": line,
                    "since": since,
                    "cache": True
                }
            elif p == "fb_feed_page":
                line = lines.replace("\r\n", "")
                data = {
                    "id": line,
                    "since": since,
                    "revisit": True
                }
            elif p == "fb_feed_personal":
                line = lines.replace("\r\n", "")
                data = {
                    "id": line,
                    "since": since,
                    "revisit": True
                }
            else:
                data = "NO JOB AVAILABLE"

            data_ = json.dumps(data)
            beans = b.Beanstalk(host=v)
            beans.push(platform=p, body=data_, tube=k)
    platforms.clear()
    list_input.clear()


def job_keyword(since=None):
    for k, v, p in choose_tube():
        for lines in list_input:
            if p == "tiktok\_.*keyword":
                line = lines.replace("\r\n", "")
                data = {
                    "sec_id": None,
                    "account_id": None,
                    "following_id": None,
                    "user_id": None,
                    "post_id": None,
                    "from_web": None,
                    "cursor": 0,
                    "post": {

                    },
                    "keyword": line,
                    "keyword_id": None
                }
            else:
                line = lines.replace("\r\n", "")
                data = {
                    "keyword": line,
                    "cache": False,
                    "since": since
                }

            data_ = json.dumps(data)
            beans = b.Beanstalk(host=v)
            beans.push(platform=p, body=data_, tube=k)
    platforms.clear()
    list_input.clear()
    # b.Beanstalk().close()

# job_keyword(since="2022-01-01")
# job_instagram(since="2022-01-01",until="2023-01-02")
