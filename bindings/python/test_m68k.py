#!/usr/bin/env python

# Capstone Python bindings, by Nicolas PLANEL <nplanel@gmail.com>
from __future__ import print_function
from capstone import *
from capstone.m68k import *
from xprint import to_hex, to_x

M68K_CODE = b"\xd4\x40\x87\x5a\x4e\x71\x02\xb4\xc0\xde\xc0\xde\x5c\x00\x1d\x80\x71\x12\x01\x23\xf2\x3c\x44\x22\x40\x49\x0e\x56\x54\xc5\xf2\x3c\x44\x00\x44\x7a\x00\x00\xf2\x00\x0a\x28\x4E\xB9\x00\x00\x00\x12\x4E\x75"

all_tests = (
        (CS_ARCH_M68K, CS_MODE_BIG_ENDIAN | CS_MODE_M68K_040, M68K_CODE, "M68K"),
)

s_addressing_modes = {
	0:  "<invalid mode>",

	1:  "Register Direct - Data",
	2:  "Register Direct - Address",

	3:  "Register Indirect - Address",
	4:  "Register Indirect - Address with Postincrement",
	5:  "Register Indirect - Address with Predecrement",
	6:  "Register Indirect - Address with Displacement",

	7:  "Address Register Indirect With Index - 8-bit displacement",
	8:  "Address Register Indirect With Index - Base displacement",

	9:  "Memory indirect - Postindex",
	10: "Memory indirect - Preindex",

	11: "Program Counter Indirect - with Displacement",

	12: "Program Counter Indirect with Index - with 8-Bit Displacement",
	13: "Program Counter Indirect with Index - with Base Displacement",

	14: "Program Counter Memory Indirect - Postindexed",
	15: "Program Counter Memory Indirect - Preindexed",

	16: "Absolute Data Addressing  - Short",
	17: "Absolute Data Addressing  - Long",
	18: "Immidate value",
}

def print_insn_detail(insn):
    if len(insn.operands) > 0:
        print("\top_count: %u" % (len(insn.operands)))
        print("\tgroups_count: %u" % len(insn.groups))

    for i, op in enumerate(insn.operands):
        if op.type == M68K_OP_REG:
            print("\t\toperands[%u].type: REG = %s" % (i, insn.reg_name(op.reg)))

        if op.type == M68K_OP_IMM:
            if insn.op_size.type == M68K_SIZE_TYPE_FPU:
                if insn.op_size.size == M68K_FPU_SIZE_SINGLE:
                    print("\t\toperands[%u].type: IMM = %f" % (i, op.simm))
                elif insn.op_size.size == M68K_FPU_SIZE_DOUBLE:
                    print("\t\toperands[%u].type: IMM = %lf" % (i, op.dimm))
                else:
                    print("\t\toperands[%u].type: IMM = <unsupported>" % (i))
                continue
            print("\t\toperands[%u].type: IMM = 0x%x" % (i, op.imm & 0xffffffff))

        if op.type == M68K_OP_MEM:
            print("\t\toperands[%u].type: MEM" % (i))
            if op.mem.base_reg != M68K_REG_INVALID:
                print("\t\t\toperands[%u].mem.base: REG = %s" % (i, insn.reg_name(op.mem.base_reg)))
            if op.mem.index_reg != M68K_REG_INVALID:
                print("\t\t\toperands[%u].mem.index: REG = %s" % (i, insn.reg_name(op.mem.index_reg)))
                mem_index_str = "w"
                if op.mem.index_size > 0:
                    mem_index_str = "l"
                print("\t\t\toperands[%u].mem.index: size = %s" % (i, mem_index_str))
            if op.mem.disp != 0:
                print("\t\t\toperands[%u].mem.disp: 0x%x" % (i, op.mem.disp))
            if op.mem.scale != 0:
                print("\t\t\toperands[%u].mem.scale: %d" % (i, op.mem.scale))
            print("\t\taddress mode: %s" % (s_addressing_modes[op.address_mode]))
    print()

# ## Test class Cs
def test_class():
    address = 0x01000
    for (arch, mode, code, comment) in all_tests:
        print("*" * 16)
        print("Platform: %s" % comment)
        print("Code: %s " % to_hex(code))
        print("Disasm:")

        try:
            md = Cs(arch, mode)
            md.detail = True
            last_address = 0
            for insn in md.disasm(code, address):
                last_address = insn.address + insn.size
                print("0x%x:\t%s\t%s" % (insn.address, insn.mnemonic, insn.op_str))
                print_insn_detail(insn)
            print("0x%x:\n" % (last_address))

        except CsError as e:
            print("ERROR: %s" % e.__str__())

if __name__ == '__main__':
    test_class()





