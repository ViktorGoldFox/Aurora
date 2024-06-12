import matplotlib.pyplot as plt
import pandas as pd

def create_temp_metric(data_json):
    print(data_json)
    # data_json = {
    #     'date': ['2024-06-01', '2024-06-02', '2024-06-03', '2024-06-04', '2024-06-05', 
    #              '2024-06-06', '2024-06-07', '2024-06-08', '2024-06-09', '2024-06-10'],
    #     'temperature': [23, 25, 22, 20, 24, 26, 25, 21, 23, 22]
    # }
    # data_json = {
    #     'date': ['2024-06-01', '2024-06-02', '2024-06-03', '2024-06-04', '2024-06-05', 
    #          '2024-06-06', '2024-06-07', '2024-06-08', '2024-06-09', '2024-06-10'],
    #     'temperature': [23, 25, 22, 20, 24, 26, 25, 21, 23, 22]
    # }

    df = pd.DataFrame(data_json)
    # df['date'] = pd.to_datetime(df['date'])

    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['temperature'], marker='o')

    # plt.xlabel('')
    # plt.ylabel('°C)')
    start_date = data_json['date'][0]
    stop_date = data_json['date'][int(len(data_json["date"]) - 1)]
    
    plt.title(f'Температура {start_date} - {stop_date}')
    plt.grid(True)  # Добавление сетки

    # Сохранение графика в файл
    path = "temp_metrics.png"
    plt.savefig("temp_metrics.png")  # Укажите нужное имя и формат файла
    
    return path
