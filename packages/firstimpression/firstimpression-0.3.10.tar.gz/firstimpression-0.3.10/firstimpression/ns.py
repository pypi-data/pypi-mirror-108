import requests
from datetime import datetime


def get_departures(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    response_json = response.json()

    if response_json.get('statusCode', None) == 429:
        raise Exception('Rate limit exceeded')

    departures = response_json['payload']['departures']

    return departures


def get_stations(url, headers):
    response = requests.get(url, headers=headers)
    response_json = response.json()

    return response_json


def get_departure_number(departure):
    return departure['product']['number']


def parse_departure_time(datetime_object):
    return str(datetime.strftime(datetime_object, "%H:%M"))


def get_departure_time(departure):
    departure_Time = datetime.strptime(
        departure['plannedDateTime'][:-5], '%Y-%m-%dT%H:%M:%S')
    return str(datetime.strftime(departure_Time, '%Y-%m-%dT%H:%M:%S'))


def get_destination(departure):
    return departure['direction']


def get_train_category(departure):
    return departure['product']['longCategoryName']


def get_route_text(departure):
    # Returns string with stations on route in this format: '{station}, {station}, {station}'
    return ', '.join([station['mediumName'] for station in departure['routeStations']])


def get_operator(departure):
    return departure['product']['operatorName']


def get_planned_track(departure):
    return departure['plannedTrack']


def get_actual_track(departure):
    return departure.get('actualTrack', '')


def get_delay(departure):
    try:
        if departure['cancelled'] == True:
            return 'Rijdt niet'
    except KeyError:
        pass

    plannedDepartureTime = datetime.strptime(
        departure['plannedDateTime'][:-5], '%Y-%m-%dT%H:%M:%S')
    actualDepartureTime = datetime.strptime(
        departure['actualDateTime'][:-5], '%Y-%m-%dT%H:%M:%S')

    if plannedDepartureTime < actualDepartureTime:
        delayedTime = actualDepartureTime - plannedDepartureTime
        delayedTimeSplit = str(delayedTime).split(':')
        delayedMinutes = int(
            delayedTimeSplit[0]) * 60 + int(delayedTimeSplit[1])
        if int(delayedTimeSplit[2]) > 30:
            delayedMinutes += 1
        return ''.join(['+', str(delayedMinutes), ' min'])
    else:
        return ''


def get_message(departure):
    try:
        message = departure.get('messages', False)
        if message:
            msg = message[0]['message']
        else:
            msg = ''
    except KeyError:
        msg = ''
    return msg


def get_parsed_departures(url, header, params):
    departures = get_departures(url, header, params)
    parsed_departures = list()
    for departure in departures:
        parsed_departure = dict()
        parsed_departure['departure_number'] = get_departure_number(departure)
        parsed_departure['departure_time'] = get_departure_time(departure)
        parsed_departure['destination'] = get_destination(departure)
        parsed_departure['train_category'] = get_train_category(departure)
        parsed_departure['route_text'] = get_route_text(departure)
        parsed_departure['operator'] = get_operator(departure)
        parsed_departure['planned_track'] = get_planned_track(departure)
        parsed_departure['actual_track'] = get_actual_track(departure)
        parsed_departure['delay'] = get_delay(departure)
        parsed_departure['message'] = get_message(departure)
        parsed_departures.append(parsed_departure)

    return parsed_departures
