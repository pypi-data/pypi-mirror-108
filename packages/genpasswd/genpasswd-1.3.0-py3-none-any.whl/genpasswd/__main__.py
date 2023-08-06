import argparse
from . import genpasswd

# def usage_string():
#     return """{0} 
# {2:{1}} [--length] [--ignore]
# {2:{1}} [--include] [--only] [--repeat]
# {2:{1}} [--separation] [--separator] [--seplen]
# {2:{1}} --help --version""".format('genpasswd', len('usage:'), '')

def get_argument():
    parser = argparse.ArgumentParser(usage="genpasswd [options]")
    parser.add_argument('-v','--version', action='version', help='show version number and exit.', version="1.3.0")
    group = parser.add_argument_group("to customize Password")
    group.add_argument("-l", "--length", dest="length", type=int, metavar='', help="to set length to the password")
    group.add_argument("-n", "--ignore", dest="ignore", metavar='', help="to ignore unwanted characters to the password")
    group.add_argument("-i", "--include", dest="include", metavar='', help="to include characters to the password")
    group.add_argument("-o", "--only", dest="only", metavar='', help="to create password only using wanted characters")
    group.add_argument("-s", "--separator", dest="separator", metavar='', help="the separator character")
    group.add_argument("-c", "--seplen", dest="separatorlength", type=int, metavar='', help="the length of characters between separator")
    group.add_argument("--repeat", dest="repeat", action='store_true', default=False, help="to repeat the characters in the password (default : %(default)s)")
    group.add_argument("--separation", dest="separation", default=False, action="store_true", help="to separate password characters using separator (default : %(default)s)")
    parser.add_argument_group(group)
    options = parser.parse_args()
    return options


def gen_Password(rep, separation, passlen=False, wanted=False, ign=False, inc=False, sep=False, seplen=False):
    arg = genpasswd.Password(length=passlen, only=wanted, ignore=ign, include=inc, repeat=rep, separator=sep, separator_length=seplen, separation=separation)
    passwd = arg.generate()
    return passwd


def main():
    options = get_argument()
    print(f"\n{gen_Password(options.repeat, options.separation, options.length, options.only, options.ignore, options.include, options.separator, options.separatorlength)}")


if __name__ == "__main__":
    main()
