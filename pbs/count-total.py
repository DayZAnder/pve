#!/usr/bin/env python3

# Simple ugly script to summarize vmid chunks and output total.
# Run ./estiname-size.py and pipe that output to a file like ./estiname-size.py arguments > vmidstats
# ./count-total.py vmidstats

import re
import argparse

# Function to parse chunks and sizes
def parse_chunk_size(chunk_str):
    match = re.match(r'\|\s+\d{4}-\d{2}-\d{2}.*?(\d+) chunks.*?(\d+) MiB', chunk_str)
    if match:
        chunks, size = map(int, match.groups())
        return chunks, size
    return 0, 0

# Function to parse the content of the file and summarize data
def parse_file_content(file_content):
    vmid_data = {}
    current_vmid = None

    for line in file_content.splitlines():
        if line.startswith("vmid = "):
            current_vmid = int(line.split()[-1])
            vmid_data[current_vmid] = {"chunks": 0, "size": 0}
        elif line.strip().startswith("|"):
            chunks, size = parse_chunk_size(line)
            vmid_data[current_vmid]["chunks"] += chunks
            vmid_data[current_vmid]["size"] += size

    return vmid_data

# Function to print summarized data for each vmid
def print_summary(vmid_data):
    for vmid, data in vmid_data.items():
        print(f"vmid = {vmid}")
        print(f"Total chunks: {data['chunks']}")
        print(f"Total size: {data['size']} MiB")
        print("-----------------------------")

    total_chunks = sum(data["chunks"] for data in vmid_data.values())
    total_size = sum(data["size"] for data in vmid_data.values())
    print("Total Data Usage:")
    print(f"Total chunks: {total_chunks}")
    print(f"Total size: {total_size} MiB")

def main():
    parser = argparse.ArgumentParser(description="Summarize data usage for each vmid.")
    parser.add_argument("filename", help="Path to the file containing estiname-size.py output")
    args = parser.parse_args()

    try:
        with open(args.filename, 'r') as file:
            file_content = file.read()

        vmid_data = parse_file_content(file_content)
        print_summary(vmid_data)

    except FileNotFoundError:
        print(f"File '{args.filename}' not found.")

if __name__ == "__main__":
    main()
