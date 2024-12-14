import numpy as np
import os
import tensorflow as tf
np.random.seed(143)
def fuzz_branch():
    x_shape,indice_shape,values_shape,dimension,keep_dims = gen_golden_data_simple()
    res_json = {
        "input_desc": {"x": {"shape": [*x_shape]}},
        "output_desc": {"indice": {"shape": [*indice_shape]},
                        "values": {"shape": [*values_shape]}
        },
        "attr": {"dimension": {"value": dimension},
                  "keep_dims": {"value": keep_dims}
        }
    }
    print("res_json = ",res_json)
    return res_json

def calc_expect_func(x, indice, values, dimension, keep_dims):
    
    
    res1 = np.fromfile("./output/golden_indice.bin", dtype=indice["dtype"])
    res2 = np.fromfile("./output/golden_values.bin", dtype=values["dtype"])

    return [res1, res2]


def gen_golden_data_simple():
    current_path = os.path.dirname(__file__)
    input_path = os.path.join(current_path, "input")
    output_path = os.path.join(current_path, "output")
    os.makedirs(input_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    input_x = np.random.uniform(-10, 10, [64, 64]).astype(np.float16)
    dimension = 0
    keep_dims = False
    input_x.tofile(os.path.join(input_path, "input_x.bin"))
    indice = tf.argmax(input_x, axis=dimension, output_type=tf.int32)
    values = tf.reduce_max(input_x, axis=dimension,keepdims=keep_dims)
    golden_indice = indice.numpy()
    golden_values = values.numpy()
    golden_indice.tofile(os.path.join(output_path, "golden_indice.bin"))
    golden_values.tofile(os.path.join(output_path, "golden_values.bin"))
    return input_x.shape, indice.shape ,values.shape,dimension, keep_dims


if __name__ == "__main__":
    gen_golden_data_simple()