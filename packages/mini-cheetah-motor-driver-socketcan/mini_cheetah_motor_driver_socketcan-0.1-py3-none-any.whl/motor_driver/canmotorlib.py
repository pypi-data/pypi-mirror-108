import socket
import struct
import time
import math
from bitstring import BitArray


# CAN frame packing/unpacking (see `struct can_frame` in <linux/can.h>)
# 8 bytes of data is sent to the motor
can_frame_fmt_send = "=IB3x8s"
# 6 bytes are received from the motor
can_frame_fmt_recv = "=IB3x6s"

# Precompute Constants for conversion
P_MIN = -95.5
P_MAX = 95.5
V_MIN = -45.0
V_MAX = 45.0
KP_MIN = 0.0
KP_MAX = 500.0
KD_MIN = 0.0
KD_MAX = 5.0
T_MIN = -18.0
T_MAX = 18.0

maxRawPosition = 2**16 - 1                      # 16-Bits for Raw Position Values
maxRawVelocity = 2**12 - 1                      # 12-Bits for Raw Velocity Values
maxRawTorque = 2**12 - 1                        # 12-Bits for Raw Torque Values
maxRawKp = 2**12 - 1                            # 12-Bits for Raw Kp Values
maxRawKd = 2**12 - 1                            # 12-Bits for Raw Kd Values
maxRawCurrent = 2**12 - 1                       # 12-Bits for Raw Current Values
dt_sleep = 0.0001                               # Time before motor sends a reply


def float_to_uint(x, x_min, x_max, numBits):
    span = x_max - x_min
    offset = x_min
    # Attempt to speedup by using pre-computation. Not used currently.
    if numBits == 16:
        bitRange = maxRawPosition
    elif numBits == 12:
        bitRange = maxRawVelocity
    else:
        bitRange = 2**numBits - 1
    return int(((x - offset) * (bitRange)) / span)


def uint_to_float(x_int, x_min, x_max, numBits):
    span = x_max - x_min
    offset = x_min
    if numBits == 16:
        bitRange = maxRawPosition
    elif numBits == 12:
        bitRange = maxRawVelocity
    else:
        bitRange = 2**numBits - 1
    return ((x_int * span) / (bitRange)) + offset


def waitOhneSleep(dt):
    startTime = time.time()
    while time.time() - startTime < dt:
        pass


