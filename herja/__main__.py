import json
import logging
import os
import pprint

from .conversions import html_to_soup
from .decorators import MainCommands
from .net import Session
from .settings import Settings


@MainCommands(
    ('meetup-events-list', 'List events for a specified meetup group.', [
        (['group'], {'help': 'The name of the group whose events to read.'}),
        (['-d', '--debug'], {
            'action': 'store_true',
            'default': False,
            'help': 'Whether to dump the raw events for inspection.'
        })
    ]),
    ('meetup-rsvps-list', 'List the people who have rsvped to an event.', [
        (['group'], {'help': 'The name of the group whose events to read.'}),
        (['event_id'], {'help': 'The event id to query.'}),
        (['-d', '--debug'], {
            'action': 'store_true',
            'default': False,
            'help': 'Whether to dump the raw events for inspection.'
        })
    ]),
    ('meetup-rsvp', 'RSVP to an event.', [
        (['event_id'], {'help': 'The event id to query.'}),
        (['-d', '--debug'], {
            'action': 'store_true',
            'default': False,
            'help': 'Whether to dump the raw events for inspection.'
        })
    ])
)
def main(args):
    """Handle arguments given to this module."""
    print(args)

    # load the meetup api token
    if args.command.startswith('meetup-'):
        with Settings() as settings:
            token = settings['meetup-api-token']
        meetup_api_params = {'sign': 'true', 'token': token}

    if args.command == 'meetup-events-list':

        # use a session to obtain information from meetup
        with Session() as session:
            response = session.get('https://api.meetup.com/{0}/events'.format(args.group), params=meetup_api_params)
            events = json.loads(response.content)
            for event in events:

                if args.debug:
                    pprint.pprint(event)
                    continue

                location = event['venue']['address_1']
                print((
                    '[{local_date} {local_time}:00]\n'
                    '  Event: {id}\n'
                    '  Name: {name}\n'
                    '  Location: {location}\n'
                    '  Attending: {yes_rsvp_count}\n'
                ).format(location=location, **event))

    if args.command == 'meetup-rsvps-list':

        # use a session to obtain information from meetup
        with Session() as session:
            # session.headers['Authorization'] = 'Bearer {0}'.format(token)
            response = session.get(
                'https://api.meetup.com/{0}/events/{1}/rsvps'.format(args.group, args.event_id),
                params=meetup_api_params
            )
            print(response.headers)
            rsvps = json.loads(response.content)
            for rsvp in rsvps:

                if args.debug:
                    pprint.pprint(rsvp)
                    continue

                print((
                    'Member: {member_id}\n'
                    'Name: {name}\n'
                    'Role: {role}\n'
                    'Attending: {response}\n'
                ).format(
                    member_id=rsvp['member']['id'],
                    name=rsvp['member']['name'],
                    role=rsvp['member']['role'] if 'role' in rsvp['member'] else 'None',
                    **rsvp
                ))

    if args.command == 'meetup-rsvp':

        meetup_api_params['event_id'] = args.event_id
        meetup_api_params['rsvp'] = 'yes'
        with Session() as session:
            response = session.post(
                'https://api.meetup.com/2/rsvp',
                params=meetup_api_params
            )
            print(response)
            print(response.status_code)
            print(response.content)

    return 0
