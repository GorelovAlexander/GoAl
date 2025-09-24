#!/usr/bin/env python
# coding: utf-8

#   <div class="alert alert-info">
#   Привет, Александр! Меня зовут Светлана Чих и я буду проверять твой проект. Моя основная цель — не указать на совершенные тобою ошибки, а поделиться своим опытом и помочь тебе. Предлагаю общаться на «ты». Но если это не удобно - дай знать, и мы перейдем на «вы».
# 
#   <div class="alert alert-success">
#   <b>👍 Успех:</b> Зелёным цветом отмечены удачные и элегантные решения, на которые можно опираться в будущих проектах.
#   </div>
#   <div class="alert alert-warning">
#   <b>🤔 Рекомендация:</b> Жёлтым цветом выделено то, что в следующий раз можно сделать по-другому. Ты можешь учесть эти комментарии при выполнении будущих заданий или доработать проект сейчас (однако это не обязательно).
#   </div>
#   <div class="alert alert-danger">
#   <b>😔 Необходимо исправить:</b> Красным цветом выделены комментарии, без исправления которых, я не смогу принять проект :(
#   </div>
#   <div class="alert alert-info">
#   <b>👂 Совет:</b> Какие-то дополнительные материалы
#   </div>
#   Давай работать над проектом в диалоге: если ты что-то меняешь в проекте по моим рекомендациям — пиши об этом.
#   Мне будет легче отследить изменения, если ты выделишь свои комментарии:
#   <div class="alert alert-info"> <b>🎓 Комментарий студента:</b> Например, вот так.</div>
#   Пожалуйста, не перемещай, не изменяй и не удаляй мои комментарии. Всё это поможет выполнить повторную проверку твоего проекта быстрее.
#    </div>

#   <div class="alert alert-info"> <b>🎓 Комментарий студента:</b> Светлана, здравствуй! Большое спасибо за ревью проекта. Буду исправлять все замечания.</div>

# # Итоговый проект: телекоммуникации
# 
# # Описание проекта
# 
# Оператор связи «ТелеДом» хочет бороться с оттоком клиентов. Для этого его сотрудники начнут предлагать промокоды и специальные условия всем, кто планирует отказаться от услуг связи. Чтобы заранее находить таких пользователей, «ТелеДому» нужна модель, которая будет предсказывать, разорвёт ли абонент договор. Команда оператора собрала персональные данные о некоторых клиентах, информацию об их тарифах и услугах.
# 
# Оператор предоставляет два основных типа услуг: 
# 
# - Стационарную телефонную связь. Телефон можно подключить к нескольким линиям одновременно; 
# - Интернет. Подключение может быть двух типов: через телефонную линию (DSL) или оптоволоконный кабель (Fiber optic).
# 
# Дополнительные услуги:
# 
# - Интернет-безопасность: антивирус (DeviceProtection) и блокировка небезопасных сайтов (OnlineSecurity);
# - Выделенная линия технической поддержки (TechSupport);
# - Облачное хранилище файлов для резервного копирования данных (OnlineBackup);
# - Стриминговое телевидение (StreamingTV) и каталог фильмов (StreamingMovies).
# 
# Клиенты могут платить за услуги каждый месяц или заключить договор на 1–2 года. Возможно оплатить счёт разными способами, а также получить электронный чек.
# 
# **Цель проекта** 
# 
# Обучить модель машинного обучения, прогнозирующую возможный отток клиентов.
# 
# **Задачи проекта**
# - загрузить данные
# - подготовить итоговую таблицу, которая будет включать в себя всех клиентов
# - провести исследовательский и корреляционный анализы
# - подготовить и обучить разные модели
# - выбрать лучшую модель
# - провести анализ и интерпретацию важности признаков
# 
# **Целевое ограничение** 
# 
# Значение метрики roc_auc лучшей модели на тестовой выборке должно быть >= 0.85.

# ## Подготовка

# Загружаем необходимые библиотеки.

# In[1]:


get_ipython().system('pip install pandas -q')
get_ipython().system('pip install matplotlib -q')
get_ipython().system('pip install phik -q')
get_ipython().system('pip uninstall scikit-learn -y')
get_ipython().system('pip install scikit-learn==1.3.2')


