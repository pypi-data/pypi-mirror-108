# benamer (c) Baltasar 2021 MIT License <baltasarq@gmail.com>


import os
import argparse


name = "benamer"
description = "A bulk file and directory renaming tool."
__author__ = "Baltasar"
__version__= "00.01 serial 20210526"
HEADER = f"{name} v{__version__} (c) {__author__} - {description}\n"


def decompose_name_ext(nf):
    name = nf
    ext = ""
    
    dot_pos = name.find('.')
    if dot_pos >= 0:
        name = nf[:dot_pos]
        ext = nf[dot_pos:]
    
    return (name, ext)


def add_suffix(suffix, nf):
    name, ext = decompose_name_ext(nf)
    return name + suffix + ext


def add_count(i, nf):
    name, ext = decompose_name_ext(nf)
    return name + str(i) + ext

def substitute(sust, nf):
    if not sust[0]:
        sust[0], _ = decompose_name_ext(nf)

    return nf.replace(sust[0], sust[1])


def substitute_ext(new_ext, nf):
    name, ext = decompose_name_ext(nf)
    toret = name
    
    if (new_ext
    and new_ext[0] != '.'):
        new_ext = '.' + new_ext
        
    if new_ext:
        toret += new_ext

    return toret

def to_mays(nf):
    return nf.upper()

def to_mins(nf):
    return nf.lower()

def replace_spaces(nf):
    return nf.replace(" - ", "-").replace(' ', '_')


def add_prefix(prefix, nf):
    return prefix + nf


def remove_prefix(prefix, nf):
    return nf[len(prefix):] if nf.startswith(prefix) else nf


def remove_suffix(suffix, nf):
    name, ext = decompose_name_ext(nf)
    return name[:-len(suffix)] + ext if name.endswith(suffix) else nf


def walk_files(start_num, file_sust, transf_fn_list):
    for i, nf in enumerate(file_sust):
        for transf_fn in transf_fn_list:
                file_sust[nf] = transf_fn(start_num + i, file_sust[nf])


def rename_files(directory, file_sust):
    toret = 0
    
    for old_file_name in file_sust:
        old_file_path = os.path.join(directory, old_file_name)
        new_file_name = file_sust[old_file_name]
        
        if old_file_name != new_file_name:
            new_file_path = os.path.join(directory, new_file_name)
            os.rename(old_file_path, new_file_path)
            toret += 1
            
    return toret
            

def do_subst(file_list, args):
    transf_fn_list = []
    
    if not file_list:
        if args["verbose"]:
            print("No files.")
    else:
        # Sort and filter file list, if needed
        if args["sort"]:
            if args["verbose"]:
                print("Sorting file names...")

        file_list.sort()

        # Prepare substitutions
        file_sust = dict(zip(file_list, file_list))
        
        prefix_to_remove = args.get("remove_prefix")
        if prefix_to_remove:
            if args["verbose"]:
                print("Removing prefix:", prefix_to_remove)

            transf_fn_list.append(lambda i, nf: remove_prefix(prefix_to_remove, nf))
            
        suffix_to_remove = args.get("remove_suffix")
        if suffix_to_remove:
            if args["verbose"]:
                print("Removing suffix:", suffix_to_remove)

            transf_fn_list.append(lambda i, nf: remove_suffix(suffix_to_remove, nf))
            
        suffix_to_add = args.get("add_suffix")
        if suffix_to_add:
            if args["verbose"]:
                print("Adding suffix:", suffix_to_add)

            transf_fn_list.append(lambda i, nf: add_suffix(suffix_to_add, nf))
        
        prefix_to_add = args.get("add_prefix")
        if prefix_to_add:
            if args["verbose"]:
                print("Adding prefix:", prefix_to_add)

            transf_fn_list.append(lambda i, nf: add_prefix(prefix_to_add, nf))
            
        sust = args.get("sust")
        if sust:
            sust = sust.split('/')
            
            if len(sust) < 2:
                sust = (sust[0], "")
            
            if args["verbose"]:
                print(f"Substituting: \"{sust[0]}\"/\"{sust[1]}\"")

            transf_fn_list.append(lambda i, nf: substitute(sust, nf))
            
        new_ext = args.get("ext")
        if new_ext:
            if args["verbose"]:
                print(f"Change extension to: \"{new_ext}\"")

            transf_fn_list.append(lambda i, nf: substitute_ext(new_ext, nf))
            
        start_num = args.get("add_count")
        if start_num != None:
            if args["verbose"]:
                print(f"Adding count suffix, starting from: {start_num}")

            transf_fn_list.append(lambda i, nf: add_count(i, nf))
        else:
            start_num = 0
        
        if args.get("replace_spaces"):
            if args["verbose"]:
                print("Replacing spaces with '_'")

            transf_fn_list.append(lambda i, nf: replace_spaces(nf))
            
        if args.get("upper"):
            if args["verbose"]:
                print("Converting to upper...")

            transf_fn_list.append(lambda i, nf: to_mays(nf))
            
        if args.get("lower"):
            if args["verbose"]:
                print("Converting to lower...")

            transf_fn_list.append(lambda i, nf: to_mins(nf))
        
        walk_files(start_num, file_sust, transf_fn_list)

    return file_sust


