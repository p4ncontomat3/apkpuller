#!/usr/bin/python3
import sys
import os
import subprocess

def list_apps(keyword):
    cmd = 'adb shell pm list packages | grep {}'.format(keyword)
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

            print("Invalid choice. Please try again.")
    except subprocess.CalledProcessError as e:
        print("[-] No package names were found with the keyword provided.")
        sys.exit(1)

def list_apks(package_name):
    try:
        apk_paths = []
        cmd = 'adb shell pm path {}'.format(package_name)
        print("[+] apk files found:")
        output = subprocess.check_output(cmd, shell=True)
        apk_path = output.decode().strip().replace('package:', '').split("\n")
        
        for apk in apk_path:
            print(apk)

        return apk_path
    except subprocess.CalledProcessError as e:
        print("[-] apk files not found")
        sys.exit(1)

def pull_apks(apk_path):
    try:
        for apk in apk_path:
            cmd = 'adb pull {}'.format(apk)
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
        print_banner()
        keyword = sys.argv[1]
        print("[*] Checking package names matching {}".format(keyword))
        package_name = list_apps(keyword)
        apk_path = list_apks(package_name)
        pull_apks(apk_path)



if __name__ == "__main__":
    main()
