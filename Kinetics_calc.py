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

        # Ввод значений для столбца A (оптическая плотность)
        print(f"\nВведите значения оптической плотности для времени {selected_time} мин:")
        print("Пример: 0.00224 0.00247 0.00305 0.00249 0.00368 0.00342 0.00531")

        while True:
            try:
                a_values_input = input("Значения (7 чисел через пробел): ")
                a_values = [float(x.replace(',', '.')) for x in a_values_input.split()]
                if len(a_values) == 7:
                    break
                else:
                    print(f"Нужно 7 значений,ввели {len(a_values)}")
            except ValueError:
                print("Пожалуйста, введите числа через пробел")

        c_values = []  # C - концентрация
        c_6ml_values = []  # C в 6мл в k-ый момент времени = C * 0.06
        sum_values = []  # Сумма концентраций к k-му моменту времени

        for i, a in enumerate(a_values):
            # Расчет C по формуле: C = (A + 0.00608) / 27905.64
            c = (a + 0.00608) / 27905.64
            c_values.append(c)

            # Расчет C в 6мл = C * 0.06
            c_6ml = c * 0.06
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
            'total_released': sum_values[-1]  # Сохраняем итоговое значение за 180 сек
        }

        print(f"\n{'=' * 80}")
        print(f"ТАБЛИЦА для времени {selected_time} мин")
        print(f"{'=' * 80}")
        print(f"{'Время, с':<12} {'Опт. плотность (A)':<20} {'C, мг/мл':<25} "
              f"{'C в 6мл, мг':<25} {'Сумма C, мг':<25}")
        print(f"{'-' * 110}")

        for i in range(len(time_points)):
            print(f"{time_points[i]:<12} "
                  f"{a_values[i]:<20.6f} "
                  f"{c_values[i]:<25.16f} "
                  f"{c_6ml_values[i]:<25.16f} "
                  f"{sum_values[i]:<25.16f}")

        print(f"{'=' * 80}")

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
            print("Время\tОпт. плотность (A)\tC, мг/мл\tC в 6мл, мг\tСумма C, мг")
            for i in range(len(time_points)):
                print(f"{time_points[i]}\t{data['a_values'][i]:.6f}\t{data['c_values'][i]:.16f}\t"
                      f"{data['c_6ml_values'][i]:.16f}\t{data['sum_values'][i]:.16f}")

        # ТАБЛИЦА ДЛЯ ГРАФИКА ВЫСВОБОЖДЕНИЯ
        print(f"\n{'=' * 80}")
        print("ТАБЛИЦА ДЛЯ ГРАФИКА ВЫСВОБОЖДЕНИЯ")
        print(f"{'=' * 80}")
        print("Скопируйте эту таблицу для построения графика в Excel:")
        print("Время (мин)\tВысвободилось (мг)\tПроцент высвобождения")

        # Рассчитываем проценты высвобождения для каждого времени
        total_possible = conc * 6  # Общее количество в 6 мл

        for selected_time in sorted(all_tables.keys()):
            total_released = all_tables[selected_time]['total_released']
            percentage = (total_released / total_possible) * 100 if total_possible > 0 else 0
            print(f"{selected_time}\t{total_released:.16f}\t{percentage:.4f}")

        # Дополнительная информация
        print(f"\n{'=' * 80}")
        print("ИНФОРМАЦИЯ О РАСЧЕТЕ:")
        print(f"{'=' * 80}")
        print(f"1. Использованная формула: C = (A + 0.00608) / 27905.64")
        print(f"2. Где A - оптическая плотность")
        print(f"3. C в 6мл = C * 0.06")
        print(f"4. Сумма - накопленная сумма C в 6мл")
        print(f"5. Общее количество в 6 мл: {total_possible} мг")
        print(f"6. Процент высвобождения = (высвободившееся количество / {total_possible}) * 100%")

        # Итоговые результаты
        print(f"\nРЕЗУЛЬТАТЫ ПО ВРЕМЕНАМ:")
        for selected_time in sorted(all_tables.keys()):
            total_released = all_tables[selected_time]['total_released']
            percentage = (total_released / total_possible) * 100 if total_possible > 0 else 0
            print(f"  {selected_time} мин: {total_released:.10f} мг ({percentage:.4f}%)")

        # Предложение сохранить результаты
        save = input("\nСохранить все результаты в файл? (да/нет): ").lower()
        if save in ['да', 'yes', 'y', 'д']:
            filename = f"результаты_фурациллин_{conc}мг_все_времена.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Пересчетка концентраций для кинетики (by Саша)\n")
                f.write(f"Вещество: {substance_name}\n")
                f.write(f"Концентрация раствора: {conc} мг/мл\n")
                f.write(f"Количество таблиц: {len(all_tables)}\n")
                f.write(f"{'=' * 80}\n\n")

                for selected_time in sorted(all_tables.keys()):
                    data = all_tables[selected_time]
                    f.write(f"ТАБЛИЦА для времени {selected_time} мин\n")
                    f.write(f"{'=' * 80}\n")
                    f.write(f"{'Время, с':<12} {'Опт. плотность (A)':<20} {'C, мг/мл':<25} "
                            f"{'C в 6мл, мг':<25} {'Сумма C, мг':<25}\n")
                    f.write(f"{'-' * 110}\n")

                    for i in range(len(time_points)):
                        f.write(f"{time_points[i]:<12} {data['a_values'][i]:<20.6f} {data['c_values'][i]:<25.12f} "
                                f"{data['c_6ml_values'][i]:<25.16f} {data['sum_values'][i]:<25.16f}\n")

                    f.write(f"\nДанные для Excel (время {selected_time} мин):\n")
                    f.write("Время\tОпт. плотность (A)\tC, мг/мл\tC в 6мл, мг\tСумма C, мг\n")
                    for i in range(len(time_points)):
                        f.write(f"{time_points[i]}\t{data['a_values'][i]:.6f}\t{data['c_values'][i]:.12f}\t"
                                f"{data['c_6ml_values'][i]:.16f}\t{data['sum_values'][i]:.16f}\n")
                    f.write(f"\n{'-' * 80}\n\n")

                # Сохраняем таблицу для графика
                f.write(f"ТАБЛИЦА ДЛЯ ГРАФИКА ВЫСВОБОЖДЕНИЯ\n")
                f.write(f"{'=' * 80}\n")
                f.write("Время (мин)\tВысвободилось (мг)\tПроцент высвобождения\n")

                for selected_time in sorted(all_tables.keys()):
                    total_released = all_tables[selected_time]['total_released']
                    percentage = (total_released / total_possible) * 100 if total_possible > 0 else 0
                    f.write(f"{selected_time}\t{total_released:.16f}\t{percentage:.4f}\n")

                f.write(f"\nИНФОРМАЦИЯ О РАСЧЕТЕ:\n")
                f.write(f"{'=' * 80}\n")
                f.write(f"1. Вещество: {substance_name}\n")
                f.write(f"2. Концентрация: {conc} мг/мл\n")
                f.write(f"3. Общее количество в 6 мл: {total_possible} мг\n")
                f.write(f"4. Формула: C = (A + 0.00608) / 27905.64\n")
                f.write(f"5. C в 6мл = C * 0.06\n")
                f.write(f"6. Процент = (высвободившееся / {total_possible}) * 100%\n")

            print(f"Все результаты сохранены в файл: {filename}")
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