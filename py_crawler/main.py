import requests
from bs4 import BeautifulSoup
import re
import os
import json


class Song:
    def __init__(self, song_title, singer_name, viewCount):
        self.song_title = song_title
        self.singer_name = singer_name
        self.viewCount = viewCount


def sort_songs_by_play_count(songs):
    return sorted(songs, key=lambda x: x.viewCount, reverse=True)


# 注意代理节点要是香港节点 HK
def crawl_for_youtube_playlist(playlist_id):  # 获取youtube专辑列表的歌曲名，歌手和播放量数据
    print('开始发送爬虫请求')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(f'https://www.youtube.com/playlist?list={playlist_id}', headers=headers)
    html = response.text
    # soup = BeautifulSoup(html, "html.parser")
    pattern = r'"title":(.*?),"index":{'
    matches = re.findall(pattern, html, re.DOTALL)

    dict_matches = [json.loads(match) for match in matches]
    Song_list = []
    for dict_match in dict_matches:
        song_title = re.split(' 建立者：', dict_match['accessibility']['accessibilityData']['label'])[0]
        exp_for_song_title = re.split(' 建立者：', dict_match['accessibility']['accessibilityData']['label'])[1]
        singer_name = re.split(' 收看次數：', exp_for_song_title)[0]
        exp_for_singer_name = re.split(' 收看次數：', exp_for_song_title)[1]
        viewCount_str = re.split(' 次', exp_for_singer_name)[0]
        viewCount = int(viewCount_str.replace(',', ''))
        song = Song(song_title, singer_name, viewCount)
        Song_list.append(song)

    Song_list = sort_songs_by_play_count(Song_list)
    i = 1
    with open('result.txt', 'w') as f:  # 输出结果保存至result.txt中
        for song in Song_list:
            f.write(f'[{i}]《{song.song_title}》 —— {song.singer_name}\n')
            f.write(f'--播放量: {song.viewCount}\n')
            print(f'[{i}]《{song.song_title}》 —— {song.singer_name}')
            print(f'--播放量: {song.viewCount}')
            i += 1
    result_path = os.getcwd()
    print(f'成功将结果保存至 {result_path}' + r'\result.txt 中')


if __name__ == '__main__':
    playlist_id = 'OLAK5uy_nyII7mzUzNzGtfPnBa3Auw_cazX9OmHdI'  # 播放列表的id
    crawl_for_youtube_playlist(playlist_id)