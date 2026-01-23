import mysql.connector

# -------------------------------
# MySQL connection
# -------------------------------
DB_HOST = '192.168.1.14'      # Replace with your PC LAN IP
DB_USER = 'kiosk_user'        # MySQL user
DB_PASSWORD = 'Components'    # MySQL password
DB_NAME = 'component_db'

conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()

# -------------------------------
# Create database if not exists
# -------------------------------
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
cursor.execute(f"USE {DB_NAME}")

# -------------------------------
# Drop tables if they exist (foreign key safe)
# -------------------------------
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
tables = ['logs', 'loans', 'components', 'users']
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# -------------------------------
# Create tables
# -------------------------------
cursor.execute('''
CREATE TABLE components (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    image VARCHAR(255),
    datasheet VARCHAR(255),
    type VARCHAR(255) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    student_number VARCHAR(20) NOT NULL UNIQUE,
    role VARCHAR(20) DEFAULT 'student'
)
''')

cursor.execute('''
CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    component_id INT,
    quantity INT,
    timestamp DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(component_id) REFERENCES components(id) ON DELETE CASCADE
)
''')

cursor.execute('''
CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    item VARCHAR(255),
    returned BOOLEAN DEFAULT 0,
    loan_date DATETIME,
    return_date DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
)
''')

