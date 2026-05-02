import tkinter as tk
from tkinter import ttk, messagebox
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
        # Подсказка с текущей датой
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
        errors = []
        # Проверка даты
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            errors.append("Неверный формат даты! Используйте ДД.ММ.ГГГГ")
        
        # Проверка температуры
        try:
            temp = float(temp_str)
            # Дополнительная проверка на реалистичность температуры
            if temp < -90 or temp > 60:
                errors.append("Температура должна быть в диапазоне от -90 до +60°C")
        except ValueError:
            errors.append("Температура должна быть числом!")
        
        # Проверка описания
        if not desc_str or not desc_str.strip():
            errors.append("Описание погоды не может быть пустым!")
        elif len(desc_str.strip()) < 3:
            errors.append("Описание погоды должно содержать минимум 3 символа!")
        
        # Вывод всех ошибок сразу
        if errors:
            messagebox.showerror("Ошибки валидации", "\n".join(errors))
            return False
        
        return True
    
    def add_record(self):
        """Добавление новой записи"""
        date_str = self.date_entry.get().strip()
        temp_str = self.temp_entry.get().strip()
        desc_str = self.weather_desc_entry.get().strip()
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
        
        # Сортировка записей по дате (новые сверху)
        records = sorted(records, key=lambda x: datetime.strptime(x['Дата'], "%d.%m.%Y"), reverse=True)
        
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
        date_str = self.filter_date_entry.get().strip()
        
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
        else:
            messagebox.showinfo("Результат", f"Найдено записей: {len(filtered_records)}")
    
    def filter_by_temp(self):
        """Фильтрация по температуре"""
        temp_str = self.filter_temp_entry.get().strip()
        
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
        else:
            messagebox.showinfo("Результат", f"Найдено записей: {len(filtered_records)}")
    
    def reset_filters(self):
        """Сброс фильтров и отображение всех записей"""
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.update_table()
        messagebox.showinfo("Информация", "Фильтры сброшены. Показаны все записи.")
    
    def delete_record(self):
        """Удаление выбранной записи"""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления!")
            return
        
        # Подтверждение удаления
        if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранную запись?"):
            return
        
        # Получение значений выбранной записи
        values = self.tree.item(selected_item)['values']
        
        # Поиск и удаление записи из списка
        record_to_remove = None
        for record in self.weather_records:
            if (record['Дата'] == values[0] and 
                record['Температура'] == values[1] and
                record['Описание'] == values[2] and
                record['Осадки'] == values[3]):
                record_to_remove = record
                break
        
        if record_to_remove:
            self.weather_records.remove(record_to_remove)
            self.update_table()
            messagebox.showinfo("Успех", "Запись удалена!")
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.weather_records, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", f"Данные сохранены в файл {self.data_file}\nСохранено записей: {len(self.weather_records)}")
        except PermissionError:
            messagebox.showerror("Ошибка", f"Нет прав на запись файла {self.data_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():  # Проверка, что файл не пустой
                        loaded_data = json.loads(content)
                        if isinstance(loaded_data, list):
                            self.weather_records = loaded_data
                            self.update_table()
                            messagebox.showinfo("Успех", f"Данные загружены из файла {self.data_file}\nЗагружено записей: {len(self.weather_records)}")
                        else:
                            raise ValueError("Неверный формат данных в файле")
                    else:
                        self.weather_records = []
                        self.update_table()
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка", f"Файл {self.data_file} поврежден или имеет неверный формат")
                self.weather_records = []
                self.update_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при загрузке: {str(e)}")
                self.weather_records = []
                self.update_table()
        else:
            # Создаем новый файл с примером данных
            self.weather_records = []
            self.create_sample_data()
            self.update_table()
            messagebox.showinfo("Информация", f"Файл с данными не найден. Создан новый дневник с примерами записей.")
    
    def create_sample_data(self):
        """Создание примера данных для нового пользователя"""
        sample_records = [
            {
                'Дата': '25.12.2024',
        'Температура': -5.0,
                'Описание': 'Снежно, ветрено',
                'Осадки': 'Да'
            },
            {
                'Дата': '15.06.2024',
                'Температура': 25.0,
                'Описание': 'Солнечно, ясно',
                'Осадки': 'Нет'
            },
            {
                'Дата': '01.09.2024',
                'Температура': 18.0,
                'Описание': 'Облачно, возможен дождь',
                'Осадки': 'Да'
            }
        ]
        self.weather_records = sample_records
        self.save_data()  # Автоматически сохраняем примеры данных

def main():
    """Главная функция для запуска приложения"""
    try:
        root = tk.Tk()
        app = WeatherDiary(root)
        root.mainloop()
    except Exception as e:
        print(f"Критическая ошибка при запуске приложения: {e}")
        messagebox.showerror("Критическая ошибка", f"Не удалось запустить приложение: {e}")

if __name__ == "__main__":
    main()
