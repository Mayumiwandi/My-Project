# -*- coding: utf-8 -*-
"""Laptop_Price_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12zJpF_zVNSbGpnbKEgFzoRIeaNK3sViM

# **Data Loading**
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import files
import zipfile
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

# Install public API Kaggle
!pip install kaggle

files.upload()

!mkdir ~/.kaggle
!cp kaggle.json ~/.kaggle
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d muhammetvarl/laptop-price

"""**load the dataset**"""

zip_ref = zipfile.ZipFile('/content/laptop-price.zip', 'r')
zip_ref.extractall('/content/')
zip_ref.close()

df = pd.read_csv('/content/laptop_price.csv', encoding="latin-1" )

print(f'\n\nTotal Datasets : {df.shape}\n\n\n')
df

df.info()

df = df.drop(['Product','laptop_ID'], axis= 1)

df.describe()

df.duplicated().sum()

df = df.drop_duplicates()

df.isna().sum()

df.Company.value_counts()

plt.figure(figsize=(8, 5))
sns.countplot(x='Company', data=df,
              order=df['Company'].value_counts().index, palette='crest')
plt.xticks(rotation=45, ha='right')
plt.title('Jumlah Produk Berdasarkan Perusahaan', fontsize=10)
plt.xlabel('Company', fontsize=8)
plt.ylabel('Number of Products', fontsize=8)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.show()

plt.figure(figsize=(10,5))
sns.histplot(df['Price_euros'])
plt.show()

brand_price_mean = df.groupby('Company').mean()['Price_euros'].sort_values(ascending=False)
plt.figure(figsize=(10,5))
sns.barplot(x=brand_price_mean.index, y=brand_price_mean.values)
plt.xticks(rotation=90)
plt.show()

processor_price_mean = df.groupby('Cpu').mean()['Price_euros'].sort_values(ascending=False).head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=processor_price_mean.index, y=processor_price_mean.values)
plt.xticks(rotation=90)
plt.show()

processor_price_mean = df.groupby('TypeName').mean()['Price_euros'].sort_values(ascending=False).head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=processor_price_mean.index, y=processor_price_mean.values)
plt.xticks(rotation=90)
plt.show()

processor_price_mean = df.groupby('Gpu').mean()['Price_euros'].sort_values(ascending=False).head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=processor_price_mean.index, y=processor_price_mean.values)
plt.xticks(rotation=90)
plt.show()

processor_price_mean = df.groupby('OpSys').mean()['Price_euros'].sort_values(ascending=False).head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=processor_price_mean.index, y=processor_price_mean.values)
plt.xticks(rotation=90)
plt.show()

"""# **Data Cleaning**"""

df

df["ScreenResolution"] = df.ScreenResolution.str.split(" ").apply(lambda x: x[-1])
df["Screen_Width"] = df.ScreenResolution.str.split("x").apply(lambda x: x[0])
df["Screen_Height"] = df.ScreenResolution.str.split("x").apply(lambda x: x[1])

df = df.drop("ScreenResolution", axis=1)

df["CPU_Brand"] = df.Cpu.str.split(" ").apply(lambda x: x[0])
df["CPU_Frequency_Hz"] = df.Cpu.str.split(" ").apply(lambda x: x[-1])

df["CPU_Frequency_Hz"] = df["CPU_Frequency_Hz"].str[:-3]

df = df.drop(['Cpu'], axis=1)

df["Ram"]=df["Ram"].str.replace("GB","")

df["Weight"]=df["Weight"].str.replace("kg","")

df["Memory_Amount"] = df.Memory.str.split(" ").apply(lambda x: x[0])
df["Memory_Type"] = df.Memory.str.split(" ").apply(lambda x: x[1])

def memory_into_MB(value):
    if "GB" in value:
        return float(value[:value.find("GB")]) * 1024
    elif "TB" in value:
        return float(value[:value.find("TB")]) * 1048576

df["Memory_Amount"] = df["Memory_Amount"].apply(memory_into_MB)

df = df.drop("Memory", axis=1)

df["Gpu_Brand"] = df.Gpu.str.split(" ").apply(lambda x: x[0])

df = df.drop("Gpu", axis=1)

df

df.info()

df["Ram"] = df["Ram"].astype("int")
df["Screen_Width"] = df["Screen_Width"].astype("int")
df["Screen_Height"] = df["Screen_Height"].astype("int")
df["Weight"]=df["Weight"].astype("float64")
df["CPU_Frequency_Hz"]=df["CPU_Frequency_Hz"].astype("float64")

df

"""Menangani Outliers"""

df.describe().T

df_outlier=df.select_dtypes(exclude=['object'])
for column in df_outlier:
        plt.figure()
        sns.boxplot(data=df_outlier, x=column)

"""**Melakukan penghapusan Outlier dengan IQR**"""

Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR=Q3-Q1
df = df[~((df<(Q1-1.5*IQR))|(df>(Q3+1.5*IQR))).any(axis=1)]

df.shape

numerical_columns = df.select_dtypes(include=['int', 'float']).columns
corr_matrix = df[numerical_columns].corr()
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='crest', fmt=".2f", linewidths=.5)
plt.title('Correlation Matrix', fontsize=10)
plt.xticks(rotation=45, fontsize=8)
plt.yticks(fontsize=8)
plt.show()

sns.pairplot(df, diag_kind = 'kde')

df.hist(bins=50, figsize=(20,15))
plt.show()

categorical_features = ['Company','TypeName','OpSys','CPU_Brand','Memory_Type','Gpu_Brand']

feature = categorical_features[0]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
data = pd.DataFrame({'Jumlah sampel':count, 'Persentase':percent.round(1)})
print(data)
count.plot(kind='bar', title=feature);

