import streamlit as st

# Function to calculate power usage
def calculate_power_consumption(setpoint_temp, outside_temp, efficiency):
    """
    Calculate the average power consumption of an AC device.

    Parameters:
    setpoint_temp (float): The temperature setpoint in degree Celsius.
    outside_temp (float): The outside temperature in degree Celsius.
    efficiency (float): The efficiency of the AC device (value between 0 and 1).

    Returns:
    float: The average power consumption in Watts.
    """

    # Assume a base power consumption
    base_power = 1000  # in Watts

    # Calculate the temperature difference
    temp_diff = abs(setpoint_temp - outside_temp)

    # Calculate the power consumption
    power_consumption = base_power * temp_diff * (1 / efficiency)

    return power_consumption

# Function to calculate electricity bills 
def calculate_electricity_bills(kwh, rate):
    return kwh * rate

def float_to_currency(value: float, currency_symbol: str = '$') -> str:
    return f"{currency_symbol}{format(value, ',.2f')}"

st.title('SejukHemat')

# Temp options
temp_room = st.number_input('Berapa suhu di ruanganmu saat ini? (dalam °C):', min_value=0.0)
temp_ac = st.number_input('Berapa suhu AC yang biasa kamu pilih di ruanganmu? (dalam °C):', min_value=16.0, max_value=30.0)

# Rate options
rate_options = ['900VA', '1300VA', '2200VA', '>=3500VA']
selected_rate_option = st.selectbox('Pilih daya yang terpasang di rumah:', rate_options)
# Hour options
hours = st.number_input('Berapa lama AC di ruanganmu menyala setiap harinya? (Dalam jam):', min_value=0, max_value=24, value=8)

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
    if(temp_room <= 5):
        temp_optimal = 19.5
    elif (temp_room >= 32):
        temp_optimal = 25.5
    else:
        temp_optimal = 24 #???

    temp_diff = abs(temp_room - temp_ac)
    if temp_diff <= 0.5:
        st.write(f"Temperatur pas!")
    else:
        st.write(f"Perbedaan suhu antara ruangan Anda dan suhu terpilih AC terlalu besar. Suhu paling optimal untuk kondisi Anda adalah {temp_optimal} derajat Celsius.")

    power_user = calculate_power_consumption(temp_ac, temp_room, 1)
    power_optimal = calculate_power_consumption(temp_optimal, temp_room, 1)
    power_diff = power_user - power_optimal
    st.write(f"Perbedaan Daya: {power_diff} Watt")
    st.write(f"Persentase Perbedaan: {(power_diff / power_user) * 100}%")
    st.bar_chart({'Power (W)': {"Current":power_user, "Optimal":power_optimal}})

    # TODO: Change power estimation function to just assume a % increase in power consumption at every increase/decrease in degree celcius
    # TODO: Create feature to visualize amount of money that can be saved from your energy bills based on the selected VA rating.
    total_kwh = power_diff * hours / 1000
    total_bills = calculate_electricity_bills(total_kwh, rate)
    total_idr = float_to_currency(total_bills, 'Rp')
    st.write(f"Berapa banyak tagihan listrik yang bisa dihemat dalam sebulan dengan memilih temperatur optimum?")
    st.write(f"Total tagihan listrik yang dapat dihemat adalah sebesar **{total_idr}**")