# In[60]:


import pandas as pd
import warnings
warnings.simplefilter("ignore") 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats as st
import sklearn
import phik
from datetime import (datetime as dt, 
                      date, 
                      time)
from functools import reduce
from phik.report import plot_correlation_matrix

from sklearn.model_selection import (train_test_split, 
                                     GridSearchCV, 
                                     RandomizedSearchCV,
                                     cross_val_score)
from sklearn.preprocessing import (OneHotEncoder, 
                                   OrdinalEncoder, 
                                   StandardScaler, 
                                   MinMaxScaler, 
                                   PolynomialFeatures, 
                                   RobustScaler,
                                   LabelEncoder)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.svm import SVC
from sklearn.metrics import (roc_auc_score, 
                             accuracy_score, 
                             confusion_matrix, 
                             mean_squared_error, 
                             mean_absolute_error, 
                             r2_score,
                             make_scorer,
                             RocCurveDisplay)
from catboost import CatBoostClassifier


# Вводим константы.

# In[3]:


RANDOM_STATE = 80925
TEST_SIZE = 0.25


# <div class="alert alert-success">
# <b>👍 Успех:</b> Импортированы нужные библиотеки, определены константы
# </div>

# ## Загрузка данных

# Создадим датасеты и укажем в них наши данные.

# In[4]:


contract = pd.read_csv('/datasets/contract_new.csv')
personal = pd.read_csv('/datasets/personal_new.csv')
internet = pd.read_csv('/datasets/internet_new.csv')
phone = pd.read_csv('/datasets/phone_new.csv')


# Выведем первые строки и информацию, чтобы проверить содержание наших данных.

# In[5]:


display(contract.head())
print(contract.info())
print()
display(personal.head())
print(personal.info())
print()
display(internet.head())
print(internet.info())
display(phone.head())
print(phone.info())


# **Выводы по загрузке данных**
# 
# - Данные были загружены и проверены на соответствие
# - Некоторые числа и даты записаны типом object (требуется заменить)
# - Булевые переменные обозначены словами (не требует изменений)
# - Отсутствуют пропуски в данных
# - Отсутствует столбец с целевым признаком (требуется создать) 

# <div class="alert alert-success">
# <b>👍 Успех:</b> Данные загружены и просмотрены!
# </div>

# ## Предобработка данных

# Изменим тип данных там, где это необходимо.

# In[6]:


contract['TotalCharges'] = pd.to_numeric(contract['TotalCharges'], errors='coerce')
contract['BeginDate'] = pd.to_datetime(contract['BeginDate'], format='%Y-%m-%d')


# Создадим столбец с целевым признаком, опираясь на данные из столбца EndDate. Для этого посмотрим на уникальные значения столбца.

# In[7]:


print(contract['EndDate'].unique())


# Можно выделить два вида данных: дата завершения договора и **No**, если договор не был завершен. ИСходя из этого мы можем создать столбец с целевым признаком **target**, где 1 означает незавершенный контракт (No), а 0 - завершенный контракт.

# In[8]:


contract['target'] = [1 if i != 'No' else 0 for i in contract['EndDate']]


# Проверим столбец с целевым признаком.

# In[9]:


contract.head(10)


# Чтобы изменить привести тип данных к datetime в столбце EndDate изменим значение No на дату, когда были представлены данные - 1 февраля 2020 года.

# In[10]:


contract.loc[(contract['EndDate'] == 'No'),'EndDate'] = '2020-02-01'


# <div class="alert alert-success">
# <b>👍 Успех:</b> Все верно!
# </div>

# Изменим тип данных в столбце EndDate на datetime.

# In[11]:


contract['EndDate'] = pd.to_datetime(contract['EndDate'],format= "%Y/%m/%d")


# Теперь, когда данные преведены к подходящим типам, проверим датасеты на наличие дубликатов.

# In[12]:


print(contract.duplicated().sum())
print(personal.duplicated().sum())
print(internet.duplicated().sum())
phone.duplicated().sum()


# Выведем информацию по уникальным наименованиям текстовых столбцов во всех датафреймах чтобы проверить названия на опечатки.

# In[13]:


