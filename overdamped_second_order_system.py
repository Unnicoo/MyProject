import numpy as np


class OverdampedSecondOrderSystem:
    def __init__(self, zeta, omega_n, dt):
        """
        Initialize the overdamped second-order system.

        Args:
            zeta (float): Damping ratio (>1 for overdamped)
            omega_n (float): Natural frequency (rad/s)
            dt (float): Time step for numerical integration (s)
        """
        if zeta <= 1:
            raise ValueError("Zeta must be greater than 1 for overdamped system")
        if omega_n <= 0:
            raise ValueError("Natural frequency must be positive")
        if dt <= 0:
            raise ValueError("Time step must be positive")

        self.zeta = zeta
        self.omega_n = omega_n
        self.dt = dt
        self.reset()

    def reset(self):
        """
        Reset the system state to zero.
        """
        self.state = np.array([0.0, 0.0])  # [y, dy/dt]

    def change_parameters(self, zeta, omega_n, dt=None):
        """
        Change system parameters.

        Args:
            zeta (float): New damping ratio (>1)
            omega_n (float): New natural frequency (rad/s)
            dt (float, optional): New time step (s)
        """
        if zeta <= 1:
            raise ValueError("Zeta must be greater than 1 for overdamped system")
        if omega_n <= 0:
            raise ValueError("Natural frequency must be positive")
        if dt is not None and dt <= 0:
            raise ValueError("Time step must be positive")

        self.zeta = zeta
        self.omega_n = omega_n
        if dt is not None:
            self.dt = dt
        self.reset()

    def evaluate(self, inputs, initial_state=None):
        """
        Evaluate the system response for a sequence of inputs.

        Args:
            inputs (list or np.ndarray): Sequence of input signals
            initial_state (list or np.ndarray, optional): Initial state [y, dy/dt]

        Returns:
            np.ndarray: Sequence of output responses (y values)
        """
        inputs = np.array(inputs)
        outputs = np.zeros_like(inputs)

        # Set initial state
        if initial_state is not None:
            self.state = np.array(initial_state, dtype=float)
        else:
            self.reset()

        # State-space matrices for the system
        # dx/dt = Ax + Bu
        # y = Cx
        # A: 系统内部自己怎么运动
        # B: 定义了外部输入对系统的影响
        # C: 定义了怎么从状态x提取输出y
        # 状态空间建模
        A = np.array([[0, 1],
                      [-self.omega_n ** 2, -2 * self.zeta * self.omega_n]])
        B = np.array([[0],
                      [self.omega_n ** 2]])
        C = np.array([1, 0])

        # Euler integration
        for i, u in enumerate(inputs):
            # Compute state derivative
            x_dot = A @ self.state + B.flatten() * u
            # Update state
            self.state += x_dot * self.dt
            # Compute output
            outputs[i] = C @ self.state

        return outputs
