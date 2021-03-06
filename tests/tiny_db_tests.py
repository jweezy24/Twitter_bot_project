import unittest
import sys
sys.path.append("../src/twitter_bot")
from tiny_db_calls import *


temp_tweet = {'created_at': 'Wed Feb 17 02:55:52 +0000 2021', 'id': 1361871962901934082, 'id_str': '1361871962901934082', 'text': "Photographer captures moment woman is told she's sitting in a big bean bag chair https://t.co/bkac8oyFuw", 'truncated': False, 'entities': {'hashtags': [], 'symbols': [], 'user_mentions': [], 'urls': [], 'media': [{'id': 1361871915430801413, 'id_str': '1361871915430801413', 'indices': [81, 104], 'media_url': 'http://pbs.twimg.com/media/EuZXSqTVcAUE1WA.jpg', 'media_url_https': 'https://pbs.twimg.com/media/EuZXSqTVcAUE1WA.jpg', 'url': 'https://t.co/bkac8oyFuw', 'display_url': 'pic.twitter.com/bkac8oyFuw', 'expanded_url': 'https://twitter.com/mc_lotta/status/1361871962901934082/photo/1', 'type': 'photo', 'sizes': {'thumb': {'w': 150, 'h': 150, 'resize': 'crop'}, 'small': {'w': 510, 'h': 680, 'resize': 'fit'}, 'medium': {'w': 900, 'h': 1200, 'resize': 'fit'}, 'large': {'w': 1536, 'h': 2048, 'resize': 'fit'}}}]}, 'extended_entities': {'media': [{'id': 1361871915430801413, 'id_str': '1361871915430801413', 'indices': [81, 104], 'media_url': 'http://pbs.twimg.com/media/EuZXSqTVcAUE1WA.jpg', 'media_url_https': 'https://pbs.twimg.com/media/EuZXSqTVcAUE1WA.jpg', 'url': 'https://t.co/bkac8oyFuw', 'display_url': 'pic.twitter.com/bkac8oyFuw', 'expanded_url': 'https://twitter.com/mc_lotta/status/1361871962901934082/photo/1', 'type': 'photo', 'sizes': {'thumb': {'w': 150, 'h': 150, 'resize': 'crop'}, 'small': {'w': 510, 'h': 680, 'resize': 'fit'}, 'medium': {'w': 900, 'h': 1200, 'resize': 'fit'}, 'large': {'w': 1536, 'h': 2048, 'resize': 'fit'}}}, {'id': 1361871915548254211, 'id_str': '1361871915548254211', 'indices': [81, 104], 'media_url': 'http://pbs.twimg.com/media/EuZXSqvVoAMuKK_.jpg', 'media_url_https': 'https://pbs.twimg.com/media/EuZXSqvVoAMuKK_.jpg', 'url': 'https://t.co/bkac8oyFuw', 'display_url': 'pic.twitter.com/bkac8oyFuw', 'expanded_url': 'https://twitter.com/mc_lotta/status/1361871962901934082/photo/1', 'type': 'photo', 'sizes': {'thumb': {'w': 150, 'h': 150, 'resize': 'crop'}, 'large': {'w': 1536, 'h': 2048, 'resize': 'fit'}, 'small': {'w': 510, 'h': 680, 'resize': 'fit'}, 'medium': {'w': 900, 'h': 1200, 'resize': 'fit'}}}]}, 'source': '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None, 'user': {'id': 343733969, 'id_str': '343733969', 'name': 'Charlotte McGrath', 'screen_name': 'mc_lotta', 'location': 'Los Angeles, CA', 'description': 'Of having a fat ass fame | @FunhausTeam | https://t.co/1qkAbSUee3 Wed @ 7 PST\n\nMusic @ https://t.co/KObuR9V1N8\n\nshe/her', 'url': 'https://t.co/CuCaRlf5cV', 'entities': {'url': {'urls': [{'url': 'https://t.co/CuCaRlf5cV', 'expanded_url': 'http://youtube.com/insidegaming', 'display_url': 'youtube.com/insidegaming', 'indices': [0, 23]}]}, 'description': {'urls': [{'url': 'https://t.co/1qkAbSUee3', 'expanded_url': 'http://twitch.tv/whatashow', 'display_url': 'twitch.tv/whatashow', 'indices': [42, 65]}, {'url': 'https://t.co/KObuR9V1N8', 'expanded_url': 'https://spoti.fi/3jpJkjE', 'display_url': 'spoti.fi/3jpJkjE', 'indices': [87, 110]}]}}, 'protected': False, 'followers_count': 19154, 'friends_count': 598, 'listed_count': 25, 'created_at': 'Thu Jul 28 00:33:23 +0000 2011', 'favourites_count': 18880, 'utc_offset': None, 'time_zone': None, 'geo_enabled': True, 'verified': False, 'statuses_count': 9758, 'lang': None, 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': '55B4E0', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1355676207031836673/BPO0eiQU_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1355676207031836673/BPO0eiQU_normal.jpg', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/343733969/1606460119', 'profile_link_color': 'F77C0A', 'profile_sidebar_border_color': 'FFFFFF', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 'has_extended_profile': False, 'default_profile': False, 'default_profile_image': False, 'following': False, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none'}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'retweet_count': 7, 'favorite_count': 973, 'favorited': False, 'retweeted': False, 'possibly_sensitive': False, 'lang': 'en'}




class TestTinyDBCalls(unittest.TestCase):

    def test_save(self):
        res = save_value(temp_tweet)
        self.assertTrue(save_value(temp_tweet) != None)

    def test_save(self):
        res = search_value(temp_tweet["id"])
        self.assertTrue(res)

    def test_get_all_favorites(self):
        res = get_all_favorites('alittl3ton13')
        self.assertTrue(res == [])
        res = get_all_favorites('alittl3ton13',table="favorite_tbl")
        self.assertTrue(res != [])
        self.assertTrue(type(res) == type([]))
        self.assertTrue(len(res) > 0)

    def test_get_minimum(self):
        min_ = get_minimum_id('alittl3ton13', 'favorite_tbl')
        print(min_)




if __name__ == "__main__":
    suite = unittest.main()