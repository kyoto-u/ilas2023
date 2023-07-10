import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://www.k.kyoto-u.ac.jp/external/open_syllabus/la_syllabus?lectureNo="
start_number = 50000
end_number = 99999

# CSVファイルの作成とヘッダーの書き込み
with open("syllabus.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["科目ナンバリング", "科目名", "氏名", "曜時限"])

    for lecture_number in range(start_number, end_number + 1):
        # 探索対象のURLを作成
        url = base_url + str(lecture_number).zfill(5)

        # リクエストを送信し、存在するページかどうかを確認
        response = requests.get(url)
        if response.status_code == 200:
            html = response.content.decode("cp932", "ignore")
            soup = BeautifulSoup(html, "html.parser")

            subject_number_element = soup.find("span", class_="lesson_plan_subheading", text="(科目ナンバリング)")
            if subject_number_element:
                subject_number = subject_number_element.find_next("td").get_text(strip=True)
            else:
                print("科目ナンバリングが見つかりませんでした。")
                continue

            subject_name_element = soup.find("span", class_="lesson_plan_subheading", text="(科目名)")
            if subject_name_element:
                subject_name = subject_name_element.find_next("td").get_text(strip=True)
            else:
                print("科目名が見つかりませんでした。")
                continue

            instructor_table = soup.find("table", cellspacing="0", cellpadding="0")
            if instructor_table:
                instructor_rows = instructor_table.find_all("tr")
                if len(instructor_rows) > 1:
                    instructor_name_elements = instructor_rows[1].find_all("td")
                    if len(instructor_name_elements) > 2:
                        instructor_name = instructor_name_elements[2].get_text(strip=True)
                    else:
                        print("氏名が見つかりませんでした。")
                        continue
                else:
                    print("氏名が見つかりませんでした。")
                    continue
            else:
                print("氏名が見つかりませんでした。")
                continue

            schedule_element = soup.find("span", class_="lesson_plan_subheading", text="(曜時限)")
            if schedule_element:
                schedule = schedule_element.find_next("td").get_text(strip=True)
            else:
                print("曜時限が見つかりませんでした。")
                continue

            # 抽出した情報をCSVファイルに書き込む
            writer.writerow([subject_number, subject_name, instructor_name, schedule])

            print("データを保存しました:", url)
        else:
            print("ページが存在しません:", url)

        time.sleep(1)  # 適度な時間の待機
