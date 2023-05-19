import pandas as pd

df = pd.read_csv('dataset.csv')
df_sorted = df.sort_values(by='text')
df_sorted = df_sorted.drop_duplicates(subset='text')
df_sorted.to_csv('dataset_sorted.csv', index=False)

counts = df_sorted['emotions'].value_counts()
for emotion, count in counts.items():
    print(f'Emotion: {emotion}, Count: {count}')

min_sample = df_sorted['emotions'].value_counts().min()
print(min_sample)
data = pd.concat([df_sorted[df_sorted['emotions'] == e].sample(n=min_sample, random_state=42)
                  for e in df_sorted['emotions'].unique()])
column_titles = data.iloc[:1]
values = data.iloc[1:]
shuffled_values = values.sample(frac=1, random_state=42)
data = pd.concat([column_titles, shuffled_values], axis=0)
data.to_csv('balanced_dataset.csv', index=False)