# -------------------------------
# Insert components (only if not exists)
# -------------------------------
components = [
    ('NE555', 'Timer IC used for generating precise time delays.', 'ne555.jpg', 'datasheets/ne555.pdf', 'Timer IC'),
    ('LM741', 'Operational amplifier widely used in analog circuits.', 'lm741.jpg', 'datasheets/lm741.pdf', 'Operational Amplifier'),
    ('LM7805', '5V positive voltage regulator.', 'lm7805.jpg', 'datasheets/lm7805.pdf', 'Voltage Regulator'),
    ('LM7905', '5V negative voltage regulator.', 'lm7905.jpg', 'datasheets/lm7905.pdf', 'Voltage Regulator'),
    ('LM7812', '12V positive voltage regulator.', 'lm7812.jpg', 'datasheets/lm7812.pdf', 'Voltage Regulator'),
    ('LM7912', '12V negative voltage regulator.', 'lm7912.jpg', 'datasheets/lm7912.pdf', 'Voltage Regulator'),
    ('LM 3V REGULATOR', '3V voltage regulator for low voltage circuits.', 'lm3v.jpg', 'datasheets/lm3v.pdf', 'Voltage Regulator'),
    ('LM7909', '9V negative voltage regulator.', 'lm7909.jpg', 'datasheets/lm7909.pdf', 'Voltage Regulator'),
    ('LM7809', '9V positive voltage regulator.', 'lm7809.jpg', 'datasheets/lm7809.pdf', 'Voltage Regulator'),
    ('BC237', 'NPN general-purpose transistor.', 'bc237.jpg', 'datasheets/bc237.pdf', 'Transistor'),
    ('BC337', 'NPN transistor for switching and amplification.', 'bc337.jpg', 'datasheets/bc337.pdf', 'Transistor'),
    ('2N2219', 'NPN transistor used in general purpose amplification.', '2n2219.jpg', 'datasheets/2n2219.pdf', 'Transistor'),
    ('2N2905', 'PNP transistor for amplification and switching.', '2n2905.jpg', 'datasheets/2n2905.pdf', 'Transistor'),
    ('BC547', 'NPN transistor used in low power amplification.', 'bc547.jpg', 'datasheets/bc547.pdf', 'Transistor'),
    ('BC557', 'PNP transistor for low power amplification.', 'bc557.jpg', 'datasheets/bc557.pdf', 'Transistor'),
    ('TIP31', 'NPN power transistor for switching.', 'tip31.jpg', 'datasheets/tip31.pdf', 'Transistor'),
    ('TIP32', 'PNP power transistor for switching.', 'tip32.jpg', 'datasheets/tip32.pdf', 'Transistor'),
    ('TIP 3055', 'High power NPN transistor.', 'tip3055.jpg', 'datasheets/tip3055.pdf', 'Transistor'),
    ('TIP 2955', 'High power PNP transistor.', 'tip2955.jpg', 'datasheets/tip2955.pdf', 'Transistor'),
    ('BUK455', 'Power MOSFET transistor.', 'buk455.jpg', 'datasheets/buk455.pdf', 'Transistor'),
    ('MOC3041', 'Optocoupler for TRIAC triggering.', 'moc3041.jpg', 'datasheets/moc3041.pdf', 'Optocoupler'),
    ('MOC3021', 'Optocoupler used for isolation.', 'moc3021.jpg', 'datasheets/moc3021.pdf', 'Optocoupler'),
    ('BT139', 'TRIAC used for AC power control.', 'bt139.jpg', 'datasheets/bt139.pdf', 'TRIAC'),
    ('BT136', 'TRIAC for power switching.', 'bt136.jpg', 'datasheets/bt136.pdf', 'TRIAC'),
    ('35M0630', 'Dip Switch 3 pole.', '35m0630.jpg', 'datasheets/35m0630.pdf', 'Switch'),
    ('TACT SWITCHES 5MM', 'Momentary push button switches.', 'tact_switch_5mm.jpg', '', 'Switch'),
    ('TOGGLE DPDT', 'Double pole double throw toggle switch.', 'toggle_dpdt.jpg', '', 'Switch'),
    ('TOGGLE SPST', 'Single pole single throw toggle switch.', 'toggle_spst.jpg', '', 'Switch'),
    ('14M1006', '2 Pin Tactile Switch.', '14m1006.jpg', 'datasheets/14m1006.pdf', 'Switch'),
    ('14M8977', 'Mini Micro Limit Switch SPDT Lever.', '14m8977.jpg', '', 'Switch'),
    ('VOL CONTROL POTS: 1K', 'Variable resistor, 1 kilo-ohm.', 'pot_1k.jpg', 'datasheets/pot_1k.pdf', 'Potentiometer'),
    ('VOL CONTROL POTS: 5K', 'Variable resistor, 5 kilo-ohms.', 'pot_5k.jpg', 'datasheets/pot_5k.pdf', 'Potentiometer'),
    ('VOL CONTROL POTS: 10K', 'Variable resistor, 10 kilo-ohms.', 'pot_10k.jpg', 'datasheets/pot_10k.pdf', 'Potentiometer'),
    ('VOL CONTROL POTS: 100K', 'Variable resistor, 100 kilo-ohms.', 'pot_100k.jpg', 'datasheets/pot_100k.pdf', 'Potentiometer'),
    ('LED RED 5MM', 'Red LED indicator, 5mm size.', 'led_red_5mm.jpg', '', 'LED'),
    ('LED GREEN 5MM', 'Green LED indicator, 5mm size.', 'led_green_5mm.jpg', '', 'LED'),
    ('LED YELLOW 5MM', 'Yellow LED indicator, 5mm size.', 'led_yellow_5mm.jpg', '', 'LED'),
    ('14M1010', 'PCB Tactile SWITCH.', '14m1010.jpg', '', 'Switch'),
    ('IN4148', 'Fast switching diode.', 'in4148.jpg', 'datasheets/in4148.pdf', 'Diode'),
    ('IN4007', 'High voltage rectifier diode.', 'in4007.jpg', 'datasheets/in4007.pdf', 'Diode'),
    ('RELAY 5V', '5 Volt electromagnetic relay.', 'relay_5v.jpg', 'datasheets/relay_5v.pdf', 'Relay'),
    ('RELAY 12V', '12 Volt electromagnetic relay.', 'relay_12v.jpg', 'datasheets/relay_12v.pdf', 'Relay')
]

cursor.executemany(
    "INSERT INTO components (name, description, image, datasheet, type) VALUES (%s, %s, %s, %s, %s)",
    components
)

# -------------------------------
# Add admin user (if not exists)
# -------------------------------
cursor.execute("SELECT * FROM users WHERE student_number = %s", ("000000000",))
if cursor.fetchone() is None:
    cursor.execute(
        "INSERT INTO users (name, student_number, role) VALUES (%s, %s, %s)",
        ("Admin User", "000000000", "admin")
    )

conn.commit()
cursor.close()
conn.close()

print("MySQL database initialized and ready for multiple kiosks.")
