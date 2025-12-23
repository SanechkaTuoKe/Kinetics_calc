def calculate_kinetics():
    print("Пересчетка концентраций для кинетики (by Саша)")
    print("\n1 - фурациллин MgO")
    print("2 - хлоргексидин MgO (в процессе)")

    # Выбор вещества
    while True:
        try:
            choice = int(input("\nВыберите вещество (1 или 2): "))
            if choice == 1:
                substance_name = "фурациллин & MgO"
                break
            elif choice == 2:
                print("пока в процессе")
                print("выберите фурациллин")
                continue
            else:
                print("введите 1 или 2")
        except ValueError:
            print("Введите 1 или 2")

    print(f"\nВыбрано: {substance_name}")

    # Выбор концентрации
    concentrations = [20, 15, 10, 5, 2.5, 1, 0.5, 0.1, 0.01]
    print(f"\nконцентрации раствора: {concentrations}")

    while True:
        try:
            conc = float(input("Введите концентрацию раствора: "))
            if conc in concentrations:
                break
            else:
                print("введите значение из списка")
        except ValueError:
            print("введите значение из списка")

    times_options = [1, 2.5, 5, 7.5, 10, 15, 20]

    all_tables = {}

    time_points = [15, 30, 45, 60, 90, 120, 180]

    print(f"\n{'=' * 80}")
    print(f"НАЧАЛО РАСЧЕТОВ ДЛЯ: {substance_name}")
    print(f"Концентрация раствора: {conc} мг/мл")
    print(f"{'=' * 80}")

    while True:
        print(f"\nДоступное время: {times_options}")
        print("Введите '0' для завершения ввода")

        # Выбор времени
        while True:
            try:
                time_input = input("Выберите время для расчета: ")
                if time_input == '0':
                    break

                selected_time = float(time_input)
                if selected_time in times_options:
                    if selected_time in all_tables:
                        print(f"Для времени {selected_time} мин уже есть таблица. Хотите перезаписать? (да/нет)")
                        rewrite = input().lower()
                        if rewrite not in ['да', 'yes', 'y', 'д']:
                            continue
                    break
                else:
                    print("Пожалуйста, введите значение из списка или '0' для завершения")
            except ValueError:
                print("Введите число или '0' для завершения")

        if time_input == '0':
            break

        print(f"\nВыбрано время: {selected_time} мин")

        # Ввод оптической плотности
        print(f"\nВведите значения оптической плотности для времени {selected_time} мин:")
        print("Пример: 0.00224 0.00247 0.00305 0.00249 0.00368 0.00342 0.00531")
        print("Или вводите по одному числу на строку")

        a_values = []
        
        while len(a_values) < 7:
            try:
                input_line = input(f"Значение {len(a_values)+1} или все 7 через пробел: ").strip()
                
                if not input_line:
                    print("Пустой ввод. Попробуйте еще раз:")
                    continue
                
                # Пробуем разбить по пробелам
                numbers = input_line.split()
                
                if len(numbers) == 7 and len(a_values) == 0:
                    # Введена строка с 7 числами
                    a_values = [float(x.replace(',', '.')) for x in numbers]
                    print(f"✓ Принято 7 значений из строки")
                    break
                elif len(numbers) == 1:
                    # Введено одно число
                    a_values.append(float(numbers[0].replace(',', '.')))
                    print(f"✓ Принято значение {len(a_values)}: {a_values[-1]:.6f}")
                    
                    if len(a_values) == 7:
                        print(f"✓ Принято все 7 значений")
                        break
                else:
                    print(f"Ошибка: нужно ввести либо 1 число, либо 7 чисел через пробел")
                    
            except ValueError:
                print("Ошибка: введите число")

        print(f"\nВведенные значения оптической плотности:")
        for i in range(7):
            print(f"  Время {time_points[i]} сек: {a_values[i]:.6f}")

        c_values = []  # C - концентрация в мг/мл
        c_6ml_values = []  # C в 6мл в k-ый момент времени = C * 6
        sum_values = []  # Сумма концентраций к k-му моменту времени
        percent_values = []  # Процент: (C в 6мл / Сумма) × 100%

        for i, a in enumerate(a_values):
            # Расчет C по формуле: C = (A + 0.00608) / 27905.64
            c = (a + 0.00608) / 27905.64
            c_values.append(c)

            # Расчет C в 6мл = C * 6
            c_6ml = c * 6
            c_6ml_values.append(c_6ml)

            # Расчет суммы
            if i == 0:
                sum_val = c_6ml
            else:
                sum_val = sum_values[-1] + c_6ml
            sum_values.append(sum_val)
            
            # Расчет процента: (C в 6мл / Сумма) × 100%
            percent = (c_6ml / sum_val) * 100 if sum_val > 0 else 0
            percent_values.append(percent)

        all_tables[selected_time] = {
            'a_values': a_values,
            'c_values': c_values,
            'c_6ml_values': c_6ml_values,
            'sum_values': sum_values,
            'percent_values': percent_values,
            'total_released': sum_values[-1]  # Итоговое значение за 180 сек
        }

        print(f"\n{'=' * 100}")
        print(f"ТАБЛИЦА для времени {selected_time} мин")
        print(f"{'=' * 100}")
        print(f"{'Время, с':<10} {'Опт. плотность':<15} {'C, мг/мл':<20} "
              f"{'C в 6мл, мг':<20} {'Сумма C, мг':<20} {'Процент':<10}")
        print(f"{'-' * 95}")

        for i in range(len(time_points)):
            print(f"{time_points[i]:<10} "
                  f"{a_values[i]:<15.6f} "
                  f"{c_values[i]:<20.16f} "
                  f"{c_6ml_values[i]:<20.16f} "
                  f"{sum_values[i]:<20.16f} "
                  f"{percent_values[i]:<10.2f}%")

        print(f"{'=' * 100}")

        print("\nДобавить данные для другого времени")
        continue_input = input("Введите 'да' для продолжения или 'нет' для завершения: ").lower()
        if continue_input not in ['да', 'yes', 'y', 'д']:
            break

    # Вывод всех таблиц
    if all_tables:
        print(f"\n{'=' * 80}")
        print("СВОДНАЯ ИНФОРМАЦИЯ ПО ВСЕМ ТАБЛИЦАМ")
        print(f"{'=' * 80}")

        # Вывести список созданных таблиц
        print(f"\nСоздано таблиц: {len(all_tables)}")
        print(f"Времена: {sorted(list(all_tables.keys()))}")

        # Вывод в формате для Excel
        print(f"\n{'=' * 80}")
        print("ДАННЫЕ ДЛЯ КОПИРОВАНИЯ В EXCEL:")
        print(f"{'=' * 80}")

        for selected_time in sorted(all_tables.keys()):
            print(f"\n--- Время {selected_time} мин ---")
            data = all_tables[selected_time]
            print("Время\tОпт. плотность\tC, мг/мл\tC в 6мл, мг\tСумма C, мг\tПроцент")
            for i in range(len(time_points)):
                print(f"{time_points[i]}\t{data['a_values'][i]:.6f}\t{data['c_values'][i]:.16f}\t"
                      f"{data['c_6ml_values'][i]:.16f}\t{data['sum_values'][i]:.16f}\t{data['percent_values'][i]:.2f}%")

        # ТАБЛИЦА ДЛЯ ГРАФИКА ВЫСВОБОЖДЕНИЯ
        print(f"\n{'=' * 80}")
        print("ТАБЛИЦА ДЛЯ ПОСТРОЕНИЯ ГРАФИКА ВЫСВОБОЖДЕНИЯ")
        print(f"{'=' * 80}")
        print("Сумма C (мг) для разных времен высвобождения:")
        print(f"{'-' * 80}")
        
        # Заголовок таблицы
        header = "Время (с)"
        for time_val in sorted(all_tables.keys()):
            header += f"\t{time_val} мин (мг)"
        print(header)
        
        # Данные для каждого времени (15, 30, 45, ... 180)
        for i in range(len(time_points)):
            row = f"{time_points[i]}"
            for time_val in sorted(all_tables.keys()):
                data = all_tables[time_val]
                row += f"\t{data['sum_values'][i]:.16f}"
            print(row)

        # Дополнительная информация
        print(f"\n{'=' * 80}")
        print("ИНФОРМАЦИЯ О РАСЧЕТЕ:")
        print(f"{'=' * 80}")
        print(f"1. Использованная формула: C = (A + 0.00608) / 27905.64")
        print(f"2. Где A - оптическая плотность")
        print(f"3. C в 6мл = C × 6")
        print(f"4. Сумма - накопленная сумма C в 6мл")
        print(f"5. Процент = (C в 6мл / Сумма) × 100% - показывает долю текущего шага в общей сумме на данный момент")

        # Итоговые результаты
        print(f"\n{'=' * 80}")
        print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ НА 180 СЕКУНДЕ:")
        print(f"{'=' * 80}")
        print("Время высвобождения\tСумма C (мг)\tПроцент последнего шага")
        for selected_time in sorted(all_tables.keys()):
            total_released = all_tables[selected_time]['total_released']
            last_percent = all_tables[selected_time]['percent_values'][-1]
            print(f"{selected_time} мин\t\t{total_released:.16f}\t{last_percent:.2f}%")

        # Предложение сохранить результаты
        save = input("\nСохранить все результаты в файл? (да/нет): ").lower()
        if save in ['да', 'yes', 'y', 'д']:
            from datetime import datetime
            filename = f"результаты_фурациллин_{conc}мг_все_времена.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Пересчетка концентраций для кинетики (by Саша)\n")
                f.write(f"Вещество: {substance_name}\n")
                f.write(f"Концентрация раствора: {conc} мг/мл\n")
                f.write(f"Количество таблиц: {len(all_tables)}\n")
                f.write(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
                f.write(f"{'=' * 80}\n\n")

                for selected_time in sorted(all_tables.keys()):
                    data = all_tables[selected_time]
                    f.write(f"ТАБЛИЦА для времени высвобождения {selected_time} мин\n")
                    f.write(f"{'=' * 100}\n")
                    f.write(f"{'Время, с':<10} {'Опт. плотность':<15} {'C, мг/мл':<20} "
                            f"{'C в 6мл, мг':<20} {'Сумма C, мг':<20} {'Процент':<10}\n")
                    f.write(f"{'-' * 95}\n")

                    for i in range(len(time_points)):
                        f.write(f"{time_points[i]:<10} {data['a_values'][i]:<15.6f} "
                                f"{data['c_values'][i]:<20.16f} "
                                f"{data['c_6ml_values'][i]:<20.16f} "
                                f"{data['sum_values'][i]:<20.16f} "
                                f"{data['percent_values'][i]:<10.2f}%\n")

                    f.write(f"\nДанные для Excel (время {selected_time} мин):\n")
                    f.write("Время\tОпт. плотность\tC, мг/мл\tC в 6мл, мг\tСумма C, мг\tПроцент\n")
                    for i in range(len(time_points)):
                        f.write(f"{time_points[i]}\t{data['a_values'][i]:.6f}\t{data['c_values'][i]:.16f}\t"
                                f"{data['c_6ml_values'][i]:.16f}\t{data['sum_values'][i]:.16f}\t"
                                f"{data['percent_values'][i]:.2f}%\n")
                    
                    f.write(f"\n{'-' * 80}\n\n")
                
                # ТАБЛИЦА ДЛЯ ГРАФИКА
                f.write(f"ТАБЛИЦА ДЛЯ ПОСТРОЕНИЯ ГРАФИКА ВЫСВОБОЖДЕНИЯ\n")
                f.write(f"{'=' * 80}\n")
                f.write("Время (с)")
                for time_val in sorted(all_tables.keys()):
                    f.write(f"\t{time_val} мин (мг)")
                f.write("\n")
                
                for i in range(len(time_points)):
                    row = f"{time_points[i]}"
                    for time_val in sorted(all_tables.keys()):
                        data = all_tables[time_val]
                        row += f"\t{data['sum_values'][i]:.16f}"
                    f.write(row + "\n")
                
                # Итоги
                f.write(f"\nИТОГИ НА 180 СЕКУНДЕ:\n")
                f.write(f"{'=' * 80}\n")
                f.write("Время высвобождения\tСумма C (мг)\tПроцент последнего шага\n")
                for selected_time in sorted(all_tables.keys()):
                    total_released = all_tables[selected_time]['total_released']
                    last_percent = all_tables[selected_time]['percent_values'][-1]
                    f.write(f"{selected_time} мин\t\t{total_released:.16f}\t{last_percent:.2f}%\n")

            print(f"✓ Все результаты сохранены в файл: {filename}")
    else:
        print("\nНет созданных таблиц.")


# Запуск программы
if __name__ == "__main__":
    while True:
        calculate_kinetics()

        again = input("\nВыполнить расчет для другого вещества/концентрации? (да/нет): ").lower()
        if again not in ['да', 'yes', 'y', 'д']:
            print("\nСпасибо за использование программы!")
            break
        print("\n" + "=" * 80 + "\n")
