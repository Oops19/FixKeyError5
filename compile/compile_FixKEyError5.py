import re
import time

from Utilities.unpyc3_compiler import Unpyc3PythonCompiler

# This function invocation will compile the files found within Scripts/s4cl_sample_mod_scripts, put them inside of a file named s4cl_sample_mod.ts4script, and it will finally place that ts4script file within <Project>/Release/S4CLSampleMod.
import os
import shutil

config: dict = {
    "version": "0.1",  # f"_v{version}" will be appended to the name if set. Use even numbers for releases.
    "beta_version": "1",  # For odd numbers f"-test-build.{beta_version}" will be appended to the name if set.

    "ts4script_sub_folders": ["Mods", f"_o19_"],  # # TODO Modify the author name between '_' and delete to EOL ... f"_{ModInfo._author}_"
    "mod_zip_name": "FixKeyError5",  # f"{mod_zip_name}_v{version}-test-build.{beta_version}.zip TODO Modify 'mod_name' and delete to EOL ()  ... ModInfo._name
    "mod_ts4_name": "fix_key_error_5",  # f"{mod_ts4_name}.ts4script TODO Modify 'mod_name' and delete to EOL ()  ... ModInfo._base_namespace
    "source_folders": ('fix_key_error_5', ),  # TODO Modify 'source_folders' and delete to EOL

    "release_info_folder": None,  # "release_info",  # TODO set to None if none and delete to EOL
    "release_info_sub_folders": ['mod_data', 'mod_documentation'],  # Optionally add more or less sub folders.

    "release_folder_name": 'Release',  # Keep this as 'Release'
}

version = config.get('version')
beta_version = config.get('beta_version')
ts4script_sub_folders = config.get('ts4script_sub_folders')
mod_zip_name = config.get('mod_zip_name')
mod_ts4_name = config.get('mod_ts4_name')
source_folders = config.get('source_folders')
release_info_folder = config.get('release_info_folder')
release_info_sub_folders = config.get('release_info_sub_folders')
release_folder_name = config.get('release_folder_name')

release_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))), release_folder_name)
mod_base_directory = os.path.join(release_directory, mod_zip_name)
ts4script_directory = os.path.join(mod_base_directory, *ts4script_sub_folders)

zip_file_name = os.path.join(release_directory, mod_zip_name)
if version:
    zip_file_name = f"{zip_file_name}_v{version}"
    if re.match(r"^.*[13579]$", version):
        zip_file_name = f"{zip_file_name}-test-build.{beta_version}"

print(f"Creating {ts4script_directory}/{mod_ts4_name}.ts4script from {source_folders}")
print(f"Creating {zip_file_name}.zip")
if release_info_folder:
    print(f"    with documentation {release_info_folder}/{release_info_sub_folders}")
print(f"")
time.sleep(2)

os.makedirs(ts4script_directory, exist_ok=True)
Unpyc3PythonCompiler.compile_mod(
    names_of_modules_include = source_folders,
    folder_path_to_output_ts4script_to=ts4script_directory,
    output_ts4script_name=mod_ts4_name
)

if release_info_folder:
    doc_folder = os.path.join(os.path.dirname(os.path.abspath(os.getcwd())), release_info_folder)
    if os.path.exists(doc_folder):
        for folder in release_info_sub_folders:
            try:
                shutil.copytree(os.path.join(doc_folder, folder), os.path.join(mod_base_directory, folder))
            except:
                print(f"WARNING: Remove the folder {os.path.join(mod_base_directory, folder)} to update the data.")

shutil.make_archive(os.path.join(release_directory, f"{zip_file_name}"), 'zip', mod_base_directory)
print(f'Created {os.path.join(release_directory, f"{zip_file_name}.zip")}')