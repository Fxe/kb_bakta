# -*- coding: utf-8 -*-
#BEGIN_HEADER
import json
import logging
import os
from pathlib import Path

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil
#END_HEADER


class kb_bakta:
    '''
    Module Name:
    kb_bakta

    Module Description:
    A KBase module: kb_bakta
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:Fxe/kb_bakta.git"
    GIT_COMMIT_HASH = "0987738bd55827d0d9177962eea817b937d47e3e"

    #BEGIN_CLASS_HEADER

    @staticmethod
    def run_bakta(features: dict,
                          output: Path = Path('/tmp/output'),
                          tmp_protein_faa: Path = Path('/tmp/input_genome.faa')) -> Path:

        with open(tmp_protein_faa, 'w') as fh:
            for i, s in features.items():
                fh.write(f'>{i}\n')
                fh.write(f'{s}\n')

        print(f'{tmp_protein_faa} created')

        print(os.listdir('/data/db'))
        threads = 40
        # Build cmd
        cmd = [
            'bakta_proteins',
            '--threads', str(threads),
            '--db', '/data/db',
            '--output', str(output),
            str(tmp_protein_faa),
        ]

        import subprocess
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        if output.exists() and output.is_dir():
            for f in os.listdir(output):
                print('created:', f)

        print(result)

        print(result.returncode)
        print(result.stdout.strip() if result.stdout else '')
        print(result.stderr.strip() if result.stderr else '')

        return output

    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.dfu = DataFileUtil(self.callback_url)
        #END_CONSTRUCTOR
        pass


    def run_kb_bakta(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_kb_bakta

        print(params)
        print(ctx)

        dfu_get_result = self.dfu.get_objects({'object_refs': [f'{params["workspace_id"]}/{params["input_genome"]}']})
        genome_object = dfu_get_result['data'][0]['data']

        features = {}

        for f in genome_object['features']:
            protein_translation = f.get('protein_translation')
            feature_id = f['id']
            if protein_translation:
                if feature_id not in features:
                    features[feature_id] = protein_translation
                else:
                    raise ValueError('Duplicate feature id:', feature_id)

        self.run_bakta(features)

        with open('/tmp/output/input_genome.json', 'r') as fh:
            annotation = json.load(fh)
            print(annotation)

        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created': [],
                                                'text_message': params['input_genome']},
                                                'workspace_name': params['workspace_name']})
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_kb_bakta

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_kb_bakta return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def annotate_proteins(self, ctx, proteins):
        """
        :param proteins: instance of mapping from String to String
        :returns: instance of mapping from String to unspecified object
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN annotate_proteins

        with open('/tmp/input_genome.faa', 'w') as fh:
            for i, s in proteins.items():
                fh.write(f'>{i}\n')
                fh.write(f'{s}\n')

        print('/tmp/input_genome.faa created')

        print(os.listdir('/data/db'))
        threads = 40
        # Build cmd
        cmd = [
            'bakta_proteins',
            '--threads', str(threads),
            '--db', '/data/db',
            '--output', f'/tmp/output',
            '/tmp/input_genome.faa',
        ]

        import subprocess
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        print(os.listdir('/tmp/output'))

        print(result)

        print(result.returncode)
        print(result.stdout.strip() if result.stdout else '')
        print(result.stderr.strip() if result.stderr else '')

        returnVal = {}
        with open('/tmp/output/input_genome.json', 'r') as fh:
            returnVal = json.load(fh)

        #END annotate_proteins

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method annotate_proteins return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
