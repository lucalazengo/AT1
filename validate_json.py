import os
import json

INPUT_DIR = "mpii_dataset/annotations_json"

def validate_json_structure(json_data, filename):
    if not isinstance(json_data.get('image'), str):
        print(f"Erro: 'image' inválido em {filename}")
        return False
    if not isinstance(json_data.get('joints'), list):
        print(f"Erro: 'joints' inválido em {filename}")
        return False
    activity = json_data.get('activity')
    if activity is not None and not isinstance(activity, dict):
        print(f"Erro: 'activity' inválido em {filename}")
        return False
    return True

def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.json')]
    print(f"Validando {len(files)} arquivos JSON...")

    valid_count = 0
    for file in files:
        with open(os.path.join(INPUT_DIR, file), 'r') as f:
            data = json.load(f)
            if validate_json_structure(data, file):
                valid_count += 1

    print(f"Arquivos válidos: {valid_count}/{len(files)}")

if __name__ == "__main__":
    main()
