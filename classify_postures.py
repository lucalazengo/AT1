import os
import json
import numpy as np

ANNOTATIONS_DIR = "mpii_dataset/annotations_json"
OUTPUT_DIR = "mpii_dataset/posture_classes"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_joint_by_id(joints, joint_id):
    """Retorna a posição de um joint específico."""
    for joint in joints:
        if joint['id'] == joint_id:
            return (joint['x'], joint['y'])
    return None

def classify_posture(joints):
    """Classifica postura baseada na relação altura/largura dos joints."""
    
    # IDs dos pontos principais:
    HEAD_ID = 9  # Head top
    FEET_IDS = [0, 5]  # R ankle e L ankle
    SHOULDER_IDS = [12, 13]  # R shoulder e L shoulder

    # Obter pontos
    head = get_joint_by_id(joints, HEAD_ID)
    feet = [get_joint_by_id(joints, fid) for fid in FEET_IDS]
    shoulders = [get_joint_by_id(joints, sid) for sid in SHOULDER_IDS]

    # Checar se pontos principais existem
    if not head or not all(feet) or not all(shoulders):
        return None  # Não classifica se faltar informação

    # Cálculo de Altura: distância head → ankle médio
    feet_mid = ((feet[0][0] + feet[1][0]) / 2, (feet[0][1] + feet[1][1]) / 2)
    altura = abs(head[1] - feet_mid[1])

    # Cálculo de Largura: distância entre ombros
    largura = abs(shoulders[0][0] - shoulders[1][0])

    if largura == 0:
        return None  # Evitar divisão por zero

    relacao = altura / largura

    # Regras simples:
    if relacao > 1.5:
        return 'em_pe'
    elif 0.8 <= relacao <= 1.5:
        return 'sentado'
    else:
        return 'movimento'

def main():
    files = [f for f in os.listdir(ANNOTATIONS_DIR) if f.endswith('.json')]

    classes = {'em_pe': [], 'sentado': [], 'movimento': [], 'nao_classificado': []}

    for file in files:
        with open(os.path.join(ANNOTATIONS_DIR, file), 'r') as f:
            data = json.load(f)
            joints = data.get('joints', [])
            posture = classify_posture(joints)
            if posture:
                classes[posture].append(data['image'])
            else:
                classes['nao_classificado'].append(data['image'])

    # Salvar listas
    for posture, images in classes.items():
        with open(os.path.join(OUTPUT_DIR, f"{posture}.txt"), 'w') as f:
            for img in images:
                f.write(f"{img}\n")

    # Relatório
    for posture, images in classes.items():
        print(f"{posture}: {len(images)} imagens")

if __name__ == "__main__":
    main()
