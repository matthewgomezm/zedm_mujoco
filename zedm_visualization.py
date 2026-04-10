import json
import mujoco
import mujoco.viewer as mv
import numpy as np
import pandas as pd


class ZedSim:
    def __init__(self, model_path):
        self.model = mujoco.MjModel.from_xml_path(model_path)
        self.data = mujoco.MjData(self.model)

    def get_camera_params(self, camera_name):
        cam_id = self.model.camera(camera_name).id
        fovy = float(self.model.cam_fovy[cam_id])
        width, height = self.model.cam_resolution[cam_id]
        return {"fovy_deg": fovy, "width": int(width), "height": int(height)}
 
    def get_sensor_data(self, sensor_name):
        sensor_id = self.model.sensor(sensor_name).id
        sensor_adr = self.model.sensor_adr[sensor_id]
        sensor_dim = self.model.sensor_dim[sensor_id]
        return self.data.sensordata[sensor_adr : sensor_adr + sensor_dim].copy()

    def control(self, left_speed, right_speed):
        self.data.ctrl[0] = left_speed   # left_drive_back
        self.data.ctrl[1] = right_speed  # right_drive_back
        self.data.ctrl[2] = left_speed   # left_drive_front
        self.data.ctrl[3] = right_speed  # right_drive_front


def save_to_csv(raw_data, filename, columns):
    data_array = np.array(raw_data)
    num_cols = len(columns)
    
    reshaped_data = data_array.reshape(-1, num_cols)
    df = pd.DataFrame(reshaped_data, columns=columns)
    
    if len(df) > 1:
        df.insert(0, 'Ray_Index', range(len(df)))
        
    df.to_csv(filename, index=False, mode='w')    
    return df

# columns for csv
cam_cols = ['Distance (m)', 
            'Point_X (m)', 'Point_Y (m)', 'Point_Z (m)', 
            'Normal_X', 'Normal_Y', 'Normal_Z', 
            'Depth (planar)']
gyro_cols = ['Gyro_X', 'Gyro_Y', 'Gyro_Z']
accel_cols = ['Accel_X', 'Accel_Y', 'Accel_Z']

gyro_data = []
accel_data = []
MOD_RATE = 100

#zed = ZedSim("zedm.xml")
## when rough xml is used:
zed = ZedSim("zedm_rough.xml")
step = 0

with mv.launch_passive(zed.model, zed.data) as viewer:
    while viewer.is_running():
        #zed.control(0.5, 0.1)
        ## when rough xml is used:
        zed.control(0.25, 0.25)
        mujoco.mj_step(zed.model, zed.data)
        viewer.sync()

        if step % MOD_RATE == 0:
            gyro_data.append(zed.get_sensor_data("zedm_gyro"))
            accel_data.append(zed.get_sensor_data("zedm_accel"))
        step += 1

save_to_csv(zed.get_sensor_data("zedm_perspective"), "rangefinder_data.csv", cam_cols)
save_to_csv(gyro_data, "gyro_data.csv", gyro_cols)
save_to_csv(accel_data, "accel_data.csv", accel_cols)

cam_params = zed.get_camera_params("perspective")
with open("camera_params.json", "w") as f:
    json.dump(cam_params, f, indent=2)
