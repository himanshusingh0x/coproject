import sys
OPCODES = {"add":"0110011","sub": "0110011","sll": "0110011","sltiu":"0010011","bltu":"1100011","bgeu":"1100011","slt": "0110011","sltu": "0110011","xor": "0110011","srl": "0110011","or": "0110011","and": "0110011","addi": "0010011","lw": "0000011","sltiu": "0010011","jalr": "1100111","sw": "0100011","beq": "1100011","bne": "1100011","blt": "1100011","bge": "1100011","lui": "0110111","auipc": "0010111","jal":"1101111",}
REGISTERS = {"zero": "00000","gp":"00011","tp":"00100","ra": "00001","sp": "00010","t0": "00101","t1": "00110","t2": "00111","s0": "01000","fp": "01000","s1": "01001","a0" : "01010","a1": "01011","a2": "01100","a3": "01101","a4": "01110","a5": "01111","a6": "10000","a7": "10001","s2": "10010","s3": "10011","s4": "10100","s5": "10101","s6": "10110","s7": "10111","s8": "11000","s9": "11001","s10": "11010","s11": "11011","t3": "11100","t4": "11101","t5": "11110","t6": "11111",}

def num_to_binary(num, length):
    if num < 0:
        num = (1 << length) + num
    return format(num, '0' + str(length) + 'b') 

labels = {}


def return_labels(line, labels, jc):
    parts = line.strip().split()
    if not parts or parts[0].startswith('#'):
        return None
    if parts [0][-1] == ':':
        labels[parts[0][:-1]] = jc