class CanMotorController():
    """
    Class for creating a Mini-Cheetah Motor Controller over CAN. Uses SocketCAN driver for
    communication.
    """

    # Declare Socket as Class Attribute instead of member attribute so that it can be used across
    # multiple instances and check if the socket was declared earlier by an instance.

    can_socket_declared = False
    motor_socket = None

    def __init__(self, can_socket='can0', motor_id=0x01, socket_timeout=0.05):
        """
        Instantiate the class with socket name, motor ID, and socket timeout.
        Sets up the socket communication for rest of the functions.
        """
        can_socket = (can_socket, )
        self.motor_id = motor_id
        # create a raw socket and bind it to the given CAN interface
        if not CanMotorController.can_socket_declared:
            try:
                CanMotorController.motor_socket = socket.socket(socket.AF_CAN, socket.SOCK_RAW,
                                                                socket.CAN_RAW)
                CanMotorController.motor_socket.bind(can_socket)
                CanMotorController.motor_socket.settimeout(socket_timeout)
                print("Bound to: ", can_socket)
                CanMotorController.can_socket_declared = True
            except Exception as e:
                print("Unable to Connect to Socket Specified: ", can_socket)
                print("Error:", e)
        elif CanMotorController.can_socket_declared:
            print("CAN Socket Already Available. Using: ", CanMotorController.motor_socket)

        # Initialize the command BitArrays for performance optimization
        self._p_des_BitArray = BitArray(uint=float_to_uint(0, P_MIN, P_MAX, 16), length=16)
        self._v_des_BitArray = BitArray(uint=float_to_uint(0, V_MIN, V_MAX, 12), length=12)
        self._kp_BitArray = BitArray(uint=0, length=12)
        self._kd_BitArray = BitArray(uint=0, length=12)
        self._tau_BitArray = BitArray(uint=0, length=12)
        self._cmd_bytes = BitArray(uint=0, length=64)
        self._recv_bytes = BitArray(uint=0, length=48)

    def _send_can_frame(self, data):
        """
        Send raw CAN data frame (in bytes) to the motor.
        """
        can_dlc = len(data)
        can_msg = struct.pack(can_frame_fmt_send, self.motor_id, can_dlc, data)
        try:
            CanMotorController.motor_socket.send(can_msg)
        except Exception as e:
            print("Unable to Send CAN Frame.")
            print("Error: ", e)

    def _recv_can_frame(self):
        """
        Recieve a CAN frame and unpack it. Returns can_id, can_dlc (data length), data (in bytes)
        """
        try:
            # The motor sends back only 6 bytes.
            frame, addr = CanMotorController.motor_socket.recvfrom(14)
            can_id, can_dlc, data = struct.unpack(can_frame_fmt_recv, frame)
            return can_id, can_dlc, data[:can_dlc]
        except Exception as e:
            print("Unable to Receive CAN Franme.")
            print("Error: ", e)

    def enable_motor(self):
        """
        Sends the enable motor command to the motor.
        """
        try:
            self._send_can_frame(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFC')
            waitOhneSleep(dt_sleep)
            can_id, can_dlc, motorStatusData = self._recv_can_frame()
            rawMotorData = self.decode_motor_status(motorStatusData)
            pos, vel, curr = self.convert_raw_to_physical_rad(rawMotorData[0], rawMotorData[1],
                                                            rawMotorData[2])
            print("Motor Enabled.")
            return pos, vel, curr
        except Exception as e:
            print('Error Enabling Motor!')
            print("Error: ", e)

    def disable_motor(self):
        """
        Sends the disable motor command to the motor.
        """
        try:
            self._send_can_frame(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFD')
            waitOhneSleep(dt_sleep)
            can_id, can_dlc, motorStatusData = self._recv_can_frame()
            rawMotorData = self.decode_motor_status(motorStatusData)
            pos, vel, curr = self.convert_raw_to_physical_rad(rawMotorData[0], rawMotorData[1],
                                                            rawMotorData[2])
            print("Motor Disabled.")
            return pos, vel, curr
        except Exception as e:
            print('Error Disabling Motor!')
            print("Error: ", e)

    def set_zero_position(self):
        """
        Sends command to set current position as Zero position.
        """
        try:
            self._send_can_frame(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFE')
            waitOhneSleep(dt_sleep)
            can_id, can_dlc, motorStatusData = self._recv_can_frame()
            rawMotorData = self.decode_motor_status(motorStatusData)
            pos, vel, curr = self.convert_raw_to_physical_rad(rawMotorData[0], rawMotorData[1],
                                                            rawMotorData[2])
            print("Zero Position set.")
            return pos, vel, curr
        except Exception as e:
            print('Error Setting Zero Position!')
            print("Error: ", e)

    def decode_motor_status(self, data_frame):
        '''
        Function to decode the motor status reply message into its constituent raw values.

        /// CAN Reply Packet Structure ///
        /// 16 bit position, between -4*pi and 4*pi
        /// 12 bit velocity, between -30 and + 30 rad/s
        /// 12 bit current, between -40 and 40;
        /// CAN Packet is 5 8-bit words
        /// Formatted as follows.  For each quantity, bit 0 is LSB
        /// 0: [position[15-8]]
        /// 1: [position[7-0]]
        /// 2: [velocity[11-4]]
        /// 3: [velocity[3-0], current[11-8]]
        /// 4: [current[7-0]]

        returns: the following raw values as (u)int: position, velocity, current
        '''

        # Convert the message from motor to a bit string as this is easier to deal with than hex
        # while seperating individual values.
        self._recv_bytes.bytes = data_frame
        dataBitArray = self._recv_bytes.bin

        # Separate motor satus values from the bit string.
        # Motor ID not considered necessary at the moment.
        # motor_id = dataBitArray[:8]
        positionBitArray = dataBitArray[8:24]
        velocityBitArray = dataBitArray[24:36]
        currentBitArray = dataBitArray[36:48]

        # motor_id = int(motor_id, 2)
        positionRawValue = int(positionBitArray, 2)
        velocityRawValue = int(velocityBitArray, 2)
        currentRawValue = int(currentBitArray, 2)

        # TODO: Is it necessary/better to return motor_id?
        # return motor_id, positionRawValue, velocityRawValue, currentRawValue
        return positionRawValue, velocityRawValue, currentRawValue

    def convert_raw_to_physical_rad(self, positionRawValue, velocityRawValue, currentRawValue):
        '''
        Function to convert the raw values from the motor to physical values:

        /// CAN Reply Packet Structure ///
        /// 16 bit position, between -4*pi and 4*pi
        /// 12 bit velocity, between -30 and + 30 rad/s
        /// 12 bit current, between -40 and 40;
        /// CAN Packet is 5 8-bit words
        /// Formatted as follows.  For each quantity, bit 0 is LSB
        /// 0: [position[15-8]]
        /// 1: [position[7-0]]
        /// 2: [velocity[11-4]]
        /// 3: [velocity[3-0], current[11-8]]
        /// 4: [current[7-0]]

        returns: position (radians), velocity (rad/s), current (amps)
        '''

        physicalPositionRad = uint_to_float(positionRawValue, P_MIN, P_MAX, 16)
        physicalVelocityRad = uint_to_float(velocityRawValue, V_MIN, V_MAX, 12)
        physicalCurrent = uint_to_float(currentRawValue, T_MIN, T_MAX, 12)

        return physicalPositionRad, physicalVelocityRad, physicalCurrent

    def convert_raw_to_physical_deg(self, positionRawValue, velocityRawValue, currentRawValue):
        '''
        Function to convert the raw values from the motor to physical values:

        /// CAN Reply Packet Structure ///
        /// 16 bit position, between -4*pi and 4*pi
        /// 12 bit velocity, between -30 and + 30 rad/s
        /// 12 bit current, between -40 and 40;
        /// CAN Packet is 5 8-bit words
        /// Formatted as follows.  For each quantity, bit 0 is LSB
        /// 0: [position[15-8]]
        /// 1: [position[7-0]]
        /// 2: [velocity[11-4]]
        /// 3: [velocity[3-0], current[11-8]]
        /// 4: [current[7-0]]

        returns: position (degrees), velocity (deg/s), current (amps)
        '''

        physicalPositionRad, physicalVelocityRad, physicalCurrent = \
            self.convert_raw_to_physical_rad(positionRawValue, velocityRawValue, currentRawValue)

        physicalPositionDeg = math.degrees(physicalPositionRad)
        physicalVelocityDeg = math.degrees(physicalVelocityRad)

        return physicalPositionDeg, physicalVelocityDeg, physicalCurrent

    def convert_physical_deg_to_raw(self, p_des_deg, v_des_deg, kp, kd, tau_ff):
        '''
        /// CAN Command Packet Structure ///
        /// 16 bit position command, between -4*pi and 4*pi
        /// 12 bit velocity command, between -30 and + 30 rad/s
        /// 12 bit kp, between 0 and 500 N-m/rad
        /// 12 bit kd, between 0 and 100 N-m*s/rad
        /// 12 bit feed forward torque, between -18 and 18 N-m
        /// CAN Packet is 8 8-bit words
        /// Formatted as follows.  For each quantity, bit 0 is LSB
        /// 0: [position[15-8]]
        /// 1: [position[7-0]]
        /// 2: [velocity[11-4]]
        /// 3: [velocity[3-0], kp[11-8]]
        /// 4: [kp[7-0]]
        /// 5: [kd[11-4]]
        /// 6: [kd[3-0], torque[11-8]]
        /// 7: [torque[7-0]]
        '''
        position = math.radians(p_des_deg)
        velocity = math.radians(v_des_deg)

        rawPosition = float_to_uint(position, P_MIN, P_MAX, 16)
        rawVelocity = float_to_uint(velocity, V_MIN, V_MAX, 12)
        rawTorque = float_to_uint(tau_ff, T_MIN, T_MAX, 12)

        rawKp = ((maxRawKp * kp) / KP_MAX)

        rawKd = ((maxRawKd * kd) / KD_MAX)

        return int(rawPosition), int(rawVelocity), int(rawKp), int(rawKd), int(rawTorque)

    def convert_physical_rad_to_raw(self, p_des_rad, v_des_rad, kp, kd, tau_ff):

        rawPosition = float_to_uint(p_des_rad, P_MIN, P_MAX, 16)
        rawVelocity = float_to_uint(v_des_rad, V_MIN, V_MAX, 12)
        rawTorque = float_to_uint(tau_ff, T_MIN, T_MAX, 12)

        rawKp = ((maxRawKp * kp) / KP_MAX)

        rawKd = ((maxRawKd * kd) / KD_MAX)

        return int(rawPosition), int(rawVelocity), int(rawKp), int(rawKd), int(rawTorque)

    def _send_raw_command(self, p_des, v_des, kp, kd, tau_ff):
        """
        Package and send raw (uint) values of correct length to the motor.

        _send_raw_command(desired position, desired velocity, position gain, velocity gain,
                        feed-forward torque)

        Sends data over CAN, reads response, and returns the motor status data (in bytes).
        """
        self._p_des_BitArray.uint = p_des
        self._v_des_BitArray.uint = v_des
        self._kp_BitArray.uint = kp
        self._kd_BitArray.uint = kd
        self._tau_BitArray.uint = tau_ff
        cmd_BitArray = self._p_des_BitArray.bin + self._v_des_BitArray.bin + self._kp_BitArray.bin \
                        + self._kd_BitArray.bin + self._tau_BitArray.bin

        self._cmd_bytes.bin = cmd_BitArray

        try:
            self._send_can_frame(self._cmd_bytes.tobytes())
            waitOhneSleep(dt_sleep)
            can_id, can_dlc, data = self._recv_can_frame()
            return data
        except Exception as e:
            print('Error Sending Raw Commands!')
            print("Error: ", e)

    def send_deg_command(self, p_des_deg, v_des_deg, kp, kd, tau_ff):
        """
        TODO: Add assert statements to validate input ranges.
        Function to send data to motor in physical units:
        send_deg_command(position (deg), velocity (deg/s), kp, kd, Feedforward Torque (Nm))
        Sends data over CAN, reads response, and prints the current status in deg, deg/s, amps.
        """
        rawPos, rawVel, rawKp, rawKd, rawTauff = self.convert_physical_deg_to_raw(p_des_deg,
                                                                v_des_deg, kp, kd, tau_ff)

        motorStatusData = self._send_raw_command(rawPos, rawVel, rawKp, rawKd, rawTauff)
        rawMotorData = self.decode_motor_status(motorStatusData)
        pos, vel, curr = self.convert_raw_to_physical_deg(rawMotorData[0], rawMotorData[1],
                                                            rawMotorData[2])
        return pos, vel, curr

    def send_rad_command(self, p_des_rad, v_des_rad, kp, kd, tau_ff):
        """
        TODO: Add assert statements to validate input ranges.
        Function to send data to motor in physical units:
        send_rad_command(position (rad), velocity (rad/s), kp, kd, Feedforward Torque (Nm))
        Sends data over CAN, reads response, and prints the current status in rad, rad/s, amps.
        """
        rawPos, rawVel, rawKp, rawKd, rawTauff = self.convert_physical_rad_to_raw(p_des_rad,
                                                                v_des_rad, kp, kd, tau_ff)

        motorStatusData = self._send_raw_command(rawPos, rawVel, rawKp, rawKd, rawTauff)
        rawMotorData = self.decode_motor_status(motorStatusData)
        pos, vel, curr = self.convert_raw_to_physical_rad(rawMotorData[0], rawMotorData[1],
                                                            rawMotorData[2])
        return pos, vel, curr

    def change_motor_constants(self, P_MIN_NEW, P_MAX_NEW, V_MIN_NEW, V_MAX_NEW, KP_MIN_NEW,
                            KP_MAX_NEW, KD_MIN_NEW, KD_MAX_NEW, T_MIN_NEW, T_MAX_NEW):
        """
        Function to change the global motor constants. Default values are for AK80-6 motor from
        CubeMars. For a differnt motor, the min/max values can be changed here for correct
        conversion.
        change_motor_params(P_MIN_NEW (radians), P_MAX_NEW (radians), V_MIN_NEW (rad/s),
                            V_MAX_NEW (rad/s), KP_MIN_NEW, KP_MAX_NEW, KD_MIN_NEW, KD_MAX_NEW,
                            T_MIN_NEW (Nm), T_MAX_NEW (Nm))
        """
        global P_MIN, P_MAX, V_MIN, V_MAX, KP_MIN, KP_MAX, KD_MIN, KD_MAX, T_MIN, T_MAX
        P_MIN = P_MIN_NEW
        P_MAX = P_MAX_NEW
        V_MIN = V_MIN_NEW
        V_MAX = V_MAX_NEW
        KP_MIN = KP_MIN_NEW
        KP_MAX = KP_MAX_NEW
        KD_MIN = KD_MIN_NEW
        KD_MAX = KD_MAX_NEW
        T_MIN = T_MIN_NEW
        T_MAX = T_MAX_NEW