def main():
    parser = argparse.ArgumentParser(
        description=description)
    parser.add_argument("-d", "--dir", default=".", 
                        help="set the directory to work with")
    parser.add_argument("-as", "--add-suffix", metavar="RPREFX",
                        help="add suffix to name")
    parser.add_argument("-ac", "--add-count", metavar="START",
                        type=int, help="add count suffix to name")
    parser.add_argument("-rs", "--remove-suffix", metavar="RSUFX",
                        help="remove suffix in name")
    parser.add_argument("-ap", "--add-prefix", metavar="RPREFX",
                        help="add prefix to name")
    parser.add_argument("-rp", "--remove-prefix", metavar="RPREFX",
                        help="remove prefix in name")
    parser.add_argument("-fe", "--filter_by_ext", metavar="FILTER_EXT",
                        help="filter by extension")
    parser.add_argument("-fp", "--filter_by_prefix", metavar="FILTER_PREFIX",
                        help="filter by prefix")
    parser.add_argument("-fs", "--filter_by_suffix", metavar="FILTER_SUFFIX",
                        help="filter by suffix")
    parser.add_argument("-st", "--sust", metavar="SUST",
                        help="substitute string")
    parser.add_argument("-e", "--ext", metavar="EXT",
                        help="substitute extension")
    parser.add_argument("-rsp", "--replace-spaces", action="store_true",
                        default=False,
                        help="replace spaces in files with underscores")
    parser.add_argument("-s", "--sort", action="store_true", default=False,
                        help="sort files before renaming")
    parser.add_argument("-p", "--print", action="store_true", default=False,
                        help="do nothing, just show renamings")
    parser.add_argument("-jd", "--directories", action="store_true",
                        default=False, help="rename only directories")
    parser.add_argument("-jf", "--files", action="store_true", default=False,
                        help="rename only files")
    parser.add_argument("-u", "--upper", action="store_true", default=False,
                        help="uppercase file names")
    parser.add_argument("-l", "--lower", action="store_true", default=False,
                        help="lowercase file names")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="describe what I am doing")
    args = vars(parser.parse_args())
    
    try:
        directory = args["dir"]
        
        # Retrieve file list
        file_list = [f for f in os.scandir(directory)]
        if args["files"]:
            file_list = [f.name for f in file_list if f.is_file()]
        elif args["directories"]:
            file_list = [f.name for f in file_list if f.is_dir()]
        else:
            file_list = [f.name for f in file_list]
            
        # Verbose
        if args["verbose"]:
            print(HEADER)
            print("Directory:", directory)
        
        # Do it
        file_sust = do_subst(file_list, args)
        if args.get("print"):
            print("\n" + str.join("\n", {f + "->" + file_sust[f] for f in file_sust}))
        else:
            num_files_renamed = rename_files(directory, file_sust)
            print("Files renamed:", num_files_renamed)

    except OSError as exc:
        print("OS complained:", str(exc))
    except Exception as exc:
        print("Unexpected error:", str(exc))


if __name__ == "__main__":
    main()
