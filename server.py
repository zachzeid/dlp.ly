import os

from beautifultable import BeautifulTable

import dlpy

from slackclient import SlackClient

from slackeventsapi import SlackEventAdapter


slack_events_adapter = SlackEventAdapter(
    os.environ['SLACK_VERIFICATION_TOKEN'], '/slack/events')
CLIENT = SlackClient(os.environ['TOKEN'])


def format_message_to_table(message):
    table = BeautifulTable()
    table.column_headers = ['info_type', 'finding']

    for msg in message.findings:
        table.append_row([msg.info_type.name, msg.likelihood])

    return table


@slack_events_adapter.on('message')
def handle_message(event_data):
    message = event_data['event']
    if message.get('files'):
        file_link = message['files'][0]['url_private']
        channel = message['channel']
        message = "This is a file isn't it? < @{}>!: tada:".format(
            message['user'])
        check_file = dlpy.inspect_file(os.environ['PROJECT'],
                                       file_link, 'ALL_BASIC')
        msg_to_table = format_message_to_table(check_file)
        print(msg_to_table)
        CLIENT.api_call('chat.postMessage', channel=channel, text=msg_to_table)


slack_events_adapter.start(port=3000)
