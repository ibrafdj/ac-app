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

st.title('Seberapa efisien penggunaan AC kamu?')

temp_room = st.number_input('Berapa suhu di ruanganmu saat ini? (dalam °C):', min_value=0.0)
temp_ac = st.number_input('Berapa suhu AC kamu biasanya? (dalam °C):', min_value=0.0)

if st.button('Hitung'):
    temp_diff = abs(temp_room - temp_ac)
    if temp_diff > 20:
        st.write("Perbedaan suhu antara ruangan Anda dan suhu terpilih AC terlalu besar. Suhu paling efisien dari segi energi untuk ruangan Anda adalah antara 22 hingga 25,5 derajat Celsius.")
        recommended_temp = 25.5

        power_user = calculate_power_consumption(temp_ac, temp_room, 1)
        power_recommended = calculate_power_consumption(recommended_temp, temp_room, 1)
        power_diff = power_user - power_recommended
        st.write(f"Perbedaan Daya: {power_diff} Watt")
        st.write(f"Persentase Perbedaan: {(power_diff / power_user) * 100}%")
        
        st.bar_chart({'Power (W)': {"Current":power_user, "Reccommended":power_recommended}})
        # st.bar_chart({'Power (W)': [power_user, power_recommended]})
        # label_user = "Power at" + str(temp_ac)
        # label_recommended = "Power at" + str(recommended_temp)
        # power_data=pd.DataFrame({'{label_user}':[power_user], '{label_recommended}':[power_recommended]})
        # st.bar_chart(data=power_data)
    else:
        st.write("Kamu sudah menggunakan AC dengan efisien!")
        recommended_temp = temp_ac
