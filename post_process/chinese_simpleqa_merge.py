import os
import json
import csv
import glob

def merge_json_to_csv(input_dir, output_file):
    # 存储所有模型列表
    models = [
        'gemini-1.5', 'gpt-4o', 'qwen-plus', 'yi-lightning', '360gpt2-pro'
    ]

    # 存储问题数据的字典
    questions_data = {}

    # 遍历目录中的所有 JSONL 文件
    for json_file in glob.glob(os.path.join(input_dir, '*.jsonl')):
        # 从文件名中提取模型名称
        model = os.path.basename(json_file).split('.jsonl')[0]

        if model not in models:
            raise Exception(f"Invalid model name: {model}")

        with open(json_file, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line.strip())

                # 使用问题 ID 作为唯一标识
                question_id = data['id']

                # 初始化问题数据
                if question_id not in questions_data:
                    questions_data[question_id] = {
                        'question_id': question_id,
                        'question': data['question'],
                        'model_results': {m: 1 for m in models}
                    }

                if data['score'] == 'A':
                    result = 1
                else:
                    result = 0

                # 更新模型结果
                questions_data[question_id]['model_results'][model] = result

    # 写入 CSV 文件
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        # 添加 BOM
        csvfile.write(u'\ufeff')

        # 定义 CSV 表头
        fieldnames = ['question_id', 'question'] + models
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # 写入表头
        writer.writeheader()

        # 写入每行数据
        for question_id, question_data in questions_data.items():
            row = {
                'question_id': question_id,
                'question': question_data['question']
            }
            row.update(question_data['model_results'])
            writer.writerow(row)

    print(f"CSV 文件已生成: {output_file}")

input_directory = '../result/chinese_simpleqa'
output_csv_file = '../result/chinese_simpleqa/chinese_simpleqa_results.csv'

merge_json_to_csv(input_directory, output_csv_file)