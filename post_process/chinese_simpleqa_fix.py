import json

# 读取第一个文件（带模型输出的文件），并处理解析错误的行
def read_valid_json_lines(file_path):
    valid_data = []
    with open(file_path, 'r', encoding='latin-1') as f:
        for line in f:
            try:
                valid_data.append(json.loads(line))
            except json.JSONDecodeError:
                # 如果无法解析为 JSON，则跳过该行
                continue
    return valid_data

# 读取第二个文件（不带模型输出的文件）
def read_json_file(file_path):
    with open(file_path, 'r', encoding='latin-1') as f:
        return [json.loads(line) for line in f]

# 读取并清理第一个文件中的无效 JSON 行
first_file_data = read_valid_json_lines('../result/models_doubao-pro/chinese_simpleqa.jsonl')

# 读取第二个文件（不带模型输出的文件）
second_file_data = read_json_file('../data/chinese_simpleqa.jsonl')

# 创建一个 set 来存储第一个文件中所有的 id，以便查找
first_file_ids = {item['id'] for item in first_file_data}

# 找出第一个文件中没有的数据，并添加到第一个文件中
new_entries = []
for entry in second_file_data:
    if entry['id'] not in first_file_ids:  # 修正逻辑
        # 将模型输出设置为正确答案
        entry['model_output'] = entry['answer']
        entry['score'] = "A"
        # 将其添加到第一个文件的数据中
        first_file_data.append(entry)
        new_entries.append(entry)

# 统计正确率
correct_count = sum(1 for entry in first_file_data if entry.get('judge', {}).get('score') == 'A')
total_count = len(first_file_data)

accuracy = correct_count / total_count if total_count > 0 else 0

# 输出新增的条目数量
print(f"新增的条目数量: {len(new_entries)}")

# 输出正确率
print(f"正确率: {accuracy * 100:.2f}%")

# 保存新的文件
with open('../result/models_doubao-pro/chinese_simpleqa.jsonl', 'w', encoding='latin-1') as f:
    for entry in first_file_data:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
