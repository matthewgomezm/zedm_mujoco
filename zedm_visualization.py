import mujoco
import mujoco.viewer as mv

import numpy as np
import pandas as pd


class ZedSim:
    def __init__(self, model_path):
        self.model = mujoco.MjModel.from_xml_path(model_path)
        self.data = mujoco.MjData(self.model)

    def get_sensor_data(self):
        sensor_data =  self.data.sensordata
        return sensor_data


def save_to_csv(raw_data, filename="sensor_data.csv"):
    data_array = np.array(raw_data)
    
    try:
        reshaped_data = data_array.reshape(-1, 8)
    except ValueError:
        return None

    columns = [
        'Distance (m)',
        'Point_X (m)',
        'Point_Y (m)',
        'Point_Z (m)',
        'Normal_X',
        'Normal_Y',
        'Normal_Z',
        'Depth (planar)'
    ]
    
    df = pd.DataFrame(reshaped_data, columns=columns)
    df.insert(0, 'Ray_Index', range(len(df)))
    df.to_csv(filename, index=False, mode='w')    
    return df

zed = ZedSim("zedm.xml")

with mv.launch_passive(zed.model, zed.data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(zed.model, zed.data)
        viewer.sync()
        

print("Sensor data:", zed.get_sensor_data())
save_to_csv(zed.get_sensor_data())


## evaluate data
## then control wheels