def parse_ins(line, labels, pc, LN):
    parts = line.strip().split() 
    
    if not parts or parts[0].startswith('#'):
        return None, None
    
    if parts[0][-1] == ':':
        
        if len(parts) == 1:
            return None, None
        
        parts = parts[1:]       
    inst = parts[0]

    if inst not in OPCODES:
        return f"Error at line {LN}: Unknown inst '{inst}'", None
    
    opcode = OPCODES[inst]
    
    if len(parts) > 1:

        registers = parts[1].split(',') 
        if inst in ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and"]:
            if len(registers) != 3:
                return f"Error at line {LN}: Wrong number of registers for '{inst}'", None
            
            rd = registers[0].strip()
            if rd not in REGISTERS:
                return f"Error at line {LN}: Unknown register '{rd}'", None
            
            rs1 = registers[1].strip()
            if rs1 not in REGISTERS:
                return f"Error at line {LN}: Unknown register '{rs1}'", None
            
            rs2 = registers[2].strip()
            if rs2 not in REGISTERS:
                return f"Error at line {LN}: Unknown register '{rs2}'", None
            if inst == "sub":
                funct7 = "0100000"  
            else:
                funct7 = "0000000" 
            funct3 = {"add":'000', "sub":"000", "sll":"001", "slt":'010', "sltu":'011', "xor":'100', "srl":'101', "or":'110', "and":'111'}
            instruction = f"{funct7}{REGISTERS[rs2]}{REGISTERS[rs1]}{funct3[inst]}{REGISTERS[rd]}{opcode}"
        elif inst == "addi":
            if len(registers) != 3:
                return f"Error at line {LN}: Wrong number of registers for '{inst}'", None
            rd = registers[0].strip()
            if rd not in REGISTERS:
                return f"Error at line {LN}: Unknown register '{rd}'", None
            rs1 = registers[1].strip()
            if rs1 not in REGISTERS:
                return f"Error at line {LN}: Unknown register '{rs1}'", None
            try:
                immediate = int(registers[2].strip())
            except ValueError:
                return f"Error at line {LN}: Invalid immediate value '{registers[2].strip()}'", None
            if not (-2048 <= immediate < 2048):
                return f"Error at line {LN}: Immediate value out of bounds '{registers[2].strip()}'", None
            immediate_binary = num_to_binary(immediate,12)
            funct3 = "000"
            instruction = f"{immediate_binary}{REGISTERS[rs1]}{funct3}{REGISTERS[rd]}{opcode}"
        elif inst == "sltiu":
            if len(registers) != 3:
                return f"Error at line {LN}: Wrong number of registers for '{inst}'", None
            rd = registers[0].strip()
            if rd not in REGISTERS:
                return f"Error at line {LN}: Unknown register '{rd}'", None
            rs1 = registers[1].strip()

            if rs1 not in REGISTERS:
                return f"Error at line {LN}: Unknown register '{rs1}'", None
            
            try:
                immediate = int(registers[2].strip())

            except ValueError:
                return f"Error at line {LN}: Invalid immediate value '{registers[2].strip()}'", None
            
            if not (-2048 <= immediate < 2048):
                return f"Error at line {LN}: Immediate value out of bounds '{registers[2].strip()}'", None
            
            immediate_binary = num_to_binary(immediate,12)
            
            funct3 = "011"
            instruction = f"{immediate_binary}{REGISTERS[rs1]}{funct3}{REGISTERS[rd]}{opcode}" 
        
        elif inst == "lw":
            if len(registers) != 2:
                return f"Error at line {LN}: Wrong number of registers for '{inst}'", None
            
            rd = registers[0].strip()
            if rd not in REGISTERS:
                return f"Error at line {LN}: Unknown register '{rd}'", None
            try:
                immediate, rs1_offset = map(str.strip, registers[1].split('('))
                immediate = int(immediate)  
                rs1 = rs1_offset.strip(')')
            except ValueError:
                return f"Error at line {LN}: invalid immediate value or register '{registers[1]}'", None
            
            if not (-2048 <= immediate < 2048):
                return f"Error at line {LN}: immediate value out of bounds '{registers[1]}'", None
            
            immediate_binary = num_to_binary(immediate,12)
            
            funct3 = "010"
    
            instruction = f"{immediate_binary}{REGISTERS[rs1]}{funct3}{REGISTERS[rd]}{opcode}"
        
        elif inst == "jalr":
            if len(registers) != 3:
                return f"Error at line {LN}: Wrong number of registers for '{inst}'", None
         
            rd = registers[0].strip()
            if rd not in REGISTERS:
                return f"Error at line {LN}: Unknown register '{rd}'", None
            
            rs1 = registers[1].strip()
            if rs1 not in REGISTERS:
                return f"Error at line {LN}: Unknown register '{rs1}'", None
            try:
                immediate = int(registers[2].strip())  
            except ValueError:
                return f"Error at line {LN}: invalid immediate value '{registers[2].strip()}'", None
        
            if not (-2048 <= immediate < 2048):
                return f"Error at line {LN}: immediate value out of bounds '{registers[2].strip()}'", None
         
            immediate_binary = num_to_binary(immediate,12)
       
            funct3 = "000"
            
            instruction = f"{immediate_binary}{REGISTERS[rs1]}{funct3}{REGISTERS[rd]}{opcode}"
        
        elif inst == "sw":
            if len(registers)!=2:
                return f"error at line {LN}: wrong number of registers for'{inst}'",None
            rd = registers[0].strip()
            if rd not in REGISTERS:
                return f"error at line {LN}:unkown register '{rd}'",None
            try:
                immediate,rs1_offset = map(str.strip,registers[1].split('('))
                immediate = int(immediate)
                rs1 = rs1_offset.strip(')')
            except ValueError:
                return f"error at line {LN}: invalid immediate value or register'{registers[1]}'",None
            if not(-2048<=immediate<2048):
                return f"error at line {LN}: immediate value out of bounds '{registers[1]}'",None
            immediate_binary = num_to_binary(immediate,12)
            funct3 = "010"
            instruction = f"{immediate_binary[0:7]}{REGISTERS[rd]}{REGISTERS[rs1]}{funct3}{immediate_binary[7:]}{opcode}" 
        
        elif inst in ['blt', 'beq', 'bne', 'bge', 'bltu', 'bgeu']:
            if len(registers)!=3:
                return f"error at line {LN}: wrong syntax",None
            rd = registers[0].strip()
            if rd not in registers:
                return f"error at line {LN}: wrong syntax",None
            rs1 = registers[1].strip()
            if rs1 not in registers:
                return f"error att line {LN}: unkown register",None
            if any(part in labels for part in registers):
                imm_label = next((part for part in registers if part in labels), None)
                imm_address = labels[imm_label]
                immediate = pc - imm_address
            else:
                try:
                    immediate = int(registers[2].strip())
                except ValueError:
                    return f"error at line {LN}: wrong immediate value",None
            if not (-2048 <= immediate<2048):
                return f"error at line {LN}: not in range",None
            immediate_binary = num_to_binary(immediate,12)
            funct3={"blt":"100","beq":"000","bne":"001","bge":"101","bltu":"110","bgeu":"111"}
            instruction = f"{immediate_binary[0:7]}{REGISTERS[rs1]}{REGISTERS[rd]}{funct3[inst]}{immediate_binary[7:]}{opcode}"
        elif inst == "jal":
            if len(registers)!=2:
                return f"error at line {LN}: wrong syntax please check again",None
            rd  = registers[0].strip()
            if rd not in REGISTERS:
                return f"error at line {LN}: unknown register",None
            if any(part in labels for part in registers):
                imm_label = next((part for part in registers if part in labels), None)
                imm_address = labels[imm_label]
                immediate = pc - imm_address
            else:
                try:
                    immediate = int(registers[1].strip())
                except ValueError:
                    return f"error at line {LN}: wrong immediate value",None
            if not(-2**19<= immediate <(2**19 + 1)):
                return f"error at line {LN}: immediate value out of range",None
            immediate_binary = num_to_binary(immediate,20)
            instruction = f"{immediate_binary[8:19]}{immediate_binary[0:9]}{REGISTERS[rd]}{opcode}"
        
        elif inst in ["lui","auipc"]:         
            if len(registers)!=2:
                return f"error at line {LN} : wrong syntax",None
            rd = registers[0].strip()
            if rd not in REGISTERS:
                return f"error at line {LN} : unknown register",None
            try:
                immediate = int(registers[1].strip())
            except ValueError:
                return f"error at line {LN}: invalid immediate",None
            if not(-2**31<= immediate <(2**31 + 1)):
                return f"error at line {LN}: immediate value out of range",None
            immediate_binary = num_to_binary(immediate,32)
            instruction = f"{immediate_binary[0:20]}{REGISTERS[rd]}{opcode}"
          
        else: 
            return f"Error at line {LN}: Unsupported inst '{inst}'",None
    else:
        return f"Error at line {LN}: No registers specified for '{inst}'",None

    return None,instruction


def ASM(assemblycode):
    BC = []
    pc = 4
    jc = 4
    for LN, line in enumerate(assemblycode):
        line = line.strip()
        if not line or line.startswith('#'):  
            continue
        return_labels(line, labels, jc)
        jc += 4
    for LN, line in enumerate(assemblycode):
        line = line.strip()
        if not line or line.startswith('#'):  
            continue
        error, instruction = parse_ins(line, labels, pc, LN)
        if error:
            return f"Error at line {LN+1}: {error}", None
        
        if instruction is None:
            continue
        BC.append(instruction)
        pc += 4
    
    if BC[-1]=="00000000000000000000000001100011":
        return None, BC
    else:
        return f"error no virtual halt given",None
    




def main(input_file, output_file):
    with open(input_file, 'r') as f:
        assemblycode = f.readlines()

    error, binarycode = ASM(assemblycode)

    if error:
        print(error)
        sys.exit(1)
    else:
        with open(output_file, 'w') as f1:
            for i in binarycode:
                f1.write(i + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Assembler.py <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)

