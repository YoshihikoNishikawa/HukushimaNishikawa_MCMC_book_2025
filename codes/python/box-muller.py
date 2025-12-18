###################################################################################
# PROGRAM: box-muller.py
# DATE: 2025-12-17
# NOTICE: This program accompanies the book "マルコフ連鎖モンテカルロ法入門"
#                     by Koji Hukushima and Yoshihiko Nishikawa
###################################################################################

import random
import math as m

random.seed("I love Monte Carlo!")
sample_size = 10

for _ in range(sample_size):
    u_1 = random.uniform(0, 1)
    u_2 = random.uniform(0, 1)
    sqrt_part = (-2.0 * m.log(u_1))**.5
    z_1 = sqrt_part * m.cos(2.0 * m.pi * u_2)
    z_2 = sqrt_part * m.sin(2.0 * m.pi * u_2)
    print(z_1, z_2)
