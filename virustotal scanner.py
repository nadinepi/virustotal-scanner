def scan():
    import os
    import pandas as pd
    import sys

    os.chdir(os.path.expanduser("~") + '/OneDrive/Documents/Python Scripts/the good stuff')

    x = input(
        "\n(Type * to exit) Type 'su' to scan a url, type 'sf' to scan a file, or type 'rf' to get report on file: ")

    if x == '*':
        print("\nSee you later!\n")
        sys.exit()

    elif x == 'su':
        import requests

        resource = input("(Type * to exit) Enter website name: ")

        if resource == '*':
            print("\nSee you later!\n")
            sys.exit()

        else:
            url = 'https://www.virustotal.com/vtapi/v2/url/report'

            params = {'apikey': 'ff1c1c0d323b288e247e058968de62713120e40d389e57cd0502af00430c9ec0',
                      'resource': resource}

            response = requests.get(url, params=params)

            json = response.json()

            bad = json['positives']

            scans = json['scans']

            if bad == 0:
                restart = input("\nYour url is clean! Would you like to scan another url or file? (y/n) ")
                if restart == 'y':
                    scan()
                else:
                    print("\nSee you later!\n")
                    sys.exit()

            else:
                df = pd.DataFrame.from_dict(scans, orient='columns')

                df = df.transpose()

                df1 = df[df.detected]

                y = df1.index.tolist()
                print("\nBAD URL! The following antivirus software detected malware: ", y)
                restart = input("\nWould you like to scan another url or file? (y/n) ")
                if restart == 'y':
                    scan()
                else:
                    print("\nSee you later!\n")
                    sys.exit()

    elif x == 'sf':
        import requests

        myfile = input("(Type * to exit) Input file name: ")

        if myfile == '*':
            print("\nSee you later!\n")
            sys.exit()

        else:
            url = 'https://www.virustotal.com/vtapi/v2/file/scan'

            params = {'apikey': 'ff1c1c0d323b288e247e058968de62713120e40d389e57cd0502af00430c9ec0'}

            files = {'file': (myfile, open(myfile, 'rb'))}

            response = requests.post(url, files=files, params=params)

            json = response.json()

            result = json['verbose_msg']

            scanid = json['scan_id']

            print(result, "\nBe sure to wait for a few minutes while the scan runs."
                          "\nNext steps: Copy your scan id, rerun, and type 'rf': ", scanid)

    elif x == 'rf':
        import requests

        resource = input("(Type * to exit) Enter scan id: ")

        if resource == '*':
            print("\nSee you later!\n")
            sys.exit()

        else:
            url = 'https://www.virustotal.com/vtapi/v2/file/report'

            params = {'apikey': 'ff1c1c0d323b288e247e058968de62713120e40d389e57cd0502af00430c9ec0',
                      'resource': resource}

            response = requests.get(url, params=params)

            json = response.json()

            bad = json['positives']

            total = json['total']

            scans = json['scans']

            if bad == 0:
                print("\nYour file is clean!")
                restart = input("\nWould you like to scan another url or file? (y/n) ")
                if restart == 'y':
                    scan()
                else:
                    print("\nSee you later!\n")
                    sys.exit()

            else:
                df = pd.DataFrame.from_dict(scans, orient='columns')

                df = df.transpose()

                df1 = df[df.detected]

                y = df1.index.tolist()
                print("\nBAD FILE! The following antivirus software detected malware: ", y)
                restart = input("\nWould you like to scan another url or file? (y/n) ")
                if restart == 'y':
                    scan()
                else:
                    print("\nSee you later!\n")
                    sys.exit()

    else:
        print("INVALID INPUT, try again")
        scan()


scan()
