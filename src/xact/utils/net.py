



import socket


def get_host_ip():
    # Create a socket to find the local IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This IP address doesn't need to be reachable; it's just used to determine the local IP
        s.connect(("8.8.8.8", 80))
        host_ip = s.getsockname()[0]
    except Exception:
        host_ip = "127.0.0.1"  # Fallback to localhost if unable to determine IP
    finally:
        s.close()
    
    return host_ip