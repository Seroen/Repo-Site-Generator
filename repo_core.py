import os
from threading import Thread
import paths
import utils
utils.reset_dir("processed repo")

import lep_packer
import website


website.create_file_structure()

vanilla_thread = Thread(target=utils.recursive_zip, args=(f"{paths.dist_path}/Vanilla Pack.zip", [paths.input_vanilla]))
vanilla_thread.start()

resources_thread = Thread(target=utils.recursive_zip, args=(f"{paths.dist_path}/Resources.zip", [paths.input_graphics, paths.input_materials, paths.input_props]))
resources_thread.start()

materials_thread = Thread(target=utils.recursive_zip, args=(f"{paths.dist_path}/Materials.zip", [paths.input_materials]))
materials_thread.start()

import pack_maker
lep_packer.pack_templates()
lep_packer.pack_packs()
lep_packer.pack_regions()

website.process_thumbnails()
website.create_html()

#os.system("(( speaker-test -t sine -f 440 > /dev/null)& pid=$! ; sleep 0.1s ; kill -9 $pid > /dev/null) > /dev/null")

materials_thread.join()
print("[Materials] Materials zipped")
materials_thread.join()
print("[Resources] Resources zipped")
vanilla_thread.join()
print("[Vanilla Pack] Vanilla Pack zipped")
