import os
import json
import cv2

ANNOTATIONS_DIR = "mpii_dataset/annotations_json"
IMAGES_DIR = "mpii_dataset/images"
OUTPUT_DIR = "mpii_dataset/sample_visuals"

CLASSES = ["em_pe", "sentado", "movimento"]
SAMPLES_PER_CLASS = 100

def draw_joints(image_path, joints, output_path):
    img = cv2.imread(image_path)
    if img is None:
        return False

    for joint in joints:
        x, y = joint['x'], joint['y']
        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, img)
    return True

def main():
    for posture in CLASSES:
        txt_file = f"mpii_dataset/posture_classes/{posture}.txt"

        if not os.path.exists(txt_file):
            print(f"Arquivo de classe não encontrado: {txt_file}")
            continue

        with open(txt_file, 'r') as f:
            images = [line.strip() for line in f.readlines()]

        # Organizar por maior número de joints
        images_info = []

        for img_name in images:
            json_file = os.path.join(ANNOTATIONS_DIR, img_name.replace('/', '_') + '.json')
            if os.path.exists(json_file):
                with open(json_file, 'r') as jf:
                    data = json.load(jf)
                    joints = data.get('joints', [])
                    images_info.append((img_name, len(joints)))

        # Ordenar: mais joints primeiro
        images_info.sort(key=lambda x: x[1], reverse=True)

        count = 0
        tried = 0

        for img_name, _ in images_info:
            if count >= SAMPLES_PER_CLASS:
                break

            json_file = os.path.join(ANNOTATIONS_DIR, img_name.replace('/', '_') + '.json')
            img_path = os.path.join(IMAGES_DIR, img_name)
            output_path = os.path.join(OUTPUT_DIR, posture, img_name.replace('/', '_'))

            with open(json_file, 'r') as jf:
                data = json.load(jf)
                joints = data.get('joints', [])

            success = draw_joints(img_path, joints, output_path)

            if success:
                count += 1
            else:
                continue  # tenta a próxima imagem

            tried += 1

        print(f"{count} exemplos gerados para a classe '{posture}'. Tentou {tried} imagens.")

if __name__ == "__main__":
    main()
