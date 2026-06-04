from app.validator import validate_input_files, validate_master_files

target_month = "202606"

csv_files = validate_input_files(target_month)
validate_master_files()

print("入力CSVチェックOK")
print(csv_files)

print("マスタファイルチェックOK")
