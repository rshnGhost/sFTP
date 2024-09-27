import paramiko
import os, getpass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def sftp_connect(host, port, username, password=None):
    """Connect to an SFTP server."""
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp
    except Exception as e:
        print(f"Error connecting to SFTP server: {e}")
        return None

def sftp_get_file(sftp, remote_path, local_path):
    """Download a single file from the SFTP server."""
    try:
        sftp.get(remote_path, local_path)
        print(f"Downloaded: {remote_path} to {local_path}")
    except Exception as e:
        print(f"Error downloading {remote_path}: {e}")

def sftp_get(sftp, remote_path, local_path, use_threads=True):
    """Download a directory or a file from the SFTP server using multithreading."""
    try:
        if not os.path.exists(local_path):
            os.makedirs(local_path)

        if sftp.stat(remote_path).st_mode & 0o40000:  # Check if it's a directory
            items = sftp.listdir(remote_path)
            paths = [(sftp, os.path.join(remote_path, item), os.path.join(local_path, item)) for item in items]

            if use_threads:
                with ThreadPoolExecutor() as executor:
                    executor.map(lambda p: sftp_get_file(*p), paths)
            else:
                for p in paths:
                    sftp_get_file(*p)
        else:
            sftp_get_file(sftp, remote_path, local_path)
    except Exception as e:
        print(f"Error downloading {remote_path}: {e}")

def sftp_put_file(sftp, local_path, remote_path):
    """Upload a single file to the SFTP server."""
    try:
        sftp.put(local_path, remote_path)
        print(f"Uploaded: {local_path} to {remote_path}")
    except Exception as e:
        print(f"Error uploading {local_path}: {e}")

def sftp_put(sftp, local_path, remote_path, use_threads=True):
    """Upload a directory or file to the SFTP server using multithreading."""
    try:
        if not os.path.exists(local_path):
            return

        if os.path.isdir(local_path):
            items = os.listdir(local_path)
            paths = [(sftp, os.path.join(local_path, item), os.path.join(remote_path, item)) for item in items]

            if use_threads:
                with ThreadPoolExecutor() as executor:
                    executor.map(lambda p: sftp_put_file(*p), paths)
            else:
                for p in paths:
                    sftp_put_file(*p)
        else:
            sftp_put_file(sftp, local_path, remote_path)
    except Exception as e:
        print(f"Error uploading {local_path}: {e}")

# Multiprocessing versions (similar structure)
def sftp_get_mp(sftp, remote_path, local_path):
    """Download using multiprocessing."""
    with ProcessPoolExecutor() as executor:
        # Similar to threading, but use ProcessPoolExecutor
        sftp_get(sftp, remote_path, local_path, use_threads=False)

def sftp_put_mp(sftp, local_path, remote_path):
    """Upload using multiprocessing."""
    with ProcessPoolExecutor() as executor:
        # Similar to threading, but use ProcessPoolExecutor
        sftp_put(sftp, local_path, remote_path, use_threads=False)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    action_mode = int(input("1\t=>\tUpload\n2\t=>\tDownload\nSelect an Option [2]: ") or 2)
    
    hostname = input("Enter Hostname [test.rebex.net]: ") or "test.rebex.net"
    portnum = int(input("Enter Port Number [22]: ") or 22)
    username = input("Enter Username [demo]: ") or "demo"
    password = getpass.getpass("Enter Password: ") or "password"

    use_multithreading = input("Use Multithreading? [y/n]: ").lower() == 'y'
    
    try:
        sftp = sftp_connect(hostname, portnum, username, password)
        if sftp:
            if action_mode == 1:
                # Put (upload)
                local_put_path = input(f"Enter Local Path [{os.path.join(os.getcwd(), 'upload')}]: ") or os.path.join(os.getcwd(), 'upload')
                remote_put_path = input(f"Enter Remote Path [/]: ") or "/"
                if use_multithreading:
                    sftp_put(sftp, local_put_path, remote_put_path)
                else:
                    sftp_put_mp(sftp, local_put_path, remote_put_path)
            elif action_mode == 2:
                # Get (download)
                remote_get_path = input(f"Enter Remote Path [/]: ") or "/"
                local_get_path = input(f"Enter Local Path [{os.path.join(os.getcwd(), 'download')}]: ") or os.path.join(os.getcwd(), 'download')
                if use_multithreading:
                    sftp_get(sftp, remote_get_path, local_get_path)
                else:
                    sftp_get_mp(sftp, remote_get_path, local_get_path)
            else:
                print("Invalid Action")
            sftp.close()
    except Exception as err:
        print(f"{err=}")
