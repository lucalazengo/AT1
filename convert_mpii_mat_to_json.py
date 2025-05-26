import scipy.io
import json
import os
from tqdm import tqdm
import numpy as np

# CONFIGURAÇÕES
MAT_FILE = "/home/lucala/HUB AI/case/mpii_dataset/annotations/mpii_human_pose_v1_u12_1.mat"
OUTPUT_DIR = "mpii_dataset/annotations_json"
CONSOLIDATED_JSON = "mpii_dataset/dataset_annotations.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def safe_extract_value(data, default=None):
    """Extrai valor de forma segura de arrays numpy/matlab"""
    try:
        if hasattr(data, 'size') and data.size == 0:
            return default
        while isinstance(data, np.ndarray):
            if data.size == 0:
                return default
            data = data[0]
        return data
    except (IndexError, AttributeError):
        return default

def parse_annotation(mat_data):
    release = mat_data['RELEASE'][0, 0]
    annolist = release['annolist'][0]
    act = release['act'][0]
    
    dataset = []
    
    for idx in tqdm(range(len(annolist)), desc="Processando anotações"):
        entry = {}
        image_info = annolist[idx]
        
        # Correção: garantir que img_name é str simples
        img_name = safe_extract_value(image_info['image']['name'])
        if isinstance(img_name, bytes):
            img_name = img_name.decode('utf-8')
        else:
            img_name = str(img_name) if img_name is not None else f"image_{idx}"
        
        entry['image'] = img_name
        entry['joints'] = []
        
        # Pode não haver anotações de pessoa
        annorect = image_info['annorect']
        if annorect.size > 0:
            for person in annorect[0]:
                if (person is not None and 
                    hasattr(person, 'dtype') and 
                    person.dtype.names is not None and
                    'annopoints' in person.dtype.names and 
                    person['annopoints'].size > 0):
                    try:
                        points_struct = person['annopoints'][0, 0]['point'][0]
                        for point in points_struct:
                            if point is None or not hasattr(point, 'dtype'):
                                continue
                            x_val = safe_extract_value(point['x'])
                            y_val = safe_extract_value(point['y'])
                            id_val = safe_extract_value(point['id'])
                            
                            is_visible_val = None
                            if ('is_visible' in point.dtype.names and 
                                point['is_visible'].size > 0):
                                is_visible_val = int(safe_extract_value(point['is_visible']))
                            
                            point_data = {
                                'x': int(x_val) if x_val is not None else 0,
                                'y': int(y_val) if y_val is not None else 0,
                                'id': int(id_val) if id_val is not None else 0,
                                'is_visible': is_visible_val
                            }
                            entry['joints'].append(point_data)
                    except Exception as e:
                        print(f"Erro ao processar pontos na imagem {img_name}: {e}")
                        continue
        
        # Atividade associada
        if idx < len(act):
            activity = act[idx]
            if (activity is not None and 
                hasattr(activity, 'size') and 
                activity.size > 0 and 
                hasattr(activity, 'dtype') and 
                activity.dtype.names is not None):
                act_entry = {}
                for field in ['act_name', 'cat_name', 'act_id']:
                    if field in activity.dtype.names:
                        val = safe_extract_value(activity[field])
                        if field == 'act_id':
                            val = int(val) if val is not None else None
                        else:
                            if isinstance(val, bytes):
                                val = val.decode('utf-8')
                    else:
                        val = None
                    act_entry[field] = val
                entry['activity'] = act_entry
            else:
                entry['activity'] = None
        else:
            entry['activity'] = None
        
        dataset.append(entry)
        
        # Salvar individualmente
        try:
            safe_filename = img_name.replace('/', '_').replace('\\', '_')
            img_json_path = os.path.join(OUTPUT_DIR, safe_filename + '.json')
            with open(img_json_path, 'w') as f:
                json.dump(entry, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar arquivo para imagem {img_name}: {e}")
    
    return dataset

def main():
    print("Carregando arquivo .mat...")
    try:
        mat_data = scipy.io.loadmat(MAT_FILE)
    except Exception as e:
        print(f"Erro ao carregar arquivo .mat: {e}")
        return
    
    print("Convertendo para JSON...")
    try:
        dataset = parse_annotation(mat_data)
    except Exception as e:
        print(f"Erro durante conversão: {e}")
        return
    
    print(f"Salvando JSON consolidado em {CONSOLIDATED_JSON}...")
    try:
        with open(CONSOLIDATED_JSON, 'w') as f:
            json.dump(dataset, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar JSON consolidado: {e}")
        return
    
    print("Conversão concluída com sucesso.")
    print(f"Total de imagens processadas: {len(dataset)}")

if __name__ == "__main__":
    main()
