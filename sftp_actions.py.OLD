import paramiko
import os, getpass

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

def sftp_get(sftp, remote_path, local_path):
    """Download a file or directory from the SFTP server."""
    if remote_path[0] in ["/", "\\"]:
        remote_path = remote_path[1:]
    try:
        if sftp.stat(remote_path).st_mode & 0o40000:  # Check if it's a directory
            os.makedirs(local_path, exist_ok=True)
            for item in sftp.listdir(remote_path):
                sftp_get(sftp, os.path.join(remote_path, item), os.path.join(local_path, item))
        else:
            sftp.get(remote_path, local_path)
        print(f"Downloaded: \{remote_path} to {local_path}")
    except Exception as e:
        print(f"Error downloading {remote_path}: {e}")

def sftp_put(sftp, local_path, remote_path):
    """Upload a file or directory to the SFTP server."""
    if remote_path[0] in ["/", "\\"]:
        remote_path = remote_path[1:]
    try:
        if os.path.isdir(local_path):  # Check if it's a directory
            try:
                sftp.mkdir(remote_path)  # Create the remote directory
            except IOError as e:
                if 'File already exists' in str(e):
                    print(f"Directory already exists: {remote_path}")
                else:
                    raise  # Raise other IOErrors
            
            for item in os.listdir(local_path):
                sftp_put(sftp, os.path.join(local_path, item), os.path.join(remote_path, item))
        else:
            sftp.put(local_path, remote_path)  # Upload the file
            print(f"Uploaded: {local_path} to \{remote_path}")
    except Exception as e:
        print(f"Error uploading {local_path}: {e}")


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    action_mode = int(input("1\t=>\tUpload\n2\t=>\tDownload\nSelect a Option [2]: ") or 2)
    if action_mode in [None, 0] or action_mode >= 3:
        exit
    
    hostname = input("Enter Hostname [test.rebex.net]: ") or "test.rebex.net"
    portnum = int(input("Enter Port Number [22]: ") or 22)
    username = input("Enter Username [demo]: ") or "demo"
    password = getpass.getpass("Enter Password: ") or "password"

    try:
        sftp = sftp_connect(hostname, portnum, username, password)
        if sftp:
            match action_mode:
                case 1:
                    # Put (upload)
                    local_put_path = input(f"Enter Local Path [{os.path.join(os.getcwd(), "upload")}]: ") or os.path.join(os.getcwd(), "upload")
                    remote_put_path = input(f"Enter Remote Path [root]: ") or "\\"
                    sftp_put(sftp, local_put_path, remote_put_path)
                case 2:
                    # Get (download)
                    remote_get_path = input(f"Enter Remote Path [root]: ") or "\\"
                    local_get_path = input(f"Enter Local Path [{os.path.join(os.getcwd(), "download")}]: ") or os.path.join(os.getcwd(), "download")
                    sftp_get(sftp, remote_get_path, local_get_path)
                case _:
                    print("Invalid Action")
            sftp.close()
    except Exception as err:
        print(f"{err=}")