unique_values = contract['Type'].unique()
print(unique_values)
unique_values = contract['PaymentMethod'].unique()
print(unique_values)
unique_values = personal['gender'].unique()
print(unique_values)
unique_values = internet['InternetService'].unique()
print(unique_values)


# Опечаток не обнаружено. Вывдеме всю информацию о датасетах ещё раз, чтобы проверить изменения.

# In[14]:


display(contract.head())
print(contract.info())
print()
display(personal.head())
print(personal.info())
print()
display(internet.head())
print(internet.info())
display(phone.head())
print(phone.info())


# **Выводы по предобработке данных**
# 
# - Числа и даты были переведены в нужный тип данных
# - Создан столбец с целевым признаком
# - Дубликаты не обнаружены
# - Опечатки не обнаружены

# ## Исследовательский анализ данных

# Для исследовательского анализа данных обьединим все датафреймы по столбцу **customerID** для более удобной дальнейшней работы.

# In[15]:


names = [contract, internet, personal, phone]
data = reduce(lambda left,right: pd.merge(left, right, on=['customerID']), names)


# <div class="alert alert-danger">
# <s><b>😔 Необходимо исправить:</b> Использование 'outer' здесь излишне, в нашем случае итог не поменяется, но с другими данными можно получить искуственно созданные пропуски и придется дополнительно обрабатывать данные</s>
# </div>

#   <div class="alert alert-info"> <b>🎓 Комментарий студента:</b> Принял! Убрал outer.</div>

# <div class="alert alert-success">
# <b>👍 Успех:</b> Все верно!
# </div>

# In[16]:


display(data.head())
print()
data.info()


# После объединения появились пропуски в данных.

# In[17]:


data.isna().sum()


# Мы видим несколько столбцов с одинаковым количеством пропусков. Разберемся с ними поотдельности. 
# 
# Столбцы со значением пропусков 1526 - это пользователи, о которых не было никакой информации в датафрейме **Internet**. Скорее всего они просто не подключили данную услугу. 
# 
# Пропуски в столбце **MyltiplieLines** говорят что пользователь не пользовался услугами телефона. 
# 
# Заменим эти пропуски на фразы **no_internet** и **no_phone**.

# In[18]:


data['MultipleLines'].fillna('no_phone', inplace = True)

internet_columns = ['InternetService', 'OnlineSecurity', 'OnlineBackup', 
                   'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']

for column in internet_columns:
    data[column].fillna('no_internet', inplace=True)


# <div class="alert alert-success">
# <b>👍 Успех:</b> Все верно!
# </div>

# In[19]:


data.isna().sum()


# Отдельно рассмотрим пропуски в столбце **TotalCharges**.

# In[20]:


data[data['TotalCharges'].isna()]


# Даты в столбцах **BeginDate** и **EndDate** совпадают. Из этого можно сделать вывод, что данные абоненты еще не успели оплатить услуги, так как заключили договор в день сбора данных. Заполним пропуски ежемесячным платежом **MonthlyCharges**.

# <div class="alert alert-success">
# <b>👍 Успех:</b> Все верно! Это новые абоненты!
# </div>

# In[21]:


data['TotalCharges'].fillna(data[data['TotalCharges'].isnull()]['MonthlyCharges'], inplace = True)


# Создадим новый столбец **period** с количеством дней, которые пользователи пользуются подпиской.

# In[22]:


data['period']=(data['EndDate']-data['BeginDate'])/np.timedelta64(1,'D')


# Проверим все изменения.

# In[23]:


data.info()


# <div class="alert alert-success">
# <b>👍 Успех:</b> Отлично, с пропусками разобрались!
# </div>

# После того, как все пропуски были заполнены, можно приступить к визуализации данных.
# 
# Создадим гистограммы для численных данных и круговые диаграммы для категориальных.

# In[24]:


print('Гистаграммы для всех числовых переменных:\n')

# Найдем числовые столбцы в датафрейме
numerical_columns = ['MonthlyCharges', 'TotalCharges','period']

# Зададим размер фигуры для удобства визуализации
plt.figure(figsize=(12, 8))

