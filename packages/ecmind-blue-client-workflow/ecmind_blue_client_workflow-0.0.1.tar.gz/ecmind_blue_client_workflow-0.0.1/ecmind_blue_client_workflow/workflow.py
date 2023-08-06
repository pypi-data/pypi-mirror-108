from ecmind_blue_client import Job
from ecmind_blue_client import Client
from XmlElement import XmlElement


def get_organisations(client:Client, only_active:bool=True):
    result_get_organisations = client.execute(Job(jobname='wfm.GetOrganisations'))
    if not result_get_organisations.return_code == 0:
        raise RuntimeError(result_get_organisations.error_message)

    organisations = XmlElement.from_string(result_get_organisations.values['Organisations']).to_dict()['Organisation']

    if not isinstance(organisations, list):
        organisations = [ organisations ]

    if only_active:
        return { o['@Id']: o['@Name'] for o in organisations if o['@Active'] == 1 }
    else:
        return { o['@Id']: o['@Name'] for o in organisations }
