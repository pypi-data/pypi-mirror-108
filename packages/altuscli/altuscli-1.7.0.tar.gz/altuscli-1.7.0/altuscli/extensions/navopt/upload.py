# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os

from altuscli import xform_name
from altuscli.extensions.commands import BasicCommand
from altuscli.extensions.generatecliskeleton import GenerateCliSkeletonArgument
from altuscli.formatter import get_formatter
import altuscli.thirdparty.requests as requests

HEADER_FIELD_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "coltype": {
                "type": "string",
                "description": "Type of the column",
                "enum": ["NONE", "SQL_ID", "SQL_QUERY", "ELAPSED_TIME"]
            },
            "use": {
                "type": "boolean",
                "description": "Specified will be used for computation."
            },
            "count": {
                "type": "integer",
                "description":
                    "Count the specified field."
            },
            "name": {
                "type": "string",
                "description": "The column name in csv file, header supplied in \
                            csv needs to be used to determine this."
            },
            "tag": {
                "type": "string",
                "description": "This is used to set custom column type."
            }
        }
    }
}


class UploadCommand(BasicCommand):
    NAME = 'upload'
    DESCRIPTION = BasicCommand.FROM_FILE()
    ARG_TABLE = [
        {
            'name': 'file-location',
            'no_paramfile': True,  # To disable the default paramfile behavior
            'required': True,
            'help_text': 'The location of the file that needs to be uploaded',
        },
        {
            'name': 'source-platform',
            'required': True,
            'help_text': (
                         'The source platform for the file that needs to'
                         'be uploaded'),
        },
        {
            'name': 'file-name',
            'help_text': (
                         'Name of the file, uploaded file will also have'
                         'same name'),
        },
        {
            'name': 'tenant',
            'required': True,
            'help_text': 'Unique id of the user doing the upload',
        },
        {
            'name': 'row-delim',
            'help_text': (
                         'The row delimiter if any for this file,'
                         'applicable in csv style file '),
        },
        {
            'name': 'col-delim',
            'help_text': (
                         'The column delimiter if any for this file,'
                         'applicable in csv style file.')
        },
        {
            'name': 'header-fields',
            'nargs': '+',
            'schema': HEADER_FIELD_SCHEMA,
            'help_text': (
                         'The per column header information associated with'
                         'csv style file.')
        }
    ]

    def __init__(self, prompter=None, config_writer=None):
        super(UploadCommand, self).__init__()
        self._operation_callers = []

    def _display_response(self, command_name, response, parsed_globals):
        output = parsed_globals.output
        if output is None:
            output = "json"
        formatter = get_formatter(output, parsed_globals)
        formatter(command_name, response)

    def _invoke(self,
                client,
                operation_name,
                parameters,
                parsed_args,
                parsed_globals):
        response = getattr(client, xform_name(operation_name))(**parameters)
        self._display_response(operation_name, response, parsed_globals)
        return response

    def update_call_parameters(self, call_parameters):
        json_str = call_parameters['cli_input_json']
        json_str = json_str.strip('\n')
        json_params = json.loads(json_str.replace("\n", ""))
        if 'fileLocation' in json_params and json_params['fileLocation']:
            call_parameters['file_location'] = json_params['fileLocation']
        if 'tenant' in json_params and json_params['tenant']:
            call_parameters['tenant'] = json_params['tenant']
        if 'fileName' in json_params and json_params['fileName']:
            call_parameters['file_name'] = json_params['fileName']
        if 'sourcePlatform' in json_params and json_params['sourcePlatform']:
            call_parameters['source_platform'] = json_params['sourcePlatform']
        if 'colDelim' in json_params and json_params['colDelim']:
            call_parameters['col_delim'] = json_params['colDelim']
        if 'rowDelim' in json_params and json_params['rowDelim']:
            call_parameters['row_delim'] = json_params['rowDelim']
        if 'headerFields' in json_params and json_params['headerFields']:
            call_parameters['header_fields'] = json_params['headerFields']
        return call_parameters

    def _run_main(self, client_creator, parsed_args, parsed_globals):
        if (client_creator is None) or (parsed_args is None):
            return False
        client = client_creator.create_client(
            'navopt',
            parsed_globals.endpoint_url,
            parsed_globals.verify_tls,
            client_creator.context.get_credentials())

        call_parameters = vars(parsed_args)
        if 'generate_cli_skeleton' in call_parameters and\
           call_parameters['generate_cli_skeleton']:
            generate_cli_skeleton_arg = GenerateCliSkeletonArgument(
                                        self.argument_model)
            return generate_cli_skeleton_arg.invoke(client,
                                                    None,
                                                    None,
                                                    parsed_args,
                                                    parsed_globals)

        if 'cli_input_json' in call_parameters and \
           call_parameters['cli_input_json']:
            # add params from call_parameters['cli_input_json']
            # to call_parameters
            call_parameters = self.update_call_parameters(call_parameters)

        url_parameters = {'fileName': '', 'tenant': ''}
        if 'file_name' in call_parameters and call_parameters['file_name']:
            url_parameters['fileName'] = call_parameters['file_name']
        elif 'file_location' in call_parameters and call_parameters['file_location']:
            if os.path.isfile(call_parameters['file_location']):
                fileName = os.path.basename(call_parameters['file_location'])
                url_parameters['fileName'] = fileName

        if 'tenant' in call_parameters and call_parameters['tenant']:
            url_parameters['tenant'] = call_parameters['tenant']
        response = self._invoke(client,
                                "getS3url",
                                url_parameters,
                                parsed_args,
                                parsed_globals)
        if response:
            # upload file to S3 bucket
            if 'url' in response and 'file_location' in call_parameters\
               and call_parameters['file_location']:
                requests.put(response['url'],
                             data=open(call_parameters['file_location']).read())
            # build upload parameters
            upload_params = {'rowDelim': '', 'colDelim': '', 'headerFields': [],
                             'tenant': '', 'fileType': 0}
            if 'tenant' in call_parameters and call_parameters['tenant']:
                upload_params['tenant'] = call_parameters['tenant']
            if 'file_location' in call_parameters:
                upload_params['fileLocation'] = call_parameters['file_location']
                if os.path.isfile(call_parameters['file_location']):
                    fileName = os.path.basename(call_parameters['file_location'])
                    upload_params['fileName'] = fileName
            if 'source_platform' in call_parameters:
                upload_params['sourcePlatform'] = call_parameters['source_platform']
            if 'header_fields' in call_parameters and call_parameters['header_fields']:
                upload_params['headerFields'] = call_parameters['header_fields']
            if 'file_name' in call_parameters and call_parameters['file_name']:
                upload_params['fileName'] = call_parameters['file_name']
            if 'row_delim' in call_parameters and call_parameters['row_delim']:
                upload_params['rowDelim'] = call_parameters['row_delim']
            if 'col_delim' in call_parameters and call_parameters['col_delim']:
                upload_params['colDelim'] = call_parameters['col_delim']
            if 'file_type' in call_parameters and call_parameters['file_type']:
                upload_params['fileType'] = call_parameters['file_type']
            response = self._invoke(client,
                                    "upload",
                                    upload_params,
                                    parsed_args,
                                    parsed_globals)
            return True
