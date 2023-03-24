#!/usr/bin/python3
import sys
import os
import subprocess

def select_device():
    result = subprocess.run(['adb', 'devices', '-l'], capture_output=True, text=True)

    devices = []
    transports = []
    lines = result.stdout.strip().split('\n')[1:]
    if len(lines) > 1:
        for line in lines:
            device_info = line.strip()#.split()
            device_name = device_info.split('ce:')[1]
            transport = device_info.split('id:')
            devices.append({
                'serial': device_info.split()[0],
                'device_name' : device_name.split(' ')[0],
                'transport' : transport[1]
            })

        print('Available devices:')
        for i, device in enumerate(devices):
            print('%d)' % (i+1), device['device_name'],'->', 'transport_id:',device['transport'])
            
        while True:
            selection = input('Select a device (1-%d): ' % len(devices))
            try:
                index = int(selection) - 1
                if 0 <= index < len(devices):
                    return devices[index]['transport']
            except ValueError:
                pass
            print('Invalid selection.')
    else:
        print('[*] Only one device attached')
        return 0

def list_apps(keyword, transport_id):
    if transport_id == 0:
        cmd = 'adb shell pm list packages | grep {}'.format(keyword)
    else:
        cmd = 'adb -t{0} shell pm list packages | grep {1}'.format(transport_id, keyword)
    try:
        output = subprocess.check_output(cmd, shell=True)
        print("[+] Packages Found!!!")
        apps = output.decode().strip().split('\n')
        app_list = [app.replace('package:', '') for app in apps]

        print("[*] Please select a package name:")
        for index, app in enumerate(app_list):
            print("{}) {}".format(index+1, app))

        while True:
            try:
                choice = int(input("Select an option: "))
                if 1 <= choice <= len(app_list):
                    return app_list[choice-1]
            except ValueError:
                pass

            print("[-] Invalid choice. Please try again.")
    except subprocess.CalledProcessError as e:
        print("[-] No package names were found with the keyword provided.")
        sys.exit(1)

def list_apks(package_name, transport_id):
    try:
        apk_paths = []
        if transport_id == 0:
            cmd = 'adb shell pm path {}'.format(package_name)
        else:
            cmd = 'adb -t{0} shell pm path {1}'.format(transport_id, package_name)
        print("[+] apk files found:")
        output = subprocess.check_output(cmd, shell=True)
        apk_path = output.decode().strip().replace('package:', '').split("\n")
        
        for apk in apk_path:
            print(apk)

        return apk_path
    except subprocess.CalledProcessError as e:
        print("[-] apk files not found")
        sys.exit(1)

def pull_apks(apk_path, transport_id):
    try:
        for apk in apk_path:
            if transport_id == 0:
                cmd = 'adb pull {}'.format(apk)
            else:
                cmd = 'adb -t{0} pull {1}'.format(transport_id, apk)
            output = subprocess.check_output(cmd, shell=True)
        print("[*] All apk files pulled")
    except subprocess.CalledProcessError as e:
        print("[-] apk files not found")
        sys.exit(1)

def print_banner():
    banner = """
                *                        **     **                  
                *                         *      *                  
                *                         *      *                  
 ****   * ***   *   *   * ***   *    *    *      *     ****   * **  
     *  **   *  *  *    **   *  *    *    *      *    *    *   *    
 *****  *    *  ***     *    *  *    *    *      *    ******   *    
*    *  **   *  *  *    **   *  *    *    *      *    *        *    
*   **  * ***   *   *   * ***   *   **    *      *    *    *   *    
 *** *  *       *    *  *        *** *  *****  *****   ****    *    
        *               *                                           
        *               *                                           
    """

    print(banner)
    print("\t\t\t\t\tby @p4ncontomat3\n\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: {} <keyword>".format(sys.argv[0]))
        sys.exit(1)
        
    else:
        try:
            print_banner()
            keyword = sys.argv[1]
            print("[*] Checking package names matching {}".format(keyword))
            transport_id = select_device()
            package_name = list_apps(keyword, transport_id)
            apk_path = list_apks(package_name, transport_id)
            pull_apks(apk_path, transport_id)
        except KeyboardInterrupt:
            print("\n\n[<3] bai bai")



if __name__ == "__main__":
    main()