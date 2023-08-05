import logging

from dmsales.api_operations import APIOperations

logger = logging.getLogger(__name__)


class ContactCardEndpoints(APIOperations):

    def contact_card_details(self, project_id: str, base_key: str):
        '''
        Returns details about contact for given project_id and base_key.

        :param project_id: project_id
        :type project_id: str
        :param base_key: base_key
        :type base_key: str
        :return: details about contact
        :rtype: dict
        '''        
        endpoint = '/api/contact-card/'
        args_dict = {
            'project_id': project_id,
            'base_key': base_key
        }

        args_dict = {k: v for k, v in args_dict.items() if v} # exclude None args
        logger.debug('Calling contact_card details method')
        return super().make_get_request(endpoint, params=args_dict)

    def contact_card_add_note(self, project_id: str, base_key: str, content: str):
        '''
        Adds note to contact for given project_id and base_key.

        :param project_id: project_id
        :type project_id: str
        :param base_key: base_key
        :type base_key: str
        :param content: content of the note
        :type content: str
        :param tag: tag of the note
        :type tag: str
        :return: response for the post request
        :rtype: str
        '''        
        endpoint = '/api/contact-card/add-note'
        data = {
            'project_id': project_id,
            'base_key': base_key,
            'content': content
        }

        data = {k: v for k, v in data.items() if v} # exclude None args
        logger.debug('Calling add_note method')
        return super().make_post_request(endpoint, json=data)