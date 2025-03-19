import argparse
import ipaddress
import os
import socket


def get_ip_networks():
    """
    Retrieves the hostname of the container/machine and collects all configured IPv4 networks.
    Returns a dictionary with the hostname as the key and a list of IP networks as the value.
    """
    hostname = socket.gethostname()
    ip_addresses = os.popen("ip -o -f inet addr show | awk '{print $4}'").read().strip().split('\n')
    return {hostname: ip_addresses}


def write_to_file(output_file):
    """
    Writes the collected IP networks to the specified file.
    Each entry is stored in the format: "hostname: IP_network".
    """
    networks = get_ip_networks()
    with open(output_file, 'a') as f:
        for host, ips in networks.items():
            for ip in ips:
                f.write(f"{host}: {ip}\n")


def check_collisions(file_path):
    """
    Reads IP networks from the given file and detects any overlapping (colliding) networks.
    Returns a list of tuples containing the hostname and the conflicting network.
    """
    networks = {}
    collisions = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        host, net = line.strip().split(': ')
        try:
            subnet = ipaddress.ip_network(net, strict=False)
        except ValueError:
            continue  # Skip invalid IP network entries
        
        for existing_net in networks.values():
            if subnet.overlaps(existing_net):
                collisions.append((host, net))
        
        networks[host] = subnet
    
    return collisions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='IP Tool for network reporting and collision detection.')
    parser.add_argument('--check-collision', type=str, help='File path containing network list')
    parser.add_argument('--output-file', type=str, help='File path to save networks')
    
    args = parser.parse_args()
    
    if args.check_collision:
        # If --check-collision is specified, analyze the file for IP overlaps.
        colliding_networks = check_collisions(args.check_collision)
        if colliding_networks:
            print("Colliding Networks Found:")
            for host, net in colliding_networks:
                print(f"{host}: {net}")
        else:
            print("No collisions detected.")
    elif args.output_file:
        # If --output-file is specified, collect IP networks and save to file.
        write_to_file(args.output_file)
        print(f"IP networks written to {args.output_file}")
    else:
        # Default behavior: Print the collected IP networks to stdout.
        print(get_ip_networks())
