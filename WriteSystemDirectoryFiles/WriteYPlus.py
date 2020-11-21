class WriteYPlus:
    def __init__(self, file_manager, flow_properties):
        self.file_manager = file_manager
        self.flow_properties = flow_properties

    def write_y_plus(self):
        file_id = self.file_manager.create_file('system', 'yPlus')
        self.file_manager.write(file_id,
                                '/*--------------------------------*- C++ -*----------------------------------*\\\n')
        self.file_manager.write(file_id,
                                '| =========                 |                                                 |\n')
        self.file_manager.write(file_id,
                                '| \\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n')
        self.file_manager.write(file_id,
                                '|  \\\    /   O peration     | Version:  ' + self.file_manager.get_version() +
                                '                                 |\n')
        self.file_manager.write(file_id,
                                '|   \\\  /    A nd           | Web:      www.OpenFOAM.com                      |\n')
        self.file_manager.write(file_id,
                                '|    \\\/     M anipulation  |                                                 |\n')
        self.file_manager.write(file_id,
                                '\*---------------------------------------------------------------------------*/\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, 'yPlus\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    type            yPlus;\n')
        self.file_manager.write(file_id, '    libs            (fieldFunctionObjects);\n')
        self.file_manager.write(file_id, '    writeControl    writeTime;\n')
        if len(self.flow_properties['wall_boundaries']) == 1:
            self.file_manager.write(file_id, '    patches         (' + self.flow_properties['wall_boundaries'][0] +
                                    ');\n')
        else:
            self.file_manager.write(file_id, '    patches         (')
            temp_str = ''
            for boundary in self.flow_properties['wall_boundaries']:
                temp_str += boundary + ' '
            self.file_manager.write(file_id, temp_str[:-1] + ');\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')