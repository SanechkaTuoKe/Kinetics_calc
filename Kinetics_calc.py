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
    concentrations = []
    print(f"\nконцентрации раствора: {concentrations}")

    while True:
        try:
            conc_input = input("Введите концентрацию раствора: ").replace(',', '.')
            conc = float(conc_input)
            if conc in [20, 15, 10, 5, 2.5, 1, 0.5, 0.1, 0.01]:
                break
            else:
                print("введите значение из списка")
        except ValueError:
            print("введите значение из списка")

    times_options = [1, 2, 5, 5, 7, 5, 10, 15, 20]

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
                time_input_clean = time_input.replace(',', '.')
                selected_time = float(time_input_clean)

                # Проверяем с учетом возможных форматов
                if selected_time in [1, 2.5, 5, 7.5, 10, 15, 20]:
                    if selected_time in all_tables:
                        print(f"Для времени {time_input} мин уже есть таблица. Хотите перезаписать? (да/нет)")
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

        print(f"\nВыбрано время: {time_input} мин")

        print(f"\nВведите значения оптической плотности для времени {time_input} мин:")
        print("Пример: 0,00224 0,00247 0,00305 0,00249 0,00368 0,00342 0,00531")
        print("Или вводите по одному числу на строку")

        a_values = []

        while len(a_values) < 7:
            try:
                input_line = input(f"Значение {len(a_values) + 1} или все 7 через пробел: ").strip()

                if not input_line:
                    print("Пустой ввод. Попробуйте еще раз:")
                    continue
                input_line_clean = input_line.replace(',', '.')
                numbers = input_line_clean.split()

                if len(numbers) == 7 and len(a_values) == 0:
                    # Введена строка с 7 числами
                    a_values = [float(x) for x in numbers]
                    print(f"✓ Принято 7 значений из строки")
                    break
                elif len(numbers) == 1:
                    # Введено одно число
                    a_values.append(float(numbers[0]))
                    print(f"✓ Принято значение {len(a_values)}: {a_values[-1]:.6f}".replace('.', ','))

                    if len(a_values) == 7:
                        print(f"✓ Принято все 7 значений")
                        break
                else:
                    print(f"Ошибка: нужно ввести либо 1 число, либо 7 чисел через пробел")

            except ValueError:
                print("Ошибка: введите число")

        print(f"\nВведенные значения оптической плотности:")
        for i in range(7):
            print(f"  Время {time_points[i]} сек: {a_values[i]:.6f}".replace('.', ','))

        c_values = []  # C - концентрация в мг/мл
        c_6ml_values = []  # C в 6мл в k-ый момент времени = C * 6
        sum_values = []  # Сумма концентраций к k-му моменту времени

        for i, a in enumerate(a_values):
            # Расчет C по формуле: C = (A + 0,00608) / 27905,64
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
            'sum_values': sum_values
        }

        def format_number(num, decimals=6):
            return f"{num:.{decimals}f}".replace('.', ',')

        # ВЫВОД ТАБЛИЧКИ ДЛЯ EXCEL
        print(f"\n{'=' * 100}")
        print(f"ДАННЫЕ ДЛЯ EXCEL - время {time_input} мин")
        print(f"{'=' * 100}")
        print("Время\tОпт. плотность\tC, мг/мл\tC в 6мл, мг\tСумма C, мг")
        
        for i in range(len(time_points)):
            print(f"{time_points[i]}\t"
                  f"{format_number(a_values[i], 6)}\t"
                  f"{format_number(c_values[i], 16)}\t"
                  f"{format_number(c_6ml_values[i], 16)}\t"
                  f"{format_number(sum_values[i], 16)}")
        
        print(f"{'=' * 100}")

        print("\nДобавить данные для другого времени")
        continue_input = input("Введите 'да' для продолжения или 'нет' для завершения: ").lower()
        if continue_input not in ['да', 'yes', 'y', 'д']:
            break

    # Вывод всех табличек для Excel
    if all_tables:
        print(f"\n{'=' * 80}")
        print("ВСЕ ДАННЫЕ ДЛЯ EXCEL")
        print(f"{'=' * 80}")

        for selected_time in sorted(all_tables.keys()):
            data = all_tables[selected_time]
            print(f"\n--- Время {format_number(selected_time)} мин ---")
            print("Время\tОпт. плотность\tC, мг/мл\tC в 6мл, мг\tСумма C, мг")
            
            for i in range(len(time_points)):
                print(f"{time_points[i]}\t"
                      f"{format_number(data['a_values'][i], 6)}\t"
                      f"{format_number(data['c_values'][i], 16)}\t"
                      f"{format_number(data['c_6ml_values'][i], 16)}\t"
                      f"{format_number(data['sum_values'][i], 16)}")
                
        save = input("\nСохранить все результаты в файл? (да/нет): ").lower()
        if save in ['да', 'yes', 'y', 'д']:
            from datetime import datetime
            filename = f"данные_для_excel_{format_number(conc).replace(',', '_')}мг.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Данные для Excel - {substance_name}\n")
                f.write(f"Концентрация раствора: {format_number(conc)} мг/мл\n")
                f.write(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
                f.write(f"{'=' * 80}\n\n")

                for selected_time in sorted(all_tables.keys()):
                    data = all_tables[selected_time]
                    f.write(f"Время высвобождения: {format_number(selected_time)} мин\n")
                    f.write("Время\tОпт. плотность\tC, мг/мл\tC в 6мл, мг\tСумма C, мг\n")
                    
                    for i in range(len(time_points)):
                        f.write(f"{time_points[i]}\t"
                                f"{format_number(data['a_values'][i], 6)}\t"
                                f"{format_number(data['c_values'][i], 16)}\t"
                                f"{format_number(data['c_6ml_values'][i], 16)}\t"
                                f"{format_number(data['sum_values'][i], 16)}\n")
                    
                    f.write(f"\n{'-' * 80}\n\n")

            print(f"✓ Все данные сохранены в файл: {filename}")
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
