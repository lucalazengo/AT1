
# AT1 — Classificação de Posturas Humanas com o Dataset MPII

Este projeto consiste na criação e análise de um subconjunto de dados do **MPII Human Pose Dataset** com foco na classificação de posturas humanas: **em pé**, **sentado** e **em movimento**.

## 📂 Estrutura do Projeto

```
.
├── AT1_analysis.ipynb
├── convert_mpii_mat_to_json.py
├── classify_postures.py
├── draw_samples_by_class.py
├── extract_mpii.py
├── generate_graphs.py
├── validate_json.py
├── README.md
├── mpii_dataset
│   ├── annotations
│   ├── annotations_json
│   ├── dataset_annotations.json
│   ├── images
│   ├── posture_classes
│   └── sample_visuals
└── data
```

## ✅ Pré-requisitos

- Python >= 3.8
- Bibliotecas:

```
pip install numpy pandas matplotlib seaborn opencv-python tqdm scipy
```

## ✅ Como Rodar o Projeto

### 1. extrair o dataset


```
python extract_mpii.py
```

### 2. Converter anotações

```
python convert_mpii_mat_to_json.py
```

### 3. Validar anotações

```
python validate_json.py
```

### 4. Classificar posturas

```
python classify_postures.py
```

### 5. Gerar exemplos visuais

```
python draw_samples_by_class.py
```

### 6. Gerar gráficos

```
python generate_graphs.py
```

### 7. Análise via notebook

```
jupyter notebook AT1_analysis.ipynb
```

## ✅ Relatório

O relatório final encontra-se em `Relatório/AT1_Report`.

## ✅ Referências

- MPII Human Pose Dataset: [http://human-pose.mpi-inf.mpg.de/](http://human-pose.mpi-inf.mpg.de/)
- Andriluka et al., 2014 — 2D Human Pose Estimation.