# Цикл для итерации по каждому числовому столбцу
for i, column in enumerate(numerical_columns):
    # Создаем subplot для текущего столбца
    plt.subplot(2, 3, i + 1)  # 2 строки, 3 столбца, текущий график
    
    # Строим гистограмму для текущего столбца
    data[column].hist(bins=50)
    
    # Добавляем заголовок с названием столбца
    plt.title(column)
    
    # Добавляем метки для осей
    plt.xlabel(column)
    plt.ylabel('Частота')

# Отображаем все гистограммы
plt.tight_layout()
plt.show()


# In[25]:


print('Круговые диаграммы для всех категориальных переменных:\n')

# Список столбцов, для которых нужно вывести круговые диаграммы
categorical_columns = [col for col in data.columns if col not in numerical_columns and col != 'BeginDate' and col != 'customerID' and col != 'EndDate']

# Зададим размер фигуры для удобства визуализации
plt.figure(figsize=(10, 10))

# Цикл для итерации по каждому столбцу
for i, column in enumerate(categorical_columns):
    # Создаем subplot для текущего столбца
    plt.subplot(6, 3, i + 1)  # 3 строки, 2 столбца, текущий график
    
    # Подсчитываем количество каждого уникального значения в текущем столбце
    column_data = data[column].value_counts()
    
    # Строим круговую диаграмму для текущего столбца
    plt.pie(column_data, labels=column_data.index, autopct='%1.1f%%')
    
    # Добавляем заголовок с названием столбца
    plt.title(column)

# Отображаем все круговые диаграммы
plt.tight_layout()
plt.show()


# **Выводы по исследовательскому анализу данных**
# 
# - В данных выбросов не обнаружено.
# - Месячные оплаты распределены таким образом, что основная часть пользователей платят 20 долларов, видимо, это цена минимальной подписки.
# - Дальше помесячная оплата распределена более равномерно с пиками сумм 50, 60, 70, 80, 90, 100 и 110 долларов.
# - В гистограмме **period** мы видим, что новых пользователей, которые пользуются подпиской первый год, больше. Однако есть и достаточно большое количесво пользователей, которые пользуются подпиской более 5 с половиной лет.
# - Чуть больше половины пользователей предпочитаю **помесячную оплату** подписки.
# - У 21% пользователей не подключена дополнительная услуга интернета.
# - Количество пользователей мужчин и женщин практически одинаковое. 
# - 16% пользователей - это жители пенсионного возраста.
# - **15% процентов пользователей не продлили подписку**.

# <div class="alert alert-success">
# <b>👍 Успех:</b> Все верно!
# </div>

# ## Корреляционный анализ данных

# Проведем корреляционный анализ всех признаков в датасете и отберем те, которые влияют на целевую переменную.
# 
# Сначала сделаем копию данных и уберем столбец **customerID**, **EndDate** (так как на основе этого столбца формировали target) и **BeginDate** (так как на основе этого столбца формировали period).

# In[26]:


data_corr = data.copy()
data_corr = data_corr.drop(columns=['customerID', 'EndDate', 'BeginDate'])


# Построим матрицу корреляции phik.

# In[27]:


phik_overview = data_corr.phik_matrix()
phik_overview.round(2)


# In[28]:


interval_cols = ['MonthlyCharges', 'TotalCharges', 'period']

phik_overview = data_corr.phik_matrix(interval_cols = interval_cols)


# In[29]:


plot_correlation_matrix(phik_overview.values, 
                       x_labels = phik_overview.columns,
                       y_labels = phik_overview.index,
                       vmin = 0,
                       vmax = 1,
                       title = r'Корреляция по $\phi_k$',
                       color_map= "Greens",
                       fontsize_factor = 1.5,
                       figsize = (20, 12))
plt.show();


# Мы более отчетливо видим, какие признаки влияют на целевую переменную. Однако очень много признаков, которые имеют слабую корреляцию с **target**.
# 
# В датафрейм для обучения модели отберем только те, в которых корреляция больше 0.1.

# In[30]:


data1 = data_corr.drop(columns=['Dependents','SeniorCitizen','gender', 'StreamingMovies', 'StreamingTV','TechSupport', 'DeviceProtection', 'OnlineBackup', 'OnlineSecurity', 'InternetService', 'PaperlessBilling', 'Type'])


