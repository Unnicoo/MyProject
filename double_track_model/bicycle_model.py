import math


class BicycleModel:
    def __init__(self, x, y, psi, v, f_len, r_len):
        self.x = x
        self.y = y
        self.psi = psi
        self.v = v

        self.f_len = f_len
        self.r_len = r_len

    def get_state(self):
        return self.x, self.y, self.psi, self.v

    def update_state(self, a, delta_f, delta_r, dt):
        beta = math.atan((math.tan(delta_f) * self.r_len + math.tan(delta_r) * self.f_len)/(self.f_len + self.r_len))

        self.x = self.x + self.v * math.cos(self.psi + beta) * dt
        self.y = self.y + self.v * math.sin(self.psi + beta) * dt
        self.psi = self.psi + self.v * math.cos(beta) / (self.f_len + self.r_len) * (math.tan(delta_f) - math.tan(delta_r)) * dt
        self.v = self.v + a * dt

    # def cost_func(self):
    #     for i in range(67):
    #         delta =