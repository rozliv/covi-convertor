import sys
from covi_convertor import force_to_csv, pressure_to_csv, force_pressure_to_csv


def get_folder_path(name):
    return f'{name}/Robots/Data/Data/Data'


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)

    data_type = int(sys.argv[1])
    output_name = sys.argv[2]
    project_name = '.'
    use_path = False
    if len(sys.argv) > 3:
        project_name = sys.argv[3]
        if len(sys.argv) > 4:
            use_path = int(sys.argv[4]) == 1

    path = get_folder_path(project_name) if use_path else project_name
    if data_type == 0:
        force_to_csv(path, output_name)
    elif data_type == 1:
        pressure_to_csv(path, output_name, filetype='csv')
    else:
        force_pressure_to_csv(path, output_name, filetype='csv')
