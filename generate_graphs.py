import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ajuste os caminhos conforme sua estrutura
ANNOTATIONS_DIR = "mpii_dataset/annotations_json"
OUTPUT_DIR = "mpii_dataset/"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Carregar todas as anotações
data = []

for file in os.listdir(ANNOTATIONS_DIR):
    if file.endswith('.json'):
        with open(os.path.join(ANNOTATIONS_DIR, file)) as f:
            d = json.load(f)
            num_joints = len(d.get('joints', []))
            activity = d.get('activity', {}).get('act_name') if d.get('activity') else None
            data.append({
                'image': d['image'],
                'num_joints': num_joints,
                'activity': activity
            })

df = pd.DataFrame(data)

print(f"Total de imagens: {len(df)}")
print(df.describe())

# Gráfico 1: Histograma do número de joints
plt.figure(figsize=(10,6))
sns.histplot(df['num_joints'], bins=30, kde=False, color='skyblue')
plt.title('Histograma da Distribuição do Número de Joints')
plt.xlabel('Número de Joints')
plt.ylabel('Frequência')
plt.grid(True)
plt.savefig(os.path.join(OUTPUT_DIR, 'hist_joints.png'))
plt.show()

# Gráfico 2: Boxplot do número de joints
plt.figure(figsize=(8,6))
sns.boxplot(x=df['num_joints'], color='lightgreen')
plt.title('Boxplot do Número de Joints por Imagem')
plt.xlabel('Número de Joints')
plt.savefig(os.path.join(OUTPUT_DIR, 'boxplot_joints.png'))
plt.show()

# Gráfico 3: Distribuição de atividades anotadas
activity_counts = df['activity'].value_counts()

plt.figure(figsize=(12,6))
sns.barplot(x=activity_counts.index[:20], y=activity_counts.values[:20], palette='viridis')
plt.xticks(rotation=90)
plt.title('Top 20 Atividades Anotadas no Dataset')
plt.xlabel('Atividade')
plt.ylabel('Frequência')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'activity_distribution.png'))
plt.show()

# Gráfico 4: Pie Chart - presença ou ausência de atividade
activity_presence = df['activity'].notnull().value_counts()

labels = []
colors = []

if True in activity_presence.index:
    labels.append('Com Atividade')
    colors.append('#66b3ff')

if False in activity_presence.index:
    labels.append('Sem Atividade')
    colors.append('#ff9999')

plt.figure(figsize=(6,6))
plt.pie(activity_presence.values, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('Distribuição: Presença de Anotação de Atividade')
plt.savefig(os.path.join(OUTPUT_DIR, 'activity_presence_pie.png'))
plt.show()

