# Relatório AT1 - MPII Dataset

**Total de imagens analisadas:** 49978

**Média de joints por imagem:** 17.32

## Estatísticas Descritivas

count    49978.000000
mean        17.315459
std         20.436880
min          0.000000
25%          0.000000
50%         16.000000
75%         16.000000
max        256.000000
dtype: float64

## Distribuição de número de Joints

![Distribuição de Joints](mpii_dataset/joints_distribution.png)

## Distribuição de Atividades

A maioria das imagens **não possui anotações de atividade**.

## Considerações Finais

- O dataset apresenta variação considerável no número de joints por imagem.
- A maioria das imagens não possui anotações de atividade.
- Para inferência de posturas, recomenda-se usar técnicas de pose estimation.
