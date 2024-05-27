import argparse
import os
import re

DEFAULT_CURRENT_VERSION = 1
DEFAULT_MARKETING_VERSION = 1.0

def writeBuildFile(build_file, version_string, build_number):
    # Check if file exists
    if not(os.path.isfile(build_file)):
        raise Exception(f"Exception: build file <{build_file}> was not found!")
    
    with open(build_file, 'r') as f:
        data = f.read()

    # Write to file 
    with open(build_file, 'w') as f:
        # Change build number
        data = re.sub(f"CURRENT_PROJECT_VERSION = {DEFAULT_CURRENT_VERSION}", f"CURRENT_PROJECT_VERSION = {build_number}", data)

        # Change version string
        data = re.sub(f"MARKETING_VERSION = {DEFAULT_MARKETING_VERSION}", f"MARKETING_VERSION = {version_string}", data)

        # Write
        f.write(data)
    


def readConstantFile(constant_file, version_var_name, build_var_name):
    # Check if the file exists
    if not(os.path.isfile(constant_file)):
        raise Exception(f"Exception: Constants file <{constant_file} was not found!")
    
    # Read the values from file
    version_name = ''
    build_number = -1

    with open(constant_file, 'r') as f:
        readed_file = f.readlines()
        for line in readed_file:
            line = line.strip()
            if(version_var_name in line):
                # Get version name 
                search_pattern = version_var_name + r" = 'Versión ([0-9]+(\.[0-9]+)+)';"
                version_name = re.findall(search_pattern, line)[0][0]
                print(f"Version name found: {version_name}")
            elif(build_var_name in line):
                # Get build number
                search_pattern = r"\d+"
                build_number = int(re.findall(search_pattern, line)[0])
                print(f"Build number found : {build_number}")

    # Check if any values are found
    if(version_name == ''):
        raise Exception("No version name found!")
    
    elif(build_number == -1):
        raise Exception("No build number founde!")
    
    else:
        return version_name, build_number



if __name__ == '__main__':

    # Establish parser
    parser = argparse.ArgumentParser(
        description="Changes the version string and build number on the xcodeproject file"
    )

    parser.add_argument(
        "--constants-file",
        required=True,
        type=str,
        help="The file that defines the version string and build number"
    )

    parser.add_argument(
        "--version-var",
        required=True,
        type=str,
        help="The name of the version variable on the constants-file"
    )

    parser.add_argument(
        "--build-var",
        required=True,
        type=str,
        help="The name of the build version variable on the constants-file"
    )

    parser.add_argument(
        "--build-file",
        required=True,
        type=str,
        help="The build file to change"
    )


    args = parser.parse_args()

    try:
        # Get info from constant-file
        version_name, build_number =  readConstantFile(
                                            args.constants_file,
                                            args.version_var,
                                            args.build_var
                                            )
        
        writeBuildFile(args.build_file, version_name, build_number)

    except Exception as e:
        print(e)
        exit(1)    
