import json
import re

# 外部のJSONファイルを読み込み
with open('site.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 各講義のdescriptionと講師名を取得し、テキストファイルに出力
with open('descriptions.txt', 'w', encoding='utf-8') as file:
    for site in data['site_collection']:
        description = site['description']
        instructor = site['siteOwner']['userDisplayName']

        # 不要なタグや説明文を除去
        description = re.sub(r'<[^>]+>', '', description)
        description = re.sub(r'\s+', ' ', description).strip()

        # 空白が現れた場合、空白を含めてそれ以下の部分を削除
        if ' ' in description:
            description = description[:description.index(' ')]

        # 出力
        file.write(f"{description} - {instructor}\n")

