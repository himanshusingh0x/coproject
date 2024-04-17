from itertools import islice

import sys


if len(sys.argv) != 3:
    print("Usage: python Simulator.py <input_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]


def int_to_twos_complement(value, bit_width):

    if value < 0:
        value = (1 << bit_width) + value
    
    binary_string = format(value, 'b').zfill(bit_width)
    
    return binary_string


memory = [0] * 70000

mem = {
    "0x00010000": 0,
    "0x00010004": 0,
    "0x00010008": 0,
    "0x0001000c": 0,
    "0x00010010": 0,
    "0x00010014": 0,
    "0x00010018": 0,
    "0x0001001c": 0,
    "0x00010020": 0,
    "0x00010024": 0,
    "0x00010028": 0,
    "0x0001002c": 0,
    "0x00010030": 0,
    "0x00010034": 0,
    "0x00010038": 0,
    "0x0001003c": 0,
    "0x00010040": 0,
    "0x00010044": 0,
    "0x00010048": 0,
    "0x0001004c": 0,
    "0x00010050": 0,
    "0x00010054": 0,
    "0x00010058": 0,
    "0x0001005c": 0,
    "0x00010060": 0,
    "0x00010064": 0,
    "0x00010068": 0,
    "0x0001006c": 0,
    "0x00010070": 0,
    "0x00010074": 0,
    "0x00010078": 0,
    "0x0001007c": 0,
}


with open(output_file,"w") as f:
    pass
def write_in_file(filename,data):
    with open(filename,"a") as f:
        f.writelines(data)
        f.write("\n")
def shift_left(rs1, rs2):
    shift_amount = rs2 & 0x1F  
    return rs1 << shift_amount

def shift_right(rs1, rs2):
    shift_amount = rs2 & 0x1F 
    return rs1 >> shift_amount  

def to_bin(n):
    binary_string = bin(n)[2:]
    padded_binary_string = binary_string.zfill(32)
    return ("0b" + padded_binary_string)

def print_values(num, o_dict):
    lf = []
    a = "0b" + int_to_twos_complement(num, 32) + " "
    lf.append(a)
    subset_dict = dict(islice(o_dict.items(), 0, 32))
    for i in subset_dict:
        b = "0b" + int_to_twos_complement(subset_dict[i], 32) + " "
        lf.append(b)
    write_in_file(output_file,lf)

def sign_extend_binary_to_int(binary_str, total_bits):
    # Convert binary string to integer
    value = int(binary_str, 2)

    # Check if the number is negative in two's complement
    if value & (1 << (total_bits - 1)):
        # Perform sign extension
        value -= 1 << total_bits

    return value


op_codes = {'zero' : '00000', 'ra' : '00001', 'sp' : '00010', 'gp' : '00011', 'tp' : '00100', 't0' : '00101', 't1' : '00110', 't2' : '00111', 
            's0' : '01000', 's1' : '01001', 'a0' : '01010', 'a1' : '01011', 'a2' : '01100', 'a3' : '01101', 
            'a4' : '01110', 'a5' : '01111', 'a6' : '10000', 'a7' : '10001', 's2' : '10010', 's3' : '10011', 's4' : '10100', 
            's5' : '10101', 's6' : '10110', 's7' : '10111', 's8' : '11000', 's9' : '11001', 's10': '11010', 's11' :'11011', 
            't3' : '11100', 't4' : '11101', 't5' : '11110', 't6' : '11111' }

reversed_op_codes = {v: k for k, v in op_codes.items()}

registors = {'zero' : 0,'ra' : 0, 'sp' : 256, 'gp' : 0, 'tp' : 0, 't0' : 0, 't1' : 0, 't2' : 0, 's0' : 0, 's1' : 0, 'a0' : 0, 'a1' : 0,
             'a2': 0, 'a3' : 0, 'a4' : 0, 'a5' : 0, 'a6' : 0, 'a7' : 0, 's2' : 0, 's3' : 0, 's4' : 0, 's5' : 0, 's6' : 0,
             's7' : 0, 's8' : 0, 's9' : 0, 's10' : 0, 's11' : 0, 't3' : 0, 't4' : 0, 't5' : 0, 't6' : 0}



PC = 0

#0000000,00000,00000,000,01001,0110011
#f7      rs2   rs1   f3  rd    opcode
def instruction_stats(PC,lines, i):
            

    if (i[25:32] == '0110011'): 
        if(i[17:20] == '000'):
            if(i[0:7] == '0000000'): #add
                PC += 4
                for j in reversed_op_codes : #rd
                    if i[20:25] == j:
                        for k in reversed_op_codes: #rs1
                            if i[12:17] == k:
                                for l in reversed_op_codes: #rs2
                                    if i[7:12] == l:
                                        registors[reversed_op_codes[j]] = registors[reversed_op_codes[k]] + registors[reversed_op_codes[l]]
                print_values(PC, registors)   
                Pc_to_inst(PC, lines)       

            elif(i[0:7] == '0100000'): #sub
                PC += 4
                for j in reversed_op_codes :
                    if i[20:25] == j:
                        for k in reversed_op_codes:
                            if i[12:17] == k:
                                for l in reversed_op_codes:
                                    if i[7:12] == l:
                                        registors[reversed_op_codes[j]] = registors[reversed_op_codes[k]] - registors[reversed_op_codes[l]]
                print_values(PC, registors)
                Pc_to_inst(PC, lines)

            else:
                print("error")
        elif(i[17:20] == '001'): #sll
            PC += 4
            for j in reversed_op_codes :
                if i[20:25] == j:
                    for k in reversed_op_codes:
                        if i[12:17] == k:
                            for l in reversed_op_codes:
                                if i[7:12] == l:
                                    registors[reversed_op_codes[j]] = shift_left(registors[reversed_op_codes[k]] , registors[reversed_op_codes[l]])
            print_values(PC, registors)
            Pc_to_inst(PC, lines)

        elif(i[17:20] == '010'): #slt
            PC += 4
            for j in reversed_op_codes :
                    if i[20:25] == j:
                        for k in reversed_op_codes:
                            if i[12:17] == k:
                                for l in reversed_op_codes:
                                    if i[7:12] == l:
                                        if (registors[reversed_op_codes[k]] < registors[reversed_op_codes[l]]):
                                            registors[reversed_op_codes[j]] = 1
            print_values(PC, registors)
            Pc_to_inst(PC, lines)

        elif(i[17:20] == '011'): #sltu
            PC += 4
            for j in reversed_op_codes :
                    if i[20:25] == j:
                        for k in reversed_op_codes:
                            if i[12:17] == k:
                                for l in reversed_op_codes:
                                    if i[7:12] == l:
                                        if abs((registors[reversed_op_codes[k]]) < abs(registors[reversed_op_codes[l]])):
                                            registors[reversed_op_codes[j]] = 1
            print_values(PC, registors)
            Pc_to_inst(PC, lines)

        elif(i[17:20] == '100'): #xor
            PC += 4
            for j in reversed_op_codes :
                if i[20:25] == j:
                    for k in reversed_op_codes:
                        if i[12:17] == k:
                            for l in reversed_op_codes:
                                if i[7:12] == l:
                                    registors[reversed_op_codes[j]] = registors[reversed_op_codes[k]] ^ registors[reversed_op_codes[l]]
            print_values(PC, registors)
            Pc_to_inst(PC, lines)

        elif(i[17:20] == '101'): #srl
            PC += 4
            for j in reversed_op_codes :
                if i[20:25] == j:
                    for k in reversed_op_codes:
                        if i[12:17] == k:
                            for l in reversed_op_codes:
                                if i[7:12] == l:
                                    registors[reversed_op_codes[j]] = shift_right(registors[reversed_op_codes[k]] , registors[reversed_op_codes[l]])
            print_values(PC, registors)
            Pc_to_inst(PC, lines)

        elif(i[17:20] == '110'): #or
            PC += 4
            for j in reversed_op_codes :
                if i[20:25] == j:
                    for k in reversed_op_codes:
                        if i[12:17] == k:
                            for l in reversed_op_codes:
                                if i[7:12] == l:
                                    registors[reversed_op_codes[j]] = registors[reversed_op_codes[k]] | registors[reversed_op_codes[l]]
            print_values(PC, registors)
            Pc_to_inst(PC, lines)

        elif(i[17:20] == '111'): #and
            PC += 4
            for j in reversed_op_codes :
                if i[20:25] == j:
                    for k in reversed_op_codes:
                        if i[12:17] == k:
                            for l in reversed_op_codes:
                                if i[7:12] == l:
                                    registors[reversed_op_codes[j]] = registors[reversed_op_codes[k]] & registors[reversed_op_codes[l]]
            print_values(PC, registors)
            Pc_to_inst(PC, lines)

        else:
            print("error")
#000000000001,00000,000,01001,0010011
#imm          rs1   f3  rd    opcode
#000000000000,01001,010,10010,0000011
#imm          rs1   f3  rd    opcode
#0            s1        s2
    elif (i[25:32] == '0000011'): #lw
        PC += 4
        for j in reversed_op_codes:
            if i[20:25] == j:
                for k in reversed_op_codes:
                    if i[12:17] == k:
                        registors[reversed_op_codes[j]] = memory[registors[reversed_op_codes[k]] + sign_extend_binary_to_int(i[0:12], 12)]
        print_values(PC, registors)
        Pc_to_inst(PC, lines)

    elif (i[25:32] == '0010011'): 
        if (i[17:20] == '000'): #addi
            PC += 4
            for j in reversed_op_codes:
                if i[20:25] == j:
                    for k in reversed_op_codes:
                        if i[12:17] == k:
                            registors[reversed_op_codes[j]] = registors[reversed_op_codes[k]] + sign_extend_binary_to_int(i[0:12], 12)
            print_values(PC, registors)
            Pc_to_inst(PC, lines)

        elif (i[17:20] == '011'): #sltiu
            PC += 4
            for j in reversed_op_codes:
                if i[20:25] == j:
                    for k in reversed_op_codes:
                        if i[12:17] == k:
                            if abs(registors[reversed_op_codes[k]]) < abs(int(i[0:12],12)):
                                registors[reversed_op_codes[j]] = 1
            print_values(PC, registors)
            Pc_to_inst(PC, lines)

        else:
            print("error")
    elif (i[25:32] == '1100111'): #jalr
        for j in reversed_op_codes: #rd
            if i[20:25] == j: 
                for k in reversed_op_codes: #x6
                    if i[12:17] == k:
                        registors[reversed_op_codes[j]] = PC + 4
                        PC = registors[reversed_op_codes[k]] + sign_extend_binary_to_int(i[0:12],12)
        print_values(PC, registors)
        Pc_to_inst(PC, lines)
#0000000,10101,01001,010,00000,0100011
#imm     rs2   rs1   f3  imm   opcode
    elif (i[25:32] == '0100011'): #sw
        PC += 4
        for j in reversed_op_codes: #rs1
            if i[12:17] == j:
                for k in reversed_op_codes: #rs2
                    if i[7:12] == k:
                        memory[registors[reversed_op_codes[j]] + sign_extend_binary_to_int([i[0:7] + i[20:25]][0] ,12 )] = registors[reversed_op_codes[k]] 
                        print_values(PC, registors)
                        Pc_to_inst(PC, lines)
#0000000,00000,00000,000,00000,1100011
#imm     rs2   rs1   f3  imm   opcode
#0000000,10010,00000,000,10000,1100011
    elif (i[25:32] == '1100011'):
        if(i[17:20] == '000'): #beq
            if i == "00000000000000000000000001100011":
                print_values(PC, registors)
                # print("virtual halt")
                return None
            PC += 4
            for j in reversed_op_codes: #rs1
                if i[12:17] == j:
                    for k in reversed_op_codes: #rs2
                        if i[7:12] == k:
                            print_values(PC, registors)
                            if registors[reversed_op_codes[j]] == registors[reversed_op_codes[k]]:
                                imm = i[0] + i[24] +i[1:7] + i[20:24]
                                PC = PC + sign_extend_binary_to_int(imm + "0", 13) 
                                Pc_to_inst(PC, lines)
                            else:
                                Pc_to_inst(PC, lines)
                                
        elif(i[17:20] == '001'): #bne
            PC 
            for j in reversed_op_codes: #rs1
                if i[12:17] == j:
                    for k in reversed_op_codes: #rs2
                        if i[7:12] == k:
                            print_values(PC, registors)
                            imm = i[0] + i[24] + i[1:7] + i[20:24] + '0'
                            offset = sign_extend_binary_to_int(imm, 13)
                            
                            if registors[reversed_op_codes[j]] != registors[reversed_op_codes[k]]:
                                # print(PC)
                                PC += offset 
                                # print(PC)
                                Pc_to_inst(PC, lines)
                            else:
                                Pc_to_inst(PC + 4, lines)
        elif(i[17:20] == '100'): #blt
            PC += 4
            for j in reversed_op_codes: #rs1
                if i[12:17] == j:
                    for k in reversed_op_codes: #rs2
                        if i[7:12] == k:
                            print_values(PC, registors)
                            if registors[reversed_op_codes[j]] < registors[reversed_op_codes[k]]:
                                imm = i[0] + i[24] +i[1:7] + i[20:24]
                                PC = PC + sign_extend_binary_to_int(imm + "0", 13) 
                                Pc_to_inst(PC, lines)
                            else:
                                Pc_to_inst(PC, lines)
        elif(i[17:20] == '101'): #bge
            PC += 4
            for j in reversed_op_codes: #rs1
                if i[12:17] == j:
                    for k in reversed_op_codes: #rs2
                        if i[7:12] == k:
                            print_values(PC, registors)
                            if registors[reversed_op_codes[j]] >= registors[reversed_op_codes[k]]:
                                imm = i[0] + i[24] +i[1:7] + i[20:24]
                                PC = PC + sign_extend_binary_to_int(imm + "0", 13) 
                                Pc_to_inst(PC, lines)
                            else:
                                Pc_to_inst(PC, lines)
        elif(i[17:20] == '110'): #bltu
            PC += 4
            for j in reversed_op_codes: #rs1
                if i[12:17] == j:
                    for k in reversed_op_codes: #rs2
                        if i[7:12] == k:
                            print_values(PC, registors)
                            if abs(registors[reversed_op_codes[j]]) < abs(registors[reversed_op_codes[k]]):
                                imm = i[0] + i[24] +i[1:7] + i[20:24]
                                PC = PC + sign_extend_binary_to_int(imm + "0", 13) 
                                Pc_to_inst(PC, lines)
                            else:
                                Pc_to_inst(PC, lines)
        elif(i[17:20] == '111'): #bgeu
            PC += 4
            for j in reversed_op_codes: #rs1
                if i[12:17] == j:
                    for k in reversed_op_codes: #rs2
                        if i[7:12] == k:
                            print_values(PC, registors)
                            if abs(registors[reversed_op_codes[j]]) >= abs(registors[reversed_op_codes[k]]):
                                imm = i[0] + i[24] +i[1:7] + i[20:24]
                                PC = PC + sign_extend_binary_to_int(imm + "0", 13)  
                                Pc_to_inst(PC, lines)
                            else:
                                Pc_to_inst(PC, lines)
        else:
            print("error")
#00000000000000010000,01000,0110111
#imm                  rd    opcode
    elif (i[25:32] == '0110111'): #lui
        PC += 4
        for j in reversed_op_codes:
            if i[20:25] == j:
                registors[reversed_op_codes[j]] = sign_extend_binary_to_int(i[0:20] + "000000000000", 12)
        print_values(PC, registors)
        Pc_to_inst(PC, lines)

    elif (i[25:32] == '0010111'): #auipc
        for j in reversed_op_codes:
            if i[20:25] == j:
                registors[reversed_op_codes[j]] = PC + sign_extend_binary_to_int(i[0:20] + "000000000000", 12)
                PC += 4
        print_values(PC, registors)
        Pc_to_inst(PC, lines)
        
#1 11111110 0 0111111111,00001,1101111
#0 12345678 9 0123456789
#imm                  rd    opcode
    elif (i[25:32] == '1101111'): #jal
        
        for j in reversed_op_codes: #rd
            if i[20:25] == j: 
                registors[reversed_op_codes[j]] = PC + 4
                imm = i[0] + i[12:20] + i[11] + i[1:11] + '0'     
                PC = PC + (sign_extend_binary_to_int(imm , 21)) 

                
        print_values(PC, registors)
        Pc_to_inst(PC, lines)
    else:
        print("error") 
        

def Pc_to_inst(PC, lines):
    #print(PC)
    if PC > (len(lines)) * 4:
        #print(PC)
        print("code over")
    else:
        for j in range(len(lines)):
            if j * 4 == PC:
                i = lines[j]
                instruction_stats(PC,lines, i)
                

file_path = input_file
with open(file_path, "r") as file:
    lines = file.readlines()
lines = [line.strip() for line in lines]

Pc_to_inst(PC, lines)

def generate_hexadecimal(start='10000', step=4, count=32):
    current_hex = int(start, 16)
    hex_list = []
    for _ in range(count):
        hex_value = hex(current_hex)[2:].zfill(4) 
        hex_list.append('0x' + '000' + hex_value + ':')
        current_hex += step
    return hex_list


for i in range(65000,70000):
    if memory[i] != 0:
        if i == 65536:
            mem['0x00010000'] = memory[i] 
        elif i == 65540:
            mem['0x00010004'] = memory[i]
        elif i == 65544:
            mem['0x00010008'] = memory[i] 
        elif i == 65548:
            mem['0x0001000c'] = memory[i]          
        elif i == 65552:
            mem['0x00010010'] = memory[i]
        elif i == 65556:
            mem['0x00010014'] = memory[i]
        elif i == 65560:
            mem['0x00010018'] = memory[i]
        elif i == 65564:
            mem['0x0001001c'] = memory[i]    
        elif i == 65568:
            mem['0x00010020'] = memory[i]
        elif i == 65572:
            mem['0x00010024'] = memory[i]
        elif i == 65576:
            mem['0x00010028'] = memory[i] 
        elif i == 65580:
            mem['0x0001002c'] = memory[i]          
        elif i == 65584:
            mem['0x00010030'] = memory[i]
        elif i == 65588:
            mem['0x00010034'] = memory[i]
        elif i == 65592:
            mem['0x00010038'] = memory[i]
        elif i == 65596:
            mem['0x0001003c'] = memory[i]    
        elif i == 65600:
            mem['0x00010040'] = memory[i]     
        elif i == 65604:
            mem['0x00010044'] = memory[i]
        elif i == 65608:
            mem['0x00010048'] = memory[i] 
        elif i == 65612:
            mem['0x0001004c'] = memory[i]          
        elif i == 65616:
            mem['0x00010050'] = memory[i]
        elif i == 65620:
            mem['0x00010054'] = memory[i]
        elif i == 65624:
            mem['0x00010058'] = memory[i]
        elif i == 65628:
            mem['0x0001005c'] = memory[i]    
        elif i == 65632:
            mem['0x00010060'] = memory[i]  
        elif i == 65636:
            mem['0x00010064'] = memory[i]
        elif i == 65640:
            mem['0x00010068'] = memory[i] 
        elif i == 65644:
            mem['0x0001006c'] = memory[i]          
        elif i == 65648:
            mem['0x00010070'] = memory[i]
        elif i == 65652:
            mem['0x00010074'] = memory[i]
        elif i == 65656:
            mem['0x00010078'] = memory[i]
        elif i == 65660:
            mem['0x0001007c'] = memory[i]    
        
for i in mem:
    c = i + ":" + "0b" + int_to_twos_complement(mem[i], 32)
    write_in_file(output_file,c)
