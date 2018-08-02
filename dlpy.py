import mimetypes
import os

import google.cloud.dlp

import requests


def inspect_file(project, filename, info_types,
                 custom_dictionaries=None, custom_regexes=None,
                 min_likelihood=None, max_findings=None,
                 include_quote=True, mime_type=None):

    dlp = google.cloud.dlp.DlpServiceClient()

    # I suppose in theory these could just be templates if
    # I understand the concept correctly.
    info_types = [{'name': info_types}]
    inspect_config = {
        'info_types': info_types,
        'min_likelihood': min_likelihood,
        'limits': {'max_findings_per_request': max_findings},
    }

    # I guess a mime_type, but I don't know why.
    if mime_type is None:
        mime_guess = mimetypes.MimeTypes().guess_type(filename)
        mime_type = mime_guess[0]

    supported_content_types = {
        None: 0,
    }
    content_type_index = supported_content_types.get(mime_type, 0)
    try:
        headers = {'Authorization': 'Bearer ' +
                   os.environ['TOKEN']}
        r = requests.get(filename, headers=headers, stream=True)
        with open(filename.split('/')[-1], 'wb') as f:
            f.write(r.content)
    except Exception as e:
        return e
    with open(filename.split('/')[-1], mode='rb') as f:
        item = {'byte_item': {'type': content_type_index, 'data': f.read()}}

    parent = dlp.project_path(project)
    response = dlp.inspect_content(parent, inspect_config, item)
    return response.result


def inspect_image():
    pass


def inspect_string(project, content_string, info_types,
                   custom_dictionaries=None, custom_regexes=None,
                   min_likelihood=None, max_findings=None, include_quote=True):

    dlp = google.cloud.dlp.DlpServiceClient()

    parent = dlp.project_path(project)
    item = {'value': content_string}
    info_types = [{'name': info_types}]
    max_findings = 0
    include_quote = True
    min_likelihood = 'LIKELIHOOD_UNSPECIFIED'
    inspect_config = {
        'info_types': info_types,
        'min_likelihood': min_likelihood,
        'include_quote': include_quote,
        'limits': {'max_findings_per_request': max_findings},
    }

    response = dlp.inspect_content(parent, inspect_config, item)
    return response


if __name__ == '__main__':
    inspect_string(
        'herpaderp-1', '702 Hemphill St, Ypsilanti MI 48198', 'ALL_BASIC')