# In[31]:


data1.head()


# In[32]:


phik_overview = data1.phik_matrix(interval_cols = interval_cols)
plot_correlation_matrix(phik_overview.values, 
                       x_labels = phik_overview.columns,
                       y_labels = phik_overview.index,
                       vmin = 0,
                       vmax = 1,
                       title = r'Корреляция по $\phi_k$',
                       color_map= "Greens",
                       fontsize_factor = 1.5,
                       figsize = (20, 12))
plt.show();


# Мы удалили те признаки, которые оказывали меньше всего влияния и оставили более значимые, учитывая корреляцию с целевым признаком. Наибольшие значения показывают:
# - сроки использования подписки - **period**.
# - сколько клиент потратил на подписку - **TotalCharges**.
# 
# Чем дольше клиент пользуется подпиской и чем больше он заплатил за всё время, тем меньше вероятность, что клиент откажется от продления подписки.

# <div class="alert alert-success">
# <b>👍 Успех:</b> Признаки отобраны!
# </div>

# ## Подготовка и обучение модели

# Выделим из датасета data1 целевой признак.

# In[33]:


X = data1.drop('target', axis = 1)
y = data1['target']


# Выведем размеры датасетов.

# In[34]:


X.shape, y.shape


# Сформируем обучающую и тестовые выборки.

# In[35]:


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size = TEST_SIZE,
    random_state = RANDOM_STATE,
    stratify = y)


# Проверим распределение классов.

# In[36]:


print('Расспределение в тренировочной выборке:', y_train.value_counts(normalize = True))
print()
print('Расспределение в тестовой выборке:', y_test.value_counts(normalize = True))


# Создадим списки для кодирования.

# In[37]:


num_columns = X_train.select_dtypes(include=['float64','int64']).columns.tolist()
num_columns


# In[38]:


cat_columns = X_train.select_dtypes(include=['object']).columns.tolist()
for column in cat_columns:
        unique_values = X_train[column].unique()
        print(f"Уникальные значения для столбца '{column}': {unique_values}")


# In[39]:


# признаки для OneHotEncoder
ohe_columns = ['PaymentMethod', 'Partner', 'MultipleLines']

# численные признаки
num_columns = ['MonthlyCharges', 'TotalCharges', 'period']


# Создадим пайплайн для подготовки признаков из списка ohe_columns.

# In[40]:


ohe_pipe = Pipeline([
        (
            'simpleImputer_ohe', 
            SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        ),
        (    'ohe', 
            OneHotEncoder(sparse_output=False, handle_unknown='error',drop='first')
        )
])


# Создадим общий пайплайн для подготовки данных.

# In[41]:


data_preprocessor = ColumnTransformer(
    [
        ('ohe', ohe_pipe, ohe_columns),
        ('num', MinMaxScaler(), num_columns)   
    ], 
    remainder =  'passthrough'
)
print(data_preprocessor)


# Создадим итоговый пайплайн.

# In[42]:


pipe_final= Pipeline(
    [
        ('preprocessor', data_preprocessor),
        ('models', DecisionTreeRegressor(random_state=RANDOM_STATE))
    ]
)


# Визуализируем его.

# In[43]:


pipe_final


# Создадим словари для разных моделей: DecisionTreeClassifier, SVC, LogisticRegression.

# In[44]:


param_distributions = [
    # словарь для модели DecisionTreeClassifier()
    {
        'models': [DecisionTreeClassifier(random_state=RANDOM_STATE)],
        'models__max_depth': range(2, 7),
        'models__max_features': range(2, 20),
        'preprocessor__num': [StandardScaler(), MinMaxScaler(), 'passthrough'],
        'models__min_samples_split': range(2,20) ,
        'models__min_samples_leaf': range(2,20) ,
    },
    # словарь для модели SVC()
    {
        'models': [SVC(random_state=RANDOM_STATE, probability = True)],
        'models__kernel':('rbf','linear','poly'),
        'models__C': range(1,100),
        'models__degree': range(1,10),
        'preprocessor__num': [StandardScaler(), MinMaxScaler(), 'passthrough']  

    },
    # словарь для модели LogisticRegression()
    {
        'models': [LogisticRegression(random_state=RANDOM_STATE)],
        'models__solver': ('liblinear', 'saga', 'lbfgs'),
        'models__penalty': ('l1', 'l2', 'elasticnet', 'none'),
        'models__C': range(1,100),
        
        'preprocessor__num': [StandardScaler(), MinMaxScaler(), 'passthrough']  
    }

] 


