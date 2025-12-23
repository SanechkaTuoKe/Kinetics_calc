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
        percent_values = []  # С/С₀ × 100% - процент высвобождения

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

        all_tables[selected_time] = {
            'a_values': a_values,
            'c_values': c_values,
            'c_6ml_values': c_6ml_values,
            'sum_values': sum_values,
            'total_released': sum_values[-1]  # Итоговое значение за 180 сек
        }

        print(f"\n{'=' * 100}")
        print(f"ТАБЛИЦА для времени {selected_time} мин")
        print(f"{'=' * 100}")
        print(f"{'Время, с':<10} {'Опт. плотность':<15} {'C, мг/мл':<20} "
              f"{'C в 6мл, мг':<20} {'Сумма C, мг':<20}")
        print(f"{'-' * 85}")

        for i in range(len(time_points)):
            print(f"{time_points[i]:<10} "
                  f"{a_values[i]:<15.6f} "
                  f"{c_values[i]:<20.16f} "
                  f"{c_6ml_values[i]:<20.16f} "
                  f"{sum_values[i]:<20.16f}")

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

        # Общее количество загруженного вещества C₀ = conc × 6
        C0 = conc * 6  # мг в 6 мл
        
        print(f"\nРасчет процента высвобождения:")
        print(f"C₀ (начальное количество) = {conc} мг/мл × 6 мл = {C0} мг")
        print(f"Формула: Процент высвобождения = (Сумма C / C₀) × 100%")
        print(f"{'=' * 80}")

        # ВЫВОД ТАБЛИЦ С ПРОЦЕНТАМИ ВЫСВОБОЖДЕНИЯ (С/С₀ × 100%)
        print(f"\n{'=' * 80}")
        print("ТАБЛИЦЫ ПРОЦЕНТОВ ВЫСВОБОЖДЕНИЯ (С/С₀ × 100%)")
        print(f"{'=' * 80}")
        
        for selected_time in sorted(all_tables.keys()):
            print(f"\n--- Время высвобождения {selected_time} мин ---")
            data = all_tables[selected_time]
            print("Время (с)\tСумма C (мг)\tС/С₀, %")
            
            for i in range(len(time_points)):
                # Расчет процента: (Сумма C / C₀) × 100%
                percentage = (data['sum_values'][i] / C0) * 100 if C0 > 0 else 0
                print(f"{time_points[i]}\t{data['sum_values'][i]:.16f}\t{percentage:.6f}")
        
        # СВОДНАЯ ТАБЛИЦА ДЛЯ ГРАФИКА
        print(f"\n{'=' * 80}")
        print("СВОДНАЯ ТАБЛИЦА ДЛЯ ПОСТРОЕНИЯ ГРАФИКА")
        print(f"{'=' * 80}")
        print("Процент высвобождения С/С₀ × 100% для разных времен:")
        print(f"{'-' * 80}")
        
        # Заголовок
        header = "Время (с)"
        for time_val in sorted(all_tables.keys()):
            header += f"\t{time_val} мин"
        print(header)
        
        # Данные
        for i in range(len(time_points)):
            row = f"{time_points[i]}"
            for time_val in sorted(all_tables.keys()):
                data = all_tables[time_val]
                percentage = (data['sum_values'][i] / C0) * 100 if C0 > 0 else 0
                row += f"\t{percentage:.6f}"
            print(row)

        # Вывод в формате для Excel
        print(f"\n{'=' * 80}")
        print("ДАННЫЕ ДЛЯ КОПИРОВАНИЯ В EXCEL:")
        print(f"{'=' * 80}")

        for selected_time in sorted(all_tables.keys()):
            print(f"\n--- Время {selected_time} мин ---")
            data = all_tables[selected_time]
            print("Время\tОпт. плотность\tC, мг/мл\tC в 6мл, мг\tСумма C, мг\tС/С₀, %")
            for i in range(len(time_points)):
                percentage = (data['sum_values'][i] / C0) * 100 if C0 > 0 else 0
                print(f"{time_points[i]}\t{data['a_values'][i]:.6f}\t{data['c_values'][i]:.16f}\t"
                      f"{data['c_6ml_values'][i]:.16f}\t{data['sum_values'][i]:.16f}\t{percentage:.6f}")

        # Итоговые результаты
        print(f"\n{'=' * 80}")
        print("ИТОГОВЫЕ ПРОЦЕНТЫ ВЫСВОБОЖДЕНИЯ (на 180 секунде):")
        print(f"{'=' * 80}")
        print("Время высвобождения\tСумма C (мг)\tС/С₀, %")
        for selected_time in sorted(all_tables.keys()):
            total_released = all_tables[selected_time]['total_released']
            percentage = (total_released / C0) * 100 if C0 > 0 else 0
            print(f"{selected_time} мин\t\t{total_released:.16f}\t{percentage:.6f}")

        # Предложение сохранить результаты
        save = input("\nСохранить все результаты в файл? (да/нет): ").lower()
        if save in ['да', 'yes', 'y', 'д']:
            from datetime import datetime
            filename = f"результаты_фурациллин_{conc}мг_все_времена.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Пересчетка концентраций для кинетики (by Саша)\n")
                f.write(f"Вещество: {substance_name}\n")
                f.write(f"Концентрация раствора: {conc} мг/мл\n")
                f.write(f"C₀ (начальное количество) = {conc} × 6 = {C0} мг\n")
                f.write(f"Формула: Процент высвобождения = (Сумма C / C₀) × 100%\n")
                f.write(f"Количество таблиц: {len(all_tables)}\n")
                f.write(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
                f.write(f"{'=' * 80}\n\n")

                for selected_time in sorted(all_tables.keys()):
                    data = all_tables[selected_time]
                    f.write(f"ТАБЛИЦА для времени высвобождения {selected_time} мин\n")
                    f.write(f"{'=' * 100}\n")
                    f.write(f"{'Время, с':<10} {'Опт. плотность':<15} {'C, мг/мл':<20} "
                            f"{'C в 6мл, мг':<20} {'Сумма C, мг':<20} {'С/С₀, %':<15}\n")
                    f.write(f"{'-' * 100}\n")

                    for i in range(len(time_points)):
                        percentage = (data['sum_values'][i] / C0) * 100 if C0 > 0 else 0
                        f.write(f"{time_points[i]:<10} {data['a_values'][i]:<15.6f} "
                                f"{data['c_values'][i]:<20.16f} "
                                f"{data['c_6ml_values'][i]:<20.16f} "
                                f"{data['sum_values'][i]:<20.16f} "
                                f"{percentage:<15.6f}\n")

                    f.write(f"\nДанные для Excel (время {selected_time} мин):\n")
                    f.write("Время\tОпт. плотность\tC, мг/мл\tC в 6мл, мг\tСумма C, мг\tС/С₀, %\n")
                    for i in range(len(time_points)):
                        percentage = (data['sum_values'][i] / C0) * 100 if C0 > 0 else 0
                        f.write(f"{time_points[i]}\t{data['a_values'][i]:.6f}\t{data['c_values'][i]:.16f}\t"
                                f"{data['c_6ml_values'][i]:.16f}\t{data['sum_values'][i]:.16f}\t{percentage:.6f}\n")
                    
                    f.write(f"\n{'-' * 80}\n\n")
                
                # Сводная таблица для графика
                f.write(f"СВОДНАЯ ТАБЛИЦА ДЛЯ ГРАФИКА\n")
                f.write(f"{'=' * 80}\n")
                f.write("Процент высвобождения С/С₀ × 100%:\n")
                f.write(f"{'-' * 80}\n")
                f.write("Время (с)")
                for time_val in sorted(all_tables.keys()):
                    f.write(f"\t{time_val} мин")
                f.write("\n")
                
                for i in range(len(time_points)):
                    row = f"{time_points[i]}"
                    for time_val in sorted(all_tables.keys()):
                        data = all_tables[time_val]
                        percentage = (data['sum_values'][i] / C0) * 100 if C0 > 0 else 0
                        row += f"\t{percentage:.6f}"
                    f.write(row + "\n")
                
                # Итоги
                f.write(f"\nИТОГИ НА 180 СЕКУНДЕ:\n")
                f.write(f"{'=' * 80}\n")
                f.write("Время высвобождения\tСумма C (мг)\tС/С₀, %\n")
                for selected_time in sorted(all_tables.keys()):
                    total_released = all_tables[selected_time]['total_released']
                    percentage = (total_released / C0) * 100 if C0 > 0 else 0
                    f.write(f"{selected_time} мин\t\t{total_released:.16f}\t{percentage:.6f}\n")

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
