from input import GlobalVariables as Parameters


class WriteFields:
    def __init__(self, properties, file_manager):
        self.file_manager = file_manager
        self.properties = properties

    def write_field(self):
        file_id = self.file_manager.create_file('system/include', 'fields')
        self.file_manager.write_header(file_id, 'dictionary', 'system', 'fields')
        self.file_manager.write(file_id, '\n')
        if self.properties['additional_fields']['write_additional_fields']:
            for field in self.properties['additional_fields']['fields']:
                name = ''
                if field == Parameters.Q:
                    name = 'Q'
                elif field == Parameters.LAMBDA_2:
                    name = 'Lambda2'
                elif field == Parameters.VORTICITY:
                    name = 'vorticity'
                elif field == Parameters.ENSTROPHY:
                    name = 'enstrophy'
                self.__write_custom_fields(file_id, name)
        if self.properties['iso_surfaces']['write_iso_surfaces']:
            self.file_manager.write(file_id, '// include iso-surface writing here (instead of in the controlDict)\n')
            self.file_manager.write(file_id, '// in case any of the additional computed fields above (if any)\n')
            self.file_manager.write(file_id, '// are used to generate iso-surfaces\n')
            self.file_manager.write(file_id, '#include "isoSurfaces"\n')
            self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id,
                                '// ************************************************************************* //\n')

    def __write_custom_fields(self, file_id, field_name):

        self.file_manager.write(file_id, field_name + '\n')
        self.file_manager.write(file_id, '{\n')
        self.file_manager.write(file_id, '    type            ' + field_name + ';\n')
        self.file_manager.write(file_id, '    libs            (fieldFunctionObjects);\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    writeControl    writeTime;\n')
        self.file_manager.write(file_id, '\n')
        self.file_manager.write(file_id, '    log             no;\n')
        self.file_manager.write(file_id, '}\n')
        self.file_manager.write(file_id, '\n')
