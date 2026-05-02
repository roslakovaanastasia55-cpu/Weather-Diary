import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary (Дневник погоды)")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Список для хранения записей
        self.weather_records = []
        
        # Файл для сохранения данных
        self.data_file = "weather_data.json"
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка данных при запуске
        self.load_data()
        
    def create_widgets(self):
        # Главный контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка весов для адаптивности
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Секция ввода данных
        input_frame = ttk.LabelFrame(main_frame, text="Добавление записи", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        
        # Дата
        ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 20), pady=5)
        # Подсказка
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        # Температура
        ttk.Label(input_frame, text="Температура (°C):").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.temp_entry = ttk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Описание погоды
        ttk.Label(input_frame, text="Описание погоды:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.weather_desc_entry = ttk.Entry(input_frame, width=40)
        self.weather_desc_entry.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Осадки
        ttk.Label(input_frame, text="Осадки:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.precip_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Да", variable=self.precip_var).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Кнопка добавления
        add_button = ttk.Button(input_frame, text="Добавить запись", command=self.add_record)
        add_button.grid(row=2, column=2, columnspan=2, pady=10)
        
        # Секция фильтрации
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding="10")
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Фильтр по дате
        ttk.Label(filter_frame, text="По дате:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.filter_date_entry = ttk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        date_filter_btn = ttk.Button(filter_frame, text="Показать", 
                                     command=self.filter_by_date)
        date_filter_btn.grid(row=0, column=2, padx=5, pady=5)


# Фильтр по температуре
        ttk.Label(filter_frame, text="Температура >=").grid(row=0, column=3, sticky=tk.W, pady=5)
        self.filter_temp_entry = ttk.Entry(filter_frame, width=8)
        self.filter_temp_entry.grid(row=0, column=4, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(filter_frame, text="°C").grid(row=0, column=5, sticky=tk.W, pady=5)
        
        temp_filter_btn = ttk.Button(filter_frame, text="Показать", 
                                     command=self.filter_by_temp)
        temp_filter_btn.grid(row=0, column=6, padx=5, pady=5)
        
        # Кнопка сброса фильтров
        reset_filter_btn = ttk.Button(filter_frame, text="Сбросить фильтры", 
                                      command=self.reset_filters)
        reset_filter_btn.grid(row=0, column=7, padx=5, pady=5)
        
        # Таблица для отображения записей
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Создание Treeview с прокруткой
        columns = ('date', 'temperature', 'description', 'precipitation')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Определение заголовков
        self.tree.heading('date', text='Дата')
        self.tree.heading('temperature', text='Температура (°C)')
        self.tree.heading('description', text='Описание погоды')
        self.tree.heading('precipitation', text='Осадки')


# Ширина колонок
        self.tree.column('date', width=120)
        self.tree.column('temperature', width=120)
        self.tree.column('description', width=300)
        self.tree.column('precipitation', width=100)
        
        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Кнопки управления данными
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        save_button = ttk.Button(button_frame, text="Сохранить в файл", command=self.save_data)
        save_button.pack(side=tk.LEFT, padx=5)
        
        load_button = ttk.Button(button_frame, text="Загрузить из файла", command=self.load_data)
        load_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = ttk.Button(button_frame, text="Удалить запись", command=self.delete_record)
        delete_button.pack(side=tk.LEFT, padx=5)
        
    def validate_input(self, date_str, temp_str, desc_str):
        """Проверка корректности ввода"""
        # Проверка даты
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ДД.ММ.ГГГГ")
            return False
        
        # Проверка температуры
        try:
            float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return False


return True
    
    def add_record(self):
        """Добавление новой записи"""
        date_str = self.date_entry.get()
        temp_str = self.temp_entry.get()
        desc_str = self.weather_desc_entry.get()
        precip = "Да" if self.precip_var.get() else "Нет"
        
        if self.validate_input(date_str, temp_str, desc_str):
            # Создание записи
            record = {
                'Дата': date_str,
                'Температура': float(temp_str),
                'Описание': desc_str,
                'Осадки': precip
            }
            
            self.weather_records.append(record)
            self.update_table()
            self.clear_input_fields()
            messagebox.showinfo("Успех", "Запись успешно добавлена!")
    
    def update_table(self, records=None):
        """Обновление таблицы с записями"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Если записи не переданы, используем все записи
        if records is None:
            records = self.weather_records
        
        # Добавление записей в таблицу
        for record in records:
            self.tree.insert('', tk.END, values=(
                record['Дата'],
                record['Температура'],
                record['Описание'],
                record['Осадки']
            ))
    
    def clear_input_fields(self):
        """Очистка полей ввода"""
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.temp_entry.delete(0, tk.END)
        self.weather_desc_entry.delete(0, tk.END)
        self.precip_var.set(False)
    
    def filter_by_date(self):
        """Фильтрация по дате"""
        date_str = self.filter_date_entry.get()
        
        if not date_str:
            messagebox.showwarning("Предупреждение", "Введите дату для фильтрации!")
            return
        
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ДД.ММ.ГГГГ")
            return
        
        filtered_records = [r for r in self.weather_records if r['Дата'] == date_str]
        self.update_table(filtered_records)
        
        if not filtered_records:
            messagebox.showinfo("Результат", f"Записи за {date_str} не найдены")
    
    def filter_by_temp(self):
        """Фильтрация по температуре"""
        temp_str = self.filter_temp_entry.get()
        
        if not temp_str:
            messagebox.showwarning("Предупреждение", "Введите температуру для фильтрации!")
            return
        
        try:
            min_temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return


filtered_records = [r for r in self.weather_records if r['Температура'] >= min_temp]
        self.update_table(filtered_records)
        
        if not filtered_records:
            messagebox.showinfo("Результат", f"Записи с температурой >= {min_temp}°C не найдены")
    
    def reset_filters(self):
        """Сброс фильтров и отображение всех записей"""
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.update_table()
    
    def delete_record(self):
        """Удаление выбранной записи"""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления!")
            return
        
        # Получение значений выбранной записи
        values = self.tree.item(selected_item)['values']
        
        # Поиск и удаление записи из списка
        for record in self.weather_records:
            if (record['Дата'] == values[0] and 
                record['Температура'] == values[1] and
                record['Описание'] == values[2] and
                record['Осадки'] == values[3]):
                self.weather_records.remove(record)
                break
        
        self.update_table()
        messagebox.showinfo("Успех", "Запись удалена!")
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.weather_records, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", f"Данные сохранены в файл {self.data_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.weather_records = json.load(f)
                self.update_table()
                messagebox.showinfo("Успех", f"Данные загружены из файла {self.data_file}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при загрузке: {str(e)}")
        else:


messagebox.showinfo("Информация", "Файл с данными не найден. Создан новый дневник.")

def main():
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()

if __name__ == "__main__":
    main()