# In[45]:


randomized_search = RandomizedSearchCV(
    pipe_final, 
    param_distributions, 
    cv=5,
    scoring='roc_auc',
    random_state=RANDOM_STATE,
    n_jobs=-1
    
)


# In[46]:


le = LabelEncoder()
y_train = le.fit_transform(y_train)
y_train


# Обучим модель на тренировочной выборке.

# In[47]:


randomized_search.fit(X_train, y_train)


# In[48]:


print('Лучшая модель и её параметры:\n\n', randomized_search.best_estimator_)
print ('Метрика ROC_AUC лучшей модели на тренировочной выборке:', randomized_search.best_score_)


# Мы получили результат. Лучшая модель - **DecisionTreeClassifier** с гиперпараметрами **(max_depth=4, max_features=16, min_samples_leaf=4, min_samples_split=8, random_state=80925)**. Её показатели метрики **roc_auc - 0.75**, что достаточно мало и не удовлетворяет поставленной цели.
# 
# Напишем еще один пайплайн по подбору гиперпараметров для модели CatBoostClassifier.

# In[51]:


pipeline_CB = Pipeline([('scaler', data_preprocessor),('model', CatBoostClassifier(iterations=100, learning_rate=0.1))])

param_grid = [
                {
                'model': [CatBoostClassifier(random_state=RANDOM_STATE, verbose=0)],
                'model__learning_rate': [0.01, 0.03],
                'model__depth': range(2, 8, 1)
                }]

CB_CV = GridSearchCV(pipeline_CB,
                    param_grid,
                    cv = 5,
                    scoring='roc_auc',
                    n_jobs=-1,
                    verbose=1)

CB_CV.fit(X_train, y_train)


# In[52]:


print('Лучшая модель и её параметры:\n\n', CB_CV.best_estimator_)
print ('Метрика ROC_AUC лучшей модели на тренировочной выборке:', CB_CV.best_score_)


# Здесь лучше всех себя показала модель **CatBoostClassifier**. Её метрика **roc_auc - 0.85**. 
# 
# Будем использовать данную модель для финального предсказания на тестовой выборке.

# <div class="alert alert-success">
# <b>👍 Успех:</b> Лучшая модель выбрана!
# </div>

# In[53]:


y_test_probas = CB_CV.predict_proba(X_test)[:,1]
y_test_probas


# In[54]:


print(y_test.shape)
y_test_probas.shape


# Выведем лучшие параметры для полученной модели.

# In[55]:


CB_CV.best_params_


# In[56]:


print(f'Метрика ROC-AUC на тестовой выборке: {roc_auc_score(y_test, y_test_probas)}')


# Мы получили значение метрики **roc_auc 0.91** (наша цель >= 0.85). Данная модель с задачей справляется.
# 
# 
# Выведем матрицу ошибок для полученных предсказаний, чтобы проверить наличие ошибок 1 и 2 рода.

# In[57]:


y_test_pred = CB_CV.predict(X_test)
cm = confusion_matrix(y_test, y_test_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues_r')
plt.ylabel('True label')
plt.xlabel('Predicted'); 


# - У полученной модель довольно высокая точность (Accuracy), что означает, что она хорошо предсказывает в общем случае. 
# - Однако показатель Recall для класса 1 довольно низкая, что указывает на то, что модель пропускает много объектов класса 1 и предсказывает их как класс 0. Это не очень хорошо с точки зрения бизнеса, но в целом показатели довольно точные в большинстве случаев.
# 
# Количество правильных ответов модели значительно преобладает над ошибочными: 1478 True Negative, 156 True Positive.

# <div class="alert alert-success">
# <b>👍 Успех:</b> Все верно!
# </div>

# In[61]:


fig, ax = plt.subplots(figsize=(10, 6))

RocCurveDisplay.from_estimator(
    CB_CV,           
    X_test,          
    y_test,          
    ax=ax,
    name='CatBoost'  
)

ax.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Random classifier')

ax.set_title('ROC-кривая', fontsize=16)
ax.set_xlabel('False Positive Rate', fontsize=12)
ax.set_ylabel('True Positive Rate', fontsize=12)
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)

