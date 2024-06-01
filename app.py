import streamlit as st

# Function to calculate power usage
def calculate_power_consumption(area, height, temp_diff_celsius):
    # Convert temperature difference from Celsius to Fahrenheit
    temp_diff_fahrenheit = temp_diff_celsius * 9/5

    # Calculate BTU
    # btu = (area * 10.764) * (height*3.28) * temp_diff_fahrenheit * 4.5
    btu = area * height * temp_diff_fahrenheit * 4.5

    # Convert BTU to Watts
    watts = btu * 0.29307107

    return watts

# Function to calculate electricity bills 
def calculate_electricity_bills(kwh, rate):
    return kwh * rate

def float_to_currency(value: float, currency_symbol: str = '$') -> str:
    return f"{currency_symbol}{format(value, ',.2f')}"

st.title('SejukHemat')

# Temp options
temp_room = st.number_input('Berapa suhu diluar ruanganmu saat ini? (dalam °C):', min_value=0.0)
temp_ac = st.number_input('Berapa suhu AC yang biasa kamu pilih di ruanganmu? (dalam °C):', min_value=16.0, max_value=30.0)
area = st.number_input('Berapa luas ruanganmu? (dalam m^2):', min_value=0.0, value=6.0)
height = st.number_input('Berapa tinggi ruanganmu? (dalam m):', min_value=0.0, value=3.0)

# Rate options
rate_options = ['900VA', '1300VA', '2200VA', '>=3500VA']
selected_rate_option = st.selectbox('Pilih kelompok daya listrik PLN yang terpasang di rumah:', rate_options)
# Hour options
hours = st.number_input('Berapa lama AC di ruanganmu menyala setiap harinya? (dalam jam):', min_value=0, max_value=24, value=8)

match selected_rate_option:
    case '900VA':
        rate = 1352
    case '1300VA':
        rate = 1444.7
    case '2200VA':
        rate = 1444.7
    case '>=3500VA':
        rate = 1699.53

# with st.popover("Open popover"):
#     st.markdown("Hello World 👋")
#     name = st.text_input("What's your name?")
#     st.write("Your name:", name)

