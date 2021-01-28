import csv
import struct
import binascii
import re
from pathlib import Path


def write_pressure_to_csv(data, csv_name, digits=2):
    r"""Save pressure data to csv file

    Parameters
    ----------
    data : list
        measured pressure data with shape (N,H,W) - Number of measurements, Height and Width of pressure image
    csv_name : str
        prefix name of output csv file
    digits : int
        rounding precision

    Returns
    -------
    """

    num_arrs = len(data)
    max_idx = 0
    for i in range(num_arrs):
        if len(data[i]) * len(data[i][0]) > max_idx:
            max_idx = len(data[i]) * len(data[i][0])
    with open(csv_name + '_pressure.csv', mode='w') as new_file:
        file = csv.writer(new_file, delimiter=';', quotechar='"')
        file.writerow(num_arrs * ['Pressure [N/cm2]'])
        line = num_arrs * ['']
        for i in range(num_arrs):
            line[i] = 'Dims {} x {}'.format(len(data[i]), len(data[i][0]))
        file.writerow(line)
        for idx in range(max_idx):
            line = num_arrs * ['']
            for i in range(num_arrs):
                if len(data[i]) * len(data[i][0]) > idx:
                    line[i] = '{0:{1}}'.format(data[i][idx // len(data[i][0])][idx % len(data[i][0])],
                                               '.' + str(digits) + 'f')
            file.writerow(line)


def write_pressure_to_txt(data, txt_name, digits=2):
    r"""Save pressure data to txt file

    Parameters
    ----------
    data : list
        measured pressure data with shape (N,H,W) - Number of measurements, Height and Width of pressure image
    txt_name : str
        prefix name of output txt file
    digits : int
        rounding precision

    Returns
    -------
    """

    num_arrs = len(data)
    for i in range(num_arrs):
        with open(txt_name + '_' + str(i + 1) + '_pressure.txt', mode='w') as new_file:
            for j in range(len(data[i])):
                for k in range(len(data[i][j])):
                    new_file.write('{0:{1}} '.format(data[i][j][k], '.' + str(digits) + 'f'))
                new_file.write('\n')


def write_force_to_csv(data, csv_name):
    r"""Save force data to csv file

    Parameters
    ----------
    data : list
        measured pressure data with shape (N,5000) - Number of measurements
    csv_name : str
        prefix name of output csv file

    Returns
    -------
    """

    with open(csv_name + '_force.csv', mode='w') as new_file:
        file = csv.writer(new_file, delimiter=';', quotechar='"')
        num_arrs = len(data)
        file.writerow(num_arrs * ['Time [s]', 'Force [N]'])
        for idx in range(len(data[0])):
            line = 2 * num_arrs * ['']
            for i in range(num_arrs):
                line[2 * i] = format(idx / 1000, '0.3f')
                line[2 * i + 1] = format(data[i][idx], 'd')
            file.writerow(line)


def load_pressure_from_covi(path, name):
    r"""Load pressure data from .covi file to 2D list

    Parameters
    ----------
    path : str
        path to file (folder name)
    name : str
        .covi file name

    Returns
    -------
    data : list
        measured pressure data with shape (H,W) - Height and Width of pressure image
    """

    data = []
    with open(f'{path}/{name}', 'rb') as f:
        hexdata = f.read().hex()
        height = struct.unpack('>h', binascii.unhexlify(hexdata[152:156]))[0]
        width = struct.unpack('>h', binascii.unhexlify(hexdata[160:164]))[0]
        values = hexdata[164:]
        for i in range(height):
            arr = []
            for j in range(width):
                idx = j + i * width
                arr.append(struct.unpack('>d', binascii.unhexlify(values[0 + idx * 16:16 + idx * 16]))[0] / 10000)
            data.append(arr)
    return data


def load_force_from_covi(path, name):
    r"""Load force data from .covi file to 1D list

    Parameters
    ----------
    path : str
        path to file (folder name)
    name : str
        .covi file name

    Returns
    -------
    data : list
        measured force data
    """

    start_seq = bytearray(b'\xFE\xF9\xDB\x22\xD0\xEA\x00\x00\x13\x88').hex()
    force_maxidx = 5000
    data = force_maxidx * [0]
    with open(f'{path}/{name}', 'rb') as f:
        hexdata = f.read().hex()
        start = hexdata.find(start_seq)
        values = hexdata[start + len(start_seq):]
        for i in range(force_maxidx):
            data[i] = int(struct.unpack('>d', binascii.unhexlify(values[0 + i * 16:16 + i * 16]))[0])
    return data


def get_files(folder, name, indexes=None):
    """Get all files with given name in given folder (and in given order)

    Parameters
    ----------
    folder : str
        path to files (folder name)
    name : str
        file name pattern
    indexes : list
        files order

    Returns
    -------
    list
        a list of file names
    """

    nums = []
    files = []
    for path in Path(folder).glob(name):
        numbers = [int(d) for d in re.findall(r'-?\d+', path.name)]
        nums.append(numbers[-1] - 1 if len(numbers) > 0 else -1)
        files.append(path.name)
    if indexes is not None:
        files = [x for _, x in sorted(zip(indexes, files))]
    else:
        files = [x for _, x in sorted(zip(nums, files))]
    return files


def pressure_to_csv(folder, output_name, digits=2, filetype='csv', indexes=None):
    """Load pressure data from .covi file and save to csv/txt file

    Parameters
    ----------
    folder : str
        The file location of the spreadsheet
    output_name : str
        prefix name of output file
    digits : int
        rounding precision
    filetype : str
        output file type - csv/txt - default csv
    indexes : list
        files order

    Returns
    -------
    """

    files = get_files(folder, '*Pressure measurement*.covi', indexes)
    pressure_data = []
    for i in range(len(files)):
        print('{0} from {1}'.format(i + 1, len(files)))
        pressure_data.append(load_pressure_from_covi(folder, files[i]))
    if filetype == 'txt':
        write_pressure_to_txt(pressure_data, output_name, digits)
    else:
        write_pressure_to_csv(pressure_data, output_name, digits)


def force_to_csv(folder, output_name, indexes=None):
    """Load force data from .covi file and save to csv file

    Parameters
    ----------
    folder : str
        The file location of the spreadsheet
    output_name : str
        prefix name of output file
    indexes : list
        files order

    Returns
    -------
    """

    files = get_files(folder, '*Force measurement*.covi', indexes)
    force_data = []
    for i in range(len(files)):
        print('{0} from {1}'.format(i + 1, len(files)))
        force_data.append(load_force_from_covi(folder, files[i]))
    write_force_to_csv(force_data, output_name)


def force_pressure_to_csv(folder, output_name, digits=2, filetype='csv', indexes=None):
    """Load force and pressure data from .covi file and save to csv/txt files

    Parameters
    ----------
    folder : str
        The file location of the spreadsheet
    output_name : str
        prefix name of output file
    digits : int
        rounding precision
    filetype : str
        output file type - csv/txt - default csv
    indexes : list
        files order

    Returns
    -------
    """

    files = get_files(folder, '*Force-pressure*.covi', indexes)
    force_data = []
    pressure_data = []
    for i in range(len(files)):
        subfolder = folder + '/' + files[i][:-5]
        print('{0} from {1}'.format(i + 1, len(files)))
        for path in Path(subfolder).glob('*Force measurement*.covi'):
            force_data.append(load_force_from_covi(subfolder, path.name))
        for path in Path(subfolder).glob('*Pressure measurement*.covi'):
            pressure_data.append(load_pressure_from_covi(subfolder, path.name))
    write_force_to_csv(force_data, output_name)
    if filetype == 'txt':
        write_pressure_to_txt(pressure_data, output_name, digits)
    else:
        write_pressure_to_csv(pressure_data, output_name, digits)