plt.show()


# Визуализируем, какие признаки больше всего повлияли на предсказание.

# In[ ]:


X_train.columns


# In[ ]:


best_model = CB_CV.best_estimator_
model = best_model.named_steps['model']

# Получение важности признаков и их имен
feature_importances = model.get_feature_importance()

# Извлекаем шаги пайплайна с названиями признаков
data_preprocessor = best_model.named_steps['scaler']

# Получаем имена признаков после всех преобразований
transformed_feature_names = data_preprocessor.get_feature_names_out()

# Создание датафрейма для удобного отображения
feature_importance_df = pd.DataFrame({
    'Признак': transformed_feature_names,
    'Важность': feature_importances
})

# Сортировка по важности признаков
feature_importance_df = feature_importance_df.sort_values(by='Важность', ascending=False)

# Построение графика
plt.figure(figsize=(12, 8))
sns.barplot(x='Важность', y='Признак', data=feature_importance_df)
plt.title('Важность признаков для модели CatBoostClassifier')
plt.show()


# <div class="alert alert-danger">
#     <s><b>😔 Необходимо исправить:</b> Зачем здесь еще раз импортируется pandas?</s>
# </div>

#   <div class="alert alert-info"> <b>🎓 Комментарий студента:</b> Исправлено.</div>

# <div class="alert alert-success">
# <b>👍 Успех:</b> Все верно!
# </div>

# На графике можно наглядно увидеть, что самые важные признаки которые повлияли на предсказание результата это:
# 
# - period - время, которое прошло с даты заключения договора
# - TotalCharges - общие расходы абонента за все время
# - MonthlyCharges - размер ежемесячного платежа абонента
# - Partner - наличие супруга(и) у абонента
# 
# Эти признаки заметно самые весомые и важные из всех остальных. Веса остальных признаков находятся примерно на одном уровне. 

# <div class="alert alert-danger">
#     <s><b>😔 Необходимо исправить:</b> Нужно еще визуализировать ROC-кривую</s>
# </div>

#   <div class="alert alert-info"> <b>🎓 Комментарий студента:</b> Добавил визуализацию roc-кривой.</div>

# ## Итоговый вывод

