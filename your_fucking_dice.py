import math, os, time, random, pyfiglet

random_number = random.randint(1, 6)
number1, number2, number3 = 4.9, 6.2, 11
number4, number5, number6 = 21.2, 8.5, 30
start_time = time.time()

duration = {
    1: number1, 2: number2, 3: number3,
    4: number4, 5: number5, 6: number6
}[random_number]

A = B = C = 0
w, h = 160, 40
K1, cube_size, dist_cam = 40, 20, 100
inc_speed = 0.6
bg_char = '_'

def rotate(i, j, k):
    sinA, cosA = math.sin(A), math.cos(A)
    sinB, cosB = math.sin(B), math.cos(B)
    sinC, cosC = math.sin(C), math.cos(C)
    
    x = j*sinA*sinB*cosC - k*cosA*sinB*cosC + j*cosA*sinC + k*sinA*sinC + i*cosB*cosC
    y = j*cosA*cosC + k*sinA*cosC - j*sinA*sinB*sinC + k*cosA*sinB*sinC - i*cosB*sinC
    z = k*cosA*cosB - j*sinA*cosB + i*sinB + dist_cam
    return x, y, z

def render():
    z_buf = [0] * (w * h)
    buf = [bg_char] * (w * h)
    half_w, half_h = w // 2, h // 2

    offset = 10

    face_numbers = {
        '▥': 1,  # back
        '▦': 2,  # right
        '▧': 3,  # left
        '▨': 4,  # front
        '▩': 5,  # bottom
        '▤': 6   # top
    }

    for x in frange(-cube_size, cube_size, inc_speed):
        for y in frange(-cube_size, cube_size, inc_speed):
            for i, j, k, ch in [
                (x, y, -cube_size, '▥'),
                (cube_size, y, x, '▦'),
                (-cube_size, y, -x, '▧'),
                (-x, y, cube_size, '▨'),
                (x, -cube_size, -y, '▩'),
                (x, cube_size, y, '▤')
            ]: #............................. this tiny part is mostly made  by chatgpt (hard asf)
                xr, yr, zr = rotate(i, j, k) #  applies 3D rotation to the point 
                ooz = 1 / zr #  simulates perspective
                xp = int(half_w + offset + K1 * ooz * xr * 2) #converts 3d point to 2d screen coordinates
                yp = int(half_h + K1 * ooz * yr)  
                idx = xp + yp * w 
                if 0 <= idx < w * h and ooz > z_buf[idx]:
                    z_buf[idx] = ooz # updates the z-buffer and puts the face character ▦,▩ etc...
                    buf[idx] = ch
                    if -4 < x < 4 and -4 < y < 4:
                        buf[idx] = str(face_numbers[ch]) # overwrite the center characters with a number

    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n'.join(''.join(buf[i:i + w]) for i in range(0, w * h, w)))

def frange(start, stop, step):
    while start < stop:
        yield start
        start += step

def main():
    global A, B, C
    while time.time() - start_time < duration:
        render()
        A += 0.04 # X-axis
        B += 0.05 # Y-axis
        if B >= 2 * math.pi:
            B = 0
        C += 0.02 # Z-axis
        time.sleep(0.016)

if __name__ == "__main__":
    print(f"Random number chosen: {random_number}")
    main()
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')
    ascii_art = pyfiglet.figlet_format(str(random_number))
    print("Your number is:")
    print(ascii_art)