feature = categorical_features[1]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
data = pd.DataFrame({'Jumlah sampel':count, 'Persentase':percent.round(1)})
print(data)
count.plot(kind='bar', title=feature);

feature = categorical_features[2]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
data = pd.DataFrame({'Jumlah sampel':count, 'Persentase':percent.round(1)})
print(data)
count.plot(kind='bar', title=feature);

feature = categorical_features[3]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
data = pd.DataFrame({'Jumlah sampel':count, 'Persentase':percent.round(1)})
print(data)
count.plot(kind='bar', title=feature);

feature = categorical_features[4]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
data = pd.DataFrame({'Jumlah sampel':count, 'Persentase':percent.round(1)})
print(data)
count.plot(kind='bar', title=feature);

feature = categorical_features[5]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
data = pd.DataFrame({'Jumlah sampel':count, 'Persentase':percent.round(1)})
print(data)
count.plot(kind='bar', title=feature);

cat_features = df.select_dtypes(include='object').columns.to_list()



for col in cat_features:
  sns.catplot(x=col, y="Price_euros", kind="bar", dodge=False, height = 4, aspect = 3,  data=df, palette="Set3")
  plt.title("Rata-rata 'price' Relatif terhadap - {}".format(col))

plt.figure(figsize=(10, 8))
correlation_matrix = df.corr().round(2)


# Untuk menge-print nilai di dalam kotak, gunakan parameter anot=True
sns.heatmap(data=correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, )
plt.title("Correlation Matrix untuk Fitur Numerik ", size=20)

from sklearn.preprocessing import  OneHotEncoder
df = pd.concat([df, pd.get_dummies(df['Company'], prefix='Company')],axis=1)
df = pd.concat([df, pd.get_dummies(df['TypeName'], prefix='TypeName')],axis=1)
df = pd.concat([df, pd.get_dummies(df['OpSys'], prefix='OpSys')],axis=1)
df = pd.concat([df, pd.get_dummies(df['CPU_Brand'], prefix='CPU_Brand')],axis=1)
df = pd.concat([df, pd.get_dummies(df['Memory_Type'], prefix='Memory_Type')],axis=1)
df = pd.concat([df, pd.get_dummies(df['Gpu_Brand'], prefix='Gpu_Brand')],axis=1)

df.drop(['Company','TypeName','OpSys','CPU_Brand','Memory_Type','Gpu_Brand'], axis=1, inplace=True)



sns.pairplot(df[['Inches','Weight']], plot_kws={"s": 3});

from sklearn.decomposition import PCA

pca = PCA(n_components=2, random_state=123)
pca.fit(df[['Inches','Weight']])
princ_comp = pca.transform(df[['Inches','Weight']])

pca.explained_variance_ratio_.round(3)

X = df.drop(['Price_euros'], axis= 1)
y = df["Price_euros"]

from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 123)

print(f'Total # of sample in whole dataset: {len(X)}')
print(f'Total # of sample in train dataset: {len(X_train)}')
print(f'Total # of sample in test dataset: {len(X_test)}')

from sklearn.preprocessing import StandardScaler

numerical_features = ['Inches', 'Weight','Ram','Memory_Amount']
scaler = StandardScaler()
scaler.fit(X_train[numerical_features])
X_train[numerical_features] = scaler.transform(X_train.loc[:, numerical_features])
X_train[numerical_features].head()

X_train[numerical_features].describe().round(4)

# Siapkan dataframe untuk analisis model
models = pd.DataFrame(index=['train_mse', 'test_mse'],
                      columns=['KNN', 'RandomForest', 'Boosting'])

from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

knn = KNeighborsRegressor(n_neighbors=7) # n_neighbors --> Jumlah tetangga terdekat
knn.fit(X_train, y_train)

models.loc['train_mse','knn'] = mean_squared_error(y_pred = knn.predict(X_train), y_true=y_train)

# Impor library yang dibutuhkan
from sklearn.ensemble import RandomForestRegressor

# buat model prediksi
RF = RandomForestRegressor(n_estimators=50, max_depth=16, random_state=55, n_jobs=-1)
RF.fit(X_train, y_train)

models.loc['train_mse','RandomForest'] = mean_squared_error(y_pred=RF.predict(X_train), y_true=y_train)

from sklearn.ensemble import AdaBoostRegressor

boosting = AdaBoostRegressor(learning_rate=0.05, random_state=55)
boosting.fit(X_train, y_train)
models.loc['train_mse','Boosting'] = mean_squared_error(y_pred=boosting.predict(X_train), y_true=y_train)

X_test.loc[:, numerical_features] = scaler.transform(X_test[numerical_features])

mse = pd.DataFrame(columns=['train', 'test'], index=['KNN','RF','Boosting'])

# Buat dictionary untuk setiap algoritma yang digunakan
model_dict = {'KNN': knn, 'RF': RF, 'Boosting': boosting}

# Hitung Mean Squared Error masing-masing algoritma pada data train dan test
for name, model in model_dict.items():
    mse.loc[name, 'train'] = mean_squared_error(y_true=y_train, y_pred=model.predict(X_train))/1e3
    mse.loc[name, 'test'] = mean_squared_error(y_true=y_test, y_pred=model.predict(X_test))/1e3

mse

fig, ax = plt.subplots()
mse.sort_values(by='test', ascending=False).plot(kind='barh', ax=ax, zorder=3)
ax.grid(zorder=0)

prediksi = X_test.iloc[:10].copy()
pred_dict = {'y_true':y_test[:10]}
for name, model in model_dict.items():
    pred_dict['prediksi_'+name] = model.predict(prediksi).round(1)

pd.DataFrame(pred_dict)