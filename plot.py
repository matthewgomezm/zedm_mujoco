import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('rangefinder_data.csv')

plt.figure(figsize=(10, 5))
plt.plot(df['Ray_Index'], df['Distance (m)'], label='Distance (Radial)', marker='o')
plt.plot(df['Ray_Index'], df['Depth (planar)'], label='Depth (Planar)', marker='s')
plt.title("Distance vs Depth per Ray")
plt.xlabel("Ray Index")
plt.ylabel("Meters")
plt.legend()
plt.grid(True)

df_gyro = pd.read_csv('gyro_data.csv')

plt.figure(figsize=(10, 5))
plt.plot(df_gyro['Gyro_X'], label='Gyro X', color='r')
plt.plot(df_gyro['Gyro_Y'], label='Gyro Y', color='g')
plt.plot(df_gyro['Gyro_Z'], label='Gyro Z', color='b')
plt.title("Gyroscope Data (Time Series)")
plt.xlabel("Time Step")
plt.ylabel("Rad/s")
plt.legend()
plt.grid(True)

df_accel = pd.read_csv('accel_data.csv')

plt.figure(figsize=(10, 5))
plt.plot(df_accel['Accel_X'], label='Accel X', color='r')
plt.plot(df_accel['Accel_Y'], label='Accel Y', color='g')
plt.plot(df_accel['Accel_Z'], label='Accel Z', color='b')
plt.title("Accelerometer Data (Time Series)")
plt.xlabel("Time Step")
plt.ylabel("m/s^2")
plt.legend()
plt.grid(True)

plt.show()