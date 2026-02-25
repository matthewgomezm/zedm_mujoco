import mujoco
import mujoco.viewer as mv
import numpy as np

model = mujoco.MjModel.from_xml_path("zedm.xml")
data = mujoco.MjData(model)


with mv.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()
        