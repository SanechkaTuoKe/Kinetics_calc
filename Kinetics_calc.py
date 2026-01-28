def kinetics_calc():
    print("Kinetics concentration calculator (by СашаTuoKe)")
    print("\n1 - furacillin + magnesium powder (in water)")
    print(
        "Program for calculating initial concentrations, adsorption and release percentage of furacillin from magnesium powder surface")

    substance_name = "furacillin & MgO powder"

    while True:
        try:
            conc_input = input("\nEnter solution concentration (mg/ml): ").replace(',', '.')
            conc = float(conc_input)
            break
        except ValueError:
            print("Enter concentration value")

    print(f"\n{'=' * 80}")
    print(f"CALCULATION START FOR: {substance_name}")
    print(f"Solution concentration: {conc} mg/ml")
    print(f"{'=' * 80}")

    # Adsorption and initial concentrations calculation
    print("\n" + "=" * 80)
    print("ADSORPTION AND INITIAL CONCENTRATIONS CALCULATION")
    print("=" * 80)

    # C initial fur in solution
    C_start_fur = conc * 10 / 198.16

    # Enter optical density
    print(f"\nEnter 7 optical density values:")
    print("Or enter one value per line")

    a_values_ads = []
    while len(a_values_ads) < 7:
        try:
            input_line = input(f"Value {len(a_values_ads) + 1} or all 7 separated by space: ").strip()

            if not input_line:
                print("error")
                continue

            input_line_clean = input_line.replace(',', '.')
            numbers = input_line_clean.split()

            if len(numbers) == 7 and len(a_values_ads) == 0:
                a_values_ads = [float(x) for x in numbers]
                print(f"✓ Accepted 7 values from string")
                break
            elif len(numbers) == 1:
                a_values_ads.append(float(numbers[0]))
                print(f"✓ Accepted value {len(a_values_ads)}: {a_values_ads[-1]:.6f}".replace('.', ','))

                if len(a_values_ads) == 7:
                    print(f"✓ All 7 values accepted")
                    break
            else:
                print(f"Error: enter either 1 value or 7 values separated by space")
        except ValueError:
            print("Error: enter a number")

    # Dilution by default 10
    dilution_values = [10] * 7

    # Change dilution (using time instead of number)
    dilution_choice = input("\nChange dilution values? (yes/no): ").lower()
    if dilution_choice in ['да', 'yes', 'y', 'д']:
        print("\nEnter dilution values (time value):")
        print("Example: 1 10 2.5 10 5 10 7.5 10 10 10 15 10 20 10")

        while True:
            dil_input = input("Or 'ready' to finish: ")
            if dil_input.lower() in ['ready', 'done', '']:
                break

            parts = dil_input.split()
            if len(parts) >= 2:
                try:
                    # Convert time to index
                    time_val = float(parts[0].replace(',', '.'))
                    value = float(parts[1].replace(',', '.'))

                    # Find index for this time
                    time_points_ads = [1, 2.5, 5, 7.5, 10, 15, 20]
                    if time_val in time_points_ads:
                        idx = time_points_ads.index(time_val)
                        dilution_values[idx] = value
                        print(f"✓ For time {time_val} min set dilution: {value}")
                    else:
                        print(f"Error: time {time_val} not found. Available times: {time_points_ads}")
                except:
                    print("Format error")
            else:
                print("Enter time and value separated by space")

    # Calculate concentrations: C = A / 27905.64 * dilution
    C_values_spec = []
    for i in range(7):
        c = a_values_ads[i] / 27905.64 * dilution_values[i]
        C_values_spec.append(c)

    # Calculate adsorbed amount
    C0_adsorbed = []
    for c_spec in C_values_spec:
        c0 = C_start_fur - c_spec
        C0_adsorbed.append(c0)

    # Adsorption percentage
    percent_adsorption = []
    for c0 in C0_adsorbed:
        percent = (c0 / C_start_fur) * 100
        percent_adsorption.append(percent)

    # Adsorption time points
    time_points_ads = [1, 2.5, 5, 7.5, 10, 15, 20]

    def format_number(num, decimals=10):
        return f"{num:.{decimals}f}".replace('.', ',')

    # Output initial concentrations table
    print(f"\n{'=' * 100}")
    print("INITIAL CONCENTRATIONS")
    print("=" * 100)
    print("Time\tA\tDilution\tC")

    for i in range(7):
        print(f"{time_points_ads[i]}\t"
              f"{format_number(a_values_ads[i], 6)}\t"
              f"{dilution_values[i]}\t"
              f"{format_number(C_values_spec[i], 12)}")

    # Output adsorption table
    print(f"\n{'=' * 120}")
    print("ADSORPTION")
    print("=" * 120)
    print("C_initial_fur\tC₀(adsorbed)\tTime\tC_initial\t%Adsorption\tA")

    for i in range(7):
        print(f"{format_number(C_start_fur, 12)}\t"
              f"{format_number(C0_adsorbed[i], 12)}\t"
              f"{time_points_ads[i]}\t"
              f"{format_number(C_values_spec[i], 12)}\t"
              f"{format_number(percent_adsorption[i], 6)}\t"
              f"{format_number(a_values_ads[i], 6)}")

    # Create C₀ dictionary for different times
    C0_dict = {}
    for i, time in enumerate(time_points_ads):
        C0_dict[time] = C0_adsorbed[i]

    #RELEASE CALCULATION
    print(f"\n{'=' * 80}")
    print("PROCEEDING TO RELEASE CALCULATION")
    print(f"{'=' * 80}")

    times_options = [1, 2.5, 5, 7.5, 10, 15, 20]
    all_tables = {}
    time_points = [15, 30, 45, 60, 90, 120, 180]

    while True:
        print(f"\nAvailable times: {times_options}")
        print("Enter '0' to finish")

        # Select release time
        while True:
            try:
                time_input = input("Select time for calculation: ")
                if time_input == '0':
                    break

                time_input_clean = time_input.replace(',', '.')
                selected_time = float(time_input_clean)

                if selected_time in times_options:
                    if selected_time in all_tables:
                        print(f"Table for time {time_input} min already exists. Overwrite? (yes/no)")
                        rewrite = input().lower()
                        if rewrite not in ['да', 'yes', 'y', 'д']:
                            continue
                    break
                else:
                    print("Please enter value from list or '0' to finish")
            except ValueError:
                print("Enter number or '0' to finish")

        if time_input == '0':
            break

        print(f"\nSelected time: {selected_time} min")
        C0_for_this_time = C0_dict[selected_time]

        # Enter optical density for release
        print(f"\nEnter optical density values for time {selected_time} min:")
        print("Or enter one value per line")

        a_values = []
        while len(a_values) < 7:
            try:
                input_line = input(f"Value {len(a_values) + 1} or all 7 separated by space: ").strip()

                if not input_line:
                    print("Empty input. Try again:")
                    continue

                input_line_clean = input_line.replace(',', '.')
                numbers = input_line_clean.split()

                if len(numbers) == 7 and len(a_values) == 0:
                    a_values = [float(x) for x in numbers]
                    print(f"✓ Accepted 7 values from string")
                    break
                elif len(numbers) == 1:
                    a_values.append(float(numbers[0]))
                    print(f"✓ Accepted value {len(a_values)}: {a_values[-1]:.6f}".replace('.', ','))

                    if len(a_values) == 7:
                        print(f"✓ All 7 values accepted")
                        break
                else:
                    print(f"Error: enter either 1 value or 7 values separated by space")
            except ValueError:
                print("Error: enter a number")

        print(f"\nEntered optical density values:")
        for i in range(7):
            print(f"  Time {time_points[i]} sec: {a_values[i]:.6f}".replace('.', ','))

        # Calculations using original formulas
        c_values = []
        c_6ml_values = []
        sum_values = []
        percent_release = []  # NEW COLUMN

        for i, a in enumerate(a_values):
            # Original formula: C = (A + 0.00608) / 27905.64
            c = (a + 0.00608) / 27905.64
            c_values.append(c)

            # Calculate C in 6ml = C * 6
            c_6ml = c * 6
            c_6ml_values.append(c_6ml)

            # Calculate sum
            if i == 0:
                sum_val = c_6ml
            else:
                sum_val = sum_values[-1] + c_6ml
            sum_values.append(sum_val)

            # Calculate release percentage - ADDED
            if C0_for_this_time > 0:
                percent = (sum_val / C0_for_this_time) * 100
            else:
                percent = 0
            percent_release.append(percent)

        all_tables[selected_time] = {
            'a_values': a_values,
            'c_values': c_values,
            'c_6ml_values': c_6ml_values,
            'sum_values': sum_values,
            'percent_release': percent_release,
            'C0_adsorbed': C0_for_this_time
        }

        # OUTPUT TABLE FOR EXCEL with added percentage column
        print(f"\n{'=' * 120}")
        print(f"DATA FOR EXCEL - time {selected_time} min")
        print(f"C₀(adsorbed) = {format_number(C0_for_this_time, 12)}")
        print(f"{'=' * 120}")
        print("Time\tOpt.density\tC, mg/ml\tC in 6ml, mg\tSum C, mg\t% Release")

        for i in range(len(time_points)):
            print(f"{time_points[i]}\t"
                  f"{format_number(a_values[i], 6)}\t"
                  f"{format_number(c_values[i], 16)}\t"
                  f"{format_number(c_6ml_values[i], 16)}\t"
                  f"{format_number(sum_values[i], 16)}\t"
                  f"{format_number(percent_release[i], 6)}%")

        print(f"{'=' * 120}")

        print("\nAdd data for another time")
        continue_input = input("Enter 'yes' to continue or 'no' to finish: ").lower()
        if continue_input not in ['да', 'yes', 'y', 'д']:
            break

    # Output all tables for Excel
    if all_tables:
        print(f"\n{'=' * 80}")
        print("ALL DATA FOR EXCEL")
        print(f"{'=' * 80}")
        
        save_choice = input("\nSave all results to TXT file? (yes/no): ").lower()
        if save_choice in ['да', 'yes', 'y', 'д']:
            from datetime import datetime
            filename = f"kinetics_data_{conc}mg_ml_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write("KINETICS DATA CALCULATION\n")
                f.write(f"Substance: {substance_name}\n")
                f.write(f"Concentration: {conc} mg/ml\n")
                f.write(f"Date: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")

                # Write initial concentrations
                f.write("INITIAL CONCENTRATIONS\n")
                f.write("=" * 80 + "\n")
                f.write("Time\tA\tDilution\tC\n")

                for i in range(7):
                    f.write(f"{time_points_ads[i]}\t"
                            f"{format_number(a_values_ads[i], 6)}\t"
                            f"{dilution_values[i]}\t"
                            f"{format_number(C_values_spec[i], 12)}\n")

                f.write("\n" + "=" * 80 + "\n\n")

                f.write("ADSORPTION\n")
                f.write("=" * 80 + "\n")
                f.write("C_initial_fur\tC₀(adsorbed)\tTime\tC_initial\t%Adsorption\tA\n")

                for i in range(7):
                    f.write(f"{format_number(C_start_fur, 12)}\t"
                            f"{format_number(C0_adsorbed[i], 12)}\t"
                            f"{time_points_ads[i]}\t"
                            f"{format_number(C_values_spec[i], 12)}\t"
                            f"{format_number(percent_adsorption[i], 6)}\t"
                            f"{format_number(a_values_ads[i], 6)}\n")

                f.write("\n" + "=" * 80 + "\n\n")
                f.write("RELEASE DATA\n")
                f.write("=" * 80 + "\n")

                for selected_time in sorted(all_tables.keys()):
                    data = all_tables[selected_time]
                    f.write(f"\nTime: {format_number(selected_time)} min\n")
                    f.write("Time\tOpt.density\tC, mg/ml\tC in 6ml, mg\tSum C, mg\t% Release\n")

                    for i in range(len(time_points)):
                        f.write(f"{time_points[i]}\t"
                                f"{format_number(data['a_values'][i], 6)}\t"
                                f"{format_number(data['c_values'][i], 16)}\t"
                                f"{format_number(data['c_6ml_values'][i], 16)}\t"
                                f"{format_number(data['sum_values'][i], 16)}\t"
                                f"{format_number(data['percent_release'][i], 6)}%\n")

                    f.write("-" * 80 + "\n")

            print(f"✓ All data saved to file: {filename}")

        for selected_time in sorted(all_tables.keys()):
            data = all_tables[selected_time]
            print(f"\n--- Time {format_number(selected_time)} min ---")
            print("Time\tOpt.density\tC, mg/ml\tC in 6ml, mg\tSum C, mg\t% Release")

            for i in range(len(time_points)):
                print(f"{time_points[i]}\t"
                      f"{format_number(data['a_values'][i], 6)}\t"
                      f"{format_number(data['c_values'][i], 16)}\t"
                      f"{format_number(data['c_6ml_values'][i], 16)}\t"
                      f"{format_number(data['sum_values'][i], 16)}\t"
                      f"{format_number(data['percent_release'][i], 6)}%")
    else:
        print("\nNo tables created.")


if __name__ == "__main__":
    while True:
        kinetics_calc()

        again = input("\nCalculate for different concentration?").lower()
        if again not in ['да', 'yes', 'y', 'д']:
            break
        print("\n" + "=" * 80 + "\n")