# **Выводы по загрузке данных**
# 
# - Данные были загружены и проверены на соответствие
# - Некоторые числа и даты записаны типом object (требуется заменить)
# - Булевые переменные обозначены словами (не требует изменений)
# - Отсутствуют пропуски в данных
# - Отсутствует столбец с целевым признаком (требуется создать) 
# 
# **Выводы по предобработке данных**
# 
# - Числа и даты были переведены в нужный тип данных
# - Создан столбец с целевым признаком
# - Дубликаты не обнаружены
# - Опечатки не обнаружены
# 
# **Выводы по исследовательскому анализу данных**
# 
# - В данных выбросов не обнаружено.
# - Месячные оплаты распределены таким образом, что основная часть пользователей платят 20 долларов, видимо, это цена минимальной подписки.
# - Дальше помесячная оплата распределена более равномерно с пиками сумм 50, 60, 70, 80, 90, 100 и 110 долларов.
# - В гистограмме **period** мы видим, что новых пользователей, которые пользуются подпиской первый год, больше. Однако есть и достаточно большое количесво пользователей, которые пользуются подпиской более 5 с половиной лет.
# - Чуть больше половины пользователей предпочитаю **помесячную оплату** подписки.
# - У 21% пользователей не подключена дополнительная услуга интернета.
# - Количество пользователей мужчин и женщин практически одинаковое. 
# - 16% пользователей - это жители пенсионного возраста.
# - **15% процентов пользователей не продлили подписку**.
# 
# Наибольшие корреляционные значения показывают:
# - сроки использования подписки - **period**.
# - сколько клиент потратил на подписку - **TotalCharges**.
# 
# Чем дольше клиент пользуется подпиской и чем больше он заплатил за всё время, тем меньше вероятность, что клиент откажется от продления подписки.
# 
# **Подготовка и обучение модели**
# 
# В ходе подготовки и обучения использовались модели: DecisionTreeClassifier, SVC, LogisticRegression, CatBoostClassifier.
# 
# Лучше всех себя показала модель **CatBoostClassifier** с гиперпараметрами **('model__depth': 5, 'model__learning_rate': 0.03)**. Её метрика **roc_auc** на тренировочной выборке составила **0.85**. А на тестовой - **0.91**.
# - У полученной модель довольно высокая точность (Accuracy), что означает, что она хорошо предсказывает в общем случае. 
# - Однако показатель Recall для класса 1 довольно низкая, что указывает на то, что модель пропускает много объектов класса 1 и предсказывает их как класс 0. Это не очень хорошо с точки зрения бизнеса, но в целом показатели довольно точные в большинстве случаев.
# 
# Количество правильных ответов модели значительно преобладает над ошибочными: 1478 True Negative, 156 True Positive.
# 
# Самые важные признаки которые повлияли на предсказание результата это:
# 
# - period - время, которое прошло с даты заключения договора
# - TotalCharges - общие расходы абонента за все время
# - MonthlyCharges - размер ежемесячного платежа абонента
# - Partner - наличие супруга(и) у абонента
# 
# **Рекомендации для бизнеса**
# 
# На основе проведенного анализа данных и построенной модели прогнозирования оттока клиентов, можно порекомендовать следующее:
# 
# *Фокус на лояльность долгосрочных клиентов*
# 
# - Разработать программу лояльности для клиентов со стажем более 5 лет
# - Предложить эксклюзивные условия и бонусы для данной категории
# 
# *Удержания новых клиентов*
# 
# - Усилить поддержку клиентов в первый год использования услуги
# 
# *Улучшение сервиса для семейных клиентов*
# 
# - Разработать семейные пакеты и акции, так как наличие партнера является важным фактором лояльности

# <div class="alert alert-warning">
# <b>🤔 Рекомендация:</b> Нужно исправить несколько моментов, в целом отличный проект!
# </div>

#   <div class="alert alert-info"> <b>🎓 Комментарий студента:</b> Светлана, ещё раз спасибо за ревью моего проекта. Постарался исправить все замечания.</div>

# <div class="alert alert-success">
# <b>👍 Успех:</b> Молодец, финальный проект завершен! Сама работа получилась хорошей и структурированной, были предобработаны и проанализированы данные, выбран целевой признак, рассчеты подкреплены визуализацией, это очень важная часть работы, которая облегчает анализ и позволяет полнее представлять происходящее в данных. Построено и обучено несколько моделей, все они оценены и выбрана лучшая. Цель работы достигнута, получена модель хорошо предсказывающая уход клиентов. Не забывай о том, что все пункты очень важны и каждому стоит уделять максимум внимания. <p>
# С опытом становится значительно легче, но опыт это не только повторение однажды изученного, но и постоянное развитие, тем более, что ты выбрал очень динамично развивающуюся область. <p>
# В будущей профессии тебе точно пригодиться умение системно подходить к решению аналитических задач, здесь рекомендую изучить ТРИЗ и системный анализ, из литературы можно почитать Теоретический минимум по Big Data — Су Кеннет и Ын Анналин, Практическая статистика для специалистов Data Science — Брюс П. и Брюс Э., Real-World Machine Learning — Henric Brink, Joseph Мark, W. Richards Fetherolf, Прикладное машинное обучение с помощью Scikit-Learn и TensorFlow — Жерон Орельен.<p>
# Есть интересные сообщества (например https://vk.com/mashinnoe_obuchenie_ai_big_data) и конечно же https://habr.com/ru/all/<p>
# 
# Дополнительно предлагаю посмотреть:
# - Книга от ШАД: https://academy.yandex.ru/handbook/ml
# 
# - Открытый курс машинного обучения: https://habr.com/ru/company/ods/blog/322626/
# 
#  Удачи тебе и профессионального роста!
# </div>

# In[ ]:




