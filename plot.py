import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('sensor_data.csv')


plt.figure(figsize=(10, 5))
plt.plot(df['Ray_Index'], df['Distance (m)'], label='Distance (Radial)', marker='o')
plt.plot(df['Ray_Index'], df['Depth (planar)'], label='Depth (Planar)', marker='s')
plt.title("Distance vs Depth per Ray")
plt.xlabel("Ray Index")
plt.ylabel("Meters")
plt.legend()
plt.grid(True)
plt.show()