if st.button('Hitung'):
    # TODO: May not be scientific to use temp diff, better to check if it is below 5C (Setpoint=19.5C) or above 32C (Setpoint=25.5C)
    if(temp_room < temp_ac):
        st.write(f"Suhu diluar ruanganmu lebih rendah dari suhu AC. Di kondisi dingin seperti sebaiknya matikan AC saja untuk menghemat energi ya!")
    elif(temp_room < 25):
        st.write(f"Suhu diluar ruanganmu masuk dalam suhu yang cukup nyaman untuk manusia beristirahat. Di kondisi dingin seperti sebaiknya matikan AC saja untuk menghemat energi ya!")
    else:
        if(temp_room <= 5):
            temp_optimal = 19.5
        elif(temp_room >= 25 and temp_room < 26):
            temp_optimal = 25
        elif(temp_room >= 26 and temp_room < 27):
            temp_optimal = 25.3
        elif(temp_room >= 27 and temp_room < 28):
            temp_optimal = 25.4
        elif(temp_room >= 28 and temp_room < 29):
            temp_optimal = 25.4
        elif (temp_room >= 32):
            temp_optimal = 25.5
        else:
            temp_optimal = 25.5 #???

        temp_setpoint_diff = abs(temp_ac - temp_optimal)
        if temp_setpoint_diff <= 0.5:
            st.write(f"Suhu yang kamu pilih sudah pas! Kamu sudah memilih suhu AC yang hemat energi.")
            st.write(f"Suhu optimal untuk AC adalah {temp_optimal}°C.")
        elif temp_ac > temp_optimal:
            st.write(f"Suhu yang kamu pilih sudah lebih tinggi dari suhu optimal! Kamu sudah memilih suhu AC yang hemat energi.")
            st.write(f"Suhu optimal untuk AC adalah {temp_optimal}°C.")
        else:
            st.write(f"Perbedaan suhu antara ruangan Anda dan suhu terpilih AC terlalu besar!")
            st.write(f"Suhu optimal untuk AC adalah {temp_optimal}°C.")
        
        with st.popover("Suhu optimal AC ini didapatkan dari mana?"):
           st.markdown("Secara umum, [US Department of Energy](https://www.energy.gov/energysaver/energy-saver) merekomendasikan temperatur AC sebesar 25.5°C pada musim panas sebagai suhu yang paling efisien secara pengeluaran energi.")
           st.markdown("Riset dari [National University of Singapore](https://www.mdpi.com/2583274) (Talami et al., 2023) menggunakan suhu dari negara Singapura juga menunjukkan bahwa temperatur optimal AC berkisar di 25-25.5°C saat suhu di luar berada di 25-29.9°C.")
           st.markdown("Suhu optimal disini hanyalah estimasi. Perhitungan suhu yang akurat bergantung pada faktor-faktor seperti kelembaban relatif, insulasi suhu dalam ruangan, efisiensi AC, dsb.")

        temp_diff = abs(temp_ac - temp_room)
        temp_diff_optimal = abs(temp_optimal - temp_room)
        power_user = calculate_power_consumption(area, height, temp_diff)
        power_optimal = calculate_power_consumption(area, height, temp_diff_optimal)
        power_diff = power_user - power_optimal

        # TODO: Change power estimation function to just assume a % increase in power consumption at every increase/decrease in degree celcius
        # TODO: Create feature to visualize amount of money that can be saved from your energy bills based on the selected VA rating.
        kwh_user = power_user * hours / 1000
        bills_user = calculate_electricity_bills(kwh_user, rate) * 30
        bills_user_idr = float_to_currency(bills_user, 'Rp')

        kwh_optimal = power_optimal * hours / 1000
        bills_optimal = calculate_electricity_bills(kwh_optimal, rate) * 30
        bills_optimal_idr = float_to_currency(bills_optimal, 'Rp')

        # total_kwh = power_diff * hours / 1000
        # total_bills = calculate_electricity_bills(total_kwh, rate)\
        total_bills = abs(bills_user - bills_optimal)
        total_idr = float_to_currency(total_bills, 'Rp')

        # st.write(f"Daya user: {power_user} Watt")
        # st.write(f"Persentase Perbedaan: {(power_diff / power_user) * 100}%")
        st.write("Berikut adalah grafik perbandingan estimasi tagihan antara pilihan temperatur AC awal dan optimal:")
        st.bar_chart({'Estimasi Tagihan Listrik Bulanan (Rp)': {"Awal":bills_user, "Optimal":bills_optimal}})
        if(bills_user > bills_optimal):
            st.write(f"Estimasi tagihan listrik yang dapat dihemat adalah sebesar **{total_idr}** per bulan.")
        else:
            st.write(f"Estimasi tagihan listrik kamu sudah lebih hemat dari suhu optimal sebesar **{total_idr}** per bulan.")

        with st.popover("Estimasi penghematan ini cara menghitunganya bagaimana?"):
            st.markdown("Perhitungan dilakukan menggunakan rumus untuk menghitung BTU (British Thermal Unit), yaitu [rumus](https://smartacsolutions.com/air-conditioner-btu-calculator/) untuk menghitung berapa banyak daya yang diperlukan untuk memanaskan atau mendinginkan suatu ruangan ke suhu tertentu:")
            st.markdown("> BTU = Luas Ruangan x Tinggi Ruangan x 4.5")
            st.markdown("Diasumsikan insulasi ruangan standar dengan faktor insulasi 4.5")
            st.markdown("Kemudian BTU dikonversi kedalam satuan Watt (W). Diasumsikan bahwa AC memiliki efisiensi 100%, dimana daya yang dibutuhkan untuk mendinginkan ruangan sama dengan daya listrik yang dikeluarkan oleh AC.")
            st.markdown("Daya tersebut kemudian dikalikan dengan durasi AC menyala setiap harinya untuk menghasilkan pengeluaran energi dari AC per hari (dalam kWh).")
            st.markdown("Tagihan listrik dapat dihitung berdasarkan [tarif](https://web.pln.co.id/statics/uploads/2024/03/Penetapan-Penyesuaian-TTL-TARIFF-ADJUSTMENT-Apri-Juni-2024_1-1.jpg) setiap kelompok daya yang telah ditetapkan PLN.")
