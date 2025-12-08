from functions.get_files_info import get_files_info


def main():
    working_dir = "calculator"
    root_contents = get_files_info(working_dir)
    print(root_contents)
    root_contents = get_files_info(working_dir,'pkg')
    print(root_contents)
    root_contents = get_files_info(working_dir,"/bin")
    print(root_contents)
    root_contents = get_files_info(working_dir,"../")
    print(root_contents)

main()