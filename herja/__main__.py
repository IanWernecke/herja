import json
import logging
import os
import pprint

from .conversions import html_to_soup
from .decorators import MainCommands
from .net import Session, get_form_inputs
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
        (['group'], {'help': 'The name of the group whose events to read.'}),
        (['event_id'], {'help': 'The event id to query.'}),
        (['rsvp'], {
            'choices': ['yes', 'no'],
            'default': 'yes',
            'nargs': '?',
            'help': 'Set the confirmation to yes or no.'
        }),
        (['-d', '--debug'], {
            'action': 'store_true',
            'default': False,
            'help': 'Whether to dump the raw events for inspection.'
        })
    ]),
    ('test', 'Testing command.', [])
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

        with Session() as session:

            # authenticate
            response = session.get('https://secure.meetup.com/login/')
            logging.info(response)
            soup = html_to_soup(response.content)

            login_form = soup.find('form', {'id': 'loginForm'})
            assert login_form is not None, 'Failed to find login form.'

            inputs = get_form_inputs(login_form)
            with Settings() as settings:
                inputs['username'] = settings['meetup-username']
                inputs['password'] = settings['meetup-password']

            destination = login_form.attrs['action']
            response = session.post(destination, params=inputs)
            logging.info(response)

            # request the group page, if we are smart
            # GET https://www.meetup.com/VP_Boardgame_Club_at_Severna_Park/
            response = session.get('https://www.meetup.com/{0}/'.format(args.group))
            logging.info(response)
            response.content

            # rsvp to the event
            # https://www.meetup.com/VP_Boardgame_Club_at_Severna_Park/events/259097908/?action=rsvp&response=yes
            response = session.get('https://www.meetup.com/{0}/events/{1}/'.format(
                args.group, args.event_id
            ))
            logging.info(response)
            response.content

    return 0
