import zipfile
import os


def arcZip(zip_path: str, obj_paths: list, extension: str = None):
    with zipfile.ZipFile(zip_path, 'w') as zipObj:
        for obj_path in obj_paths:
            if os.path.isfile(obj_path):
                zipObj.write(obj_path, arcname=os.path.basename(obj_path))

            elif os.path.isdir:
                for folder, subfolders, files in os.walk(obj_path):
                    for file in files:
                        if extension is not None:
                            if file.endswith(extension):
                                zipObj.write(os.path.join(folder, file),
                                             os.path.relpath(os.path.join(folder, file), obj_path))

                        else:
                            zipObj.write(os.path.join(folder, file),
                                         os.path.relpath(os.path.join(folder, file), obj_path))


def arcExtract(zip_path: str, ext_path: str, file_names: list = None):
    with zipfile.ZipFile(zip_path, 'r') as zipObj:
        if file_names is not None:
            for file in file_names:
                zipObj.extract(file, ext_path)
        else:
            zipObj.extractall(ext_path)
