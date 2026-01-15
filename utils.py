import h5py
import re
import typing

def extract_source_number(filename: str) -> int:
    match = re.search(r"source(\d+)", filename)
    return int(match.group(1)) if match else float("inf")  # if no match, send to end

def print_hdf5_structure(file_path: str) -> str:
    """
    Prints the structure of an HDF5 file: groups, datasets, and attributes.

    Parameters
    ----------
    file_path : str
        Path to the HDF5 file.
    """

    def print_attrs(name, obj):
        indent = "  " * (name.count("/") - 1)
        if isinstance(obj, h5py.Group):
            print(f"{indent}📂 Group: {name}")
        elif isinstance(obj, h5py.Dataset):
            print(f"{indent}📄 Dataset: {name}, shape={obj.shape}, dtype={obj.dtype}")
        else:
            print(f"{indent}❓ {name} (unknown type)")

        # Print attributes (if any)
        for key, val in obj.attrs.items():
            print(f"{indent}   ↳ Attribute: {key} = {val}")

    with h5py.File(file_path, "r") as f:
        print(f"File: {file_path}")
        f.visititems(print_attrs)

def get_hdf5_data(file: str, colname: str) -> typing.Any:
    """
    Get hdf5 data

    Parameters
    ----------
    file : str
        Path to HDF5 file.
    colname : str
        Column name

    Returns
    -------
        column data

    """
    with h5py.File(file, "r") as f:
        data = f[colname]
        return data[:]