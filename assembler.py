import struct

instruction_set = {
    "JMP": 0x0,
    "ADC": 0x1,
    "XOR": 0x2,
    "SBC": 0x3,
    "ROR": 0x4,
    "TAT": 0x5,
    "OR": 0x6,
    "ILL": 0x7,
    "AND": 0x8,
    "LDC": 0x9,
    "BCC": 0xA,
    "BNE": 0xB,
    "LDI": 0xC,
    "STT": 0xD,
    "LDA": 0xE,
    "STA": 0xF,
}

MAX_PROGRAM_SIZE = 0x1000

variables = {}

memory = bytearray()
program = bytearray()

instruction_num = 0

def parse_data(line):
	global memory
	global program
	global instruction_num
	parts = line.strip().split()
	name = parts[0]
	addr = instruction_num * 2 + (len(variables) * 2)
	variables[name] = addr
	value = int(parts[1], 16) & 0xFFFF
	memory += value.to_bytes(2, 'little')

def parse_instruction(line):
    parts = line.strip().split()
    if len(parts) == 1:
        opcode = instruction_set.get(parts[0], None)
        return opcode, None
    elif len(parts) == 2:
        opcode = instruction_set.get(parts[0], None)
        operand = variables[parts[1]]
        return opcode, operand

def generate_program(filename):
	global memory
	global program
	global instruction_num
	in_data = True
	file = open(filename, "r")
	lines = file.readlines()
	instruction_num = len(lines) - lines.index("section .text:\n") - 1
	print(instruction_num)
	for line in lines:
		line = line.rstrip()
		if line == "section .data:":
			continue
		elif line == "section .text:":
			in_data = False
			continue
		elif in_data: 
			parse_data(line)
		else:
			opcode, operand = parse_instruction(line)

			if operand is not None:
				instruction = (opcode << 12) | (operand & 0xFFF)
			else:
				instruction = opcode << 12

			inst_bytes = struct.pack('<H', instruction)

			program += inst_bytes

	return program + memory + bytearray(MAX_PROGRAM_SIZE - len(program) - len(memory))

def save_program_to_file(program, filename="program.bin"):
    with open(filename, "wb") as f:
        f.write(program)

def print_program_in_hex(program):
	print(f"Program in hex:")
	print(f"Program length: {len(program)}")
	for i in range(0, len(program), 16):
		print(" ".join(f"{byte:02X}" for byte in program[i:i+16]))

if __name__ == "__main__":
	filename = "program.asm"

	program = generate_program(filename)

	print_program_in_hex(program)

	save_program_to_file(program)
	print(f"Program saved to 'program.bin'.")
