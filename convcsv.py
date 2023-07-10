import csv

input_file = "syllabus.csv"
output_file = "combined_data.txt"

with open(input_file, "r", encoding="utf-8") as csvfile, open(output_file, "w", encoding="utf-8") as outfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames

    combined_data_list = []  # 連結データを格納するリスト

    for row in reader:
        subject_number = row[fieldnames[0]]
        subject_name = row[fieldnames[1]]
        instructor_name = row[fieldnames[2]]
        schedule = row[fieldnames[3]]

        # ハイフンをアンダースコアに置換し、空白を削除し、大文字を小文字に変換
        schedule = schedule.replace("-", "_").replace("　", "").lower()
        subject_name = subject_name.replace("-", "_").replace(" ", "").replace("　", "").lower()
        instructor_name = instructor_name.replace("-", "_").replace(" ", "").replace("　", "").lower()
        subject_number = subject_number.replace("-", "_").replace(" ", "").replace("　", "_").lower()

        # 曜時限_科目名_氏名_科目ナンバリングの連結
        combined_data = f"{schedule}_{subject_name}_{instructor_name}_{subject_number}"
        combined_data_list.append(combined_data)

    combined_data_str = ",".join(combined_data_list)  # 連結データをカンマで区切る
    outfile.write(combined_data_str)

print("連結データの生成が完了しました。")
