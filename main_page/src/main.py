__author__ = "Azeem Mohammed"
__status__ = "Development"
__credits__ = ["Joon Bang", "Azeem Mohammed"]

import time
import functions


def create_backup():
    with open("main_page/main_page.mmd") as current:
        local_time = time.asctime(time.localtime(time.time())).split()
        local_time = "_" + '_'.join(local_time[1:3] + local_time[3:][::-1])
        with open("main_page/backups/main_page" + local_time + ".mmd.bak", "w") as backup:
            backup.write(current.read())


def main():
    if raw_input("Update main page? (y/n): ") == "n":
        return

    # read contents
    with open("main_page/main_page.mmd") as main_page:
        text = main_page.read()

    text, definitions = functions.update_macro_list(text)
    text = functions.add_symbols_data(text)
    text = functions.update_headers(text, definitions)
    text = functions.add_usage(text)

    # only create backup if program did not crash
    create_backup()

    with open("main_page/main_page.mmd", "w") as main_page:
        main_page.write(text)


if __name__ == '__main__':
    main()
