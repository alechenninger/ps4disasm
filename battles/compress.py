#!/usr/bin/python3

"""
This script compresses the battle formation data for ROM compilation.
Formation data is expected to be compressed in the original assembly.

It depends on external utilities for Kosinski compression and ASM compilation.
This may be configured using the PS4DISASM_KOSINSKI_COMP environment variable template string, 
and PS4DISASM_COMPILE environment variable template string respectively.
Each replaces {in_file} and {out_file} variables.

Using https://github.com/Clownacy/accurate-kosinski is recommended.
As of writing, https://github.com/VanderCat/accurate-kosinski is a useful fork 
for building accurate-kosinski binaries.
"""

import os
import subprocess
import sys
import tempfile

formations_asm = ["battle_formations_1.asm",
                  "battle_formations_2.asm",
                  "battle_formations_3.asm",
                  "battle_formations_4.asm",
                  "boss_formations.asm"]

compile_cmd_template = os.getenv(
    "PS4DISASM_COMPILE", ("asl -cpu 68000 -o {out_file}.p {in_file} && "
                          "p2bin {out_file}.p {out_file} && "
                          "mv {out_file}.bin {out_file}"))
compress_cmd_template = os.getenv(
    "PS4DISASM_KOSINSKI_COMP", "kcompress {in_file} {out_file}")


def run_subprocess(command):
    try:
        # Execute the external command
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        return False
    return True


def compile_constants(input_file, output_file):
    command = compile_cmd_template.format(
        in_file=input_file, out_file=output_file)
    return run_subprocess(command)


def kosinski_compress(input_file, output_file):
    # Replace placeholders in the command template
    command = compress_cmd_template.format(
        in_file=input_file, out_file=output_file)
    return run_subprocess(command)


def main():
    # Assuming files are in the same directory as the script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    success = True

    for file_name in formations_asm:
        input_file_path = os.path.join(script_dir, file_name)
        output_file_name = os.path.splitext(file_name)[0] + ".bin"
        output_file_path = os.path.join(script_dir, output_file_name)

        with tempfile.NamedTemporaryFile() as uncompressed:
            if compile_constants(input_file_path, uncompressed.name):
                print(f"Successfully compiled: {input_file_path} to {uncompressed.name}")  # nopep8
            else:
                success = False
                continue

            if kosinski_compress(uncompressed.name, output_file_path):
                print(f"Successfully compressed: {uncompressed.name} to {output_file_path}")  # nopep8
            else:
                success = False

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
