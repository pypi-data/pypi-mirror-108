# MiProbe Python SDK 'MiProbe Lib' v0.5.26 - 20210527
# Author Evan Taylor - Evan@EvanTaylor.Pro
import urllib3
import serial
import serial.tools.list_ports
import argparse
import os
import math
import time
import pytz
import datetime
from decimal import Decimal
import simplejson as json
import csv
import io
import platform
import ast
from tqdm import tqdm
import flask
import logging
from re import search
import threading

urllib3.disable_warnings()

# Lock access to files until write is complete
file_lock = threading.Lock()
measurement_lock = threading.Lock()
data_lock = threading.Lock()

# Supported MiProbe System Boards
systemBoards = ['B10', 'B56', 'B56D', 'B176', 'B56D']

cloud_data = {}

commands = {
    "B176": {
        "ALLV": "N001,N002,N003,N004,N005,N006,N007,N008,N009,N010,N011,N012,N013,N014,N015,N016,N017,N018,N019,N020,N021,N022,N023,N024,N025,N026,N027,N028,N029,N030,N031,N032,N033,N034,N035,N036,N037,N038,N039,N040,N041,N042,N043,N044,N045,N046,N047,N048,N049,N050,N051,N052,N053,N054,N055,N056,N057,N058,N059,N060,N061,N062,N063,N064,N065,N066,N067,N068,N069,N070,N071,N072,N073,N074,N075,N076,N077,N078,N079,N080,N081,N082,N083,N084,N085,N086,N087,N088,N089,N090,N091,N092,N093,N094,N095,N096,N097,N098,N099,N100,N101,N102,N103,N104,N105,N106,N107,N108,N109,N110,N111,N112,N113,N114,N115,N116,N117,N118,N119,N120,N121,N122,N123,N124,N125,N126,N127,N128,N129,N130,N131,N132,N133,N134,N135,N136,N137,N138,N139,N140,N141,N142,N143,N144,N145,N146,N147,N148,N149,N150,N151,N152,N153,N154,N155,N156,N157,N158,N159,N160,N161,N162,N163,N164,N165,N166,N167,N168,N169,N170,N171,N172,N173,N174,N175,N176",
        "ALLVT": "N001,N002,N003,N004,N005,N006,N007,N008,N009,N010,N011,N012,N013,N014,N015,N016,N017,N018,N019,N020,N021,N022,N023,N024,N025,N026,N027,N028,N029,N030,N031,N032,N033,N034,N035,N036,N037,N038,N039,N040,N041,N042,N043,N044,N045,N046,N047,N048,N049,N050,N051,N052,N053,N054,N055,N056,N057,N058,N059,N060,N061,N062,N063,N064,N065,N066,N067,N068,N069,N070,N071,N072,N073,N074,N075,N076,N077,N078,N079,N080,N081,N082,N083,N084,N085,N086,N087,N088,N089,N090,N091,N092,N093,N094,N095,N096,N097,N098,N099,N100,N101,N102,N103,N104,N105,N106,N107,N108,N109,N110,N111,N112,N113,N114,N115,N116,N117,N118,N119,N120,N121,N122,N123,N124,N125,N126,N127,N128,N129,N130,N131,N132,N133,N134,N135,N136,N137,N138,N139,N140,N141,N142,N143,N144,N145,N146,N147,N148,N149,N150,N151,N152,N153,N154,N155,N156,N157,N158,N159,N160,N161,N162,N163,N164,N165,N166,N167,N168,N169,N170,N171,N172,N173,N174,N175,N176,T1,T2,T3,T4,T5",
        "ALLT": "T1,T2,T3,T4,T5"
    },
    "B176D": {
        "ALLV": "N001,N002,N003,N004,N005,N006,N007,N008,N009,N010,N011,N012,N013,N014,N015,N016,N017,N018,N019,N020,N021,N022,N023,N024,N025,N026,N027,N028,N029,N030,N031,N032,N033,N034,N035,N036,N037,N038,N039,N040,N041,N042,N043,N044,N045,N046,N047,N048,N049,N050,N051,N052,N053,N054,N055,N056,N057,N058,N059,N060,N061,N062,N063,N064,N065,N066,N067,N068,N069,N070,N071,N072,N073,N074,N075,N076,N077,N078,N079,N080,N081,N082,N083,N084,N085,N086,N087,N088,N089,N090,N091,N092,N093,N094,N095,N096,N097,N098,N099,N100,N101,N102,N103,N104,N105,N106,N107,N108,N109,N110,N111,N112,N113,N114,N115,N116,N117,N118,N119,N120,N121,N122,N123,N124,N125,N126,N127,N128,N129,N130,N131,N132,N133,N134,N135,N136,N137,N138,N139,N140,N141,N142,N143,N144,N145,N146,N147,N148,N149,N150,N151,N152,N153,N154,N155,N156,N157,N158,N159,N160,N161,N162,N163,N164,N165,N166,N167,N168,N169,N170,N171,N172,N173,N174,N175,N176",
        "ALLVT": "N001,N002,N003,N004,N005,N006,N007,N008,N009,N010,N011,N012,N013,N014,N015,N016,N017,N018,N019,N020,N021,N022,N023,N024,N025,N026,N027,N028,N029,N030,N031,N032,N033,N034,N035,N036,N037,N038,N039,N040,N041,N042,N043,N044,N045,N046,N047,N048,N049,N050,N051,N052,N053,N054,N055,N056,N057,N058,N059,N060,N061,N062,N063,N064,N065,N066,N067,N068,N069,N070,N071,N072,N073,N074,N075,N076,N077,N078,N079,N080,N081,N082,N083,N084,N085,N086,N087,N088,N089,N090,N091,N092,N093,N094,N095,N096,N097,N098,N099,N100,N101,N102,N103,N104,N105,N106,N107,N108,N109,N110,N111,N112,N113,N114,N115,N116,N117,N118,N119,N120,N121,N122,N123,N124,N125,N126,N127,N128,N129,N130,N131,N132,N133,N134,N135,N136,N137,N138,N139,N140,N141,N142,N143,N144,N145,N146,N147,N148,N149,N150,N151,N152,N153,N154,N155,N156,N157,N158,N159,N160,N161,N162,N163,N164,N165,N166,N167,N168,N169,N170,N171,N172,N173,N174,N175,N176,T1,T2,T3,T4,T5",
        "ALLT": "T1,T2,T3,T4,T5"
    },
    "B56": {
        "ALLV": "N01,N02,N03,N04,N05,N06,N07,N08,N09,N10,N11,N12,N13,N14,N15,N16,N17,N18,N19,N20,N21,N22,N23,N24,N25,N26,N27,N28,N29,N30,N31,N32,N33,N34,N35,N36,N37,N38,N39,N40,N41,N42,N43,N44,N45,N46,N47,N48,N49,N50,N51,N52,N53,N54,N55,N56",
        "ALLVT": "T1,T2,T3,T4,T5,N01,N02,N03,N04,N05,N06,N07,N08,N09,N10,N11,N12,N13,N14,N15,N16,N17,N18,N19,N20,N21,N22,N23,N24,N25,N26,N27,N28,N29,N30,N31,N32,N33,N34,N35,N36,N37,N38,N39,N40,N41,N42,N43,N44,N45,N46,N47,N48,N49,N50,N51,N52,N53,N54,N55,N56",
        "ALLT": "T1,T2,T3,T4,T5"
    },
    "B56D": {
        "ALLV": "N01,N02,N03,N04,N05,N06,N07,N08,N09,N10,N11,N12,N13,N14,N15,N16,N17,N18,N19,N20,N21,N22,N23,N24,N25,N26,N27,N28,N29,N30,N31,N32,N33,N34,N35,N36,N37,N38,N39,N40,N41,N42,N43,N44,N45,N46,N47,N48,N49,N50,N51,N52,N53,N54,N55,N56",
        "ALLVT": "T1,T2,T3,T4,T5,N01,N02,N03,N04,N05,N06,N07,N08,N09,N10,N11,N12,N13,N14,N15,N16,N17,N18,N19,N20,N21,N22,N23,N24,N25,N26,N27,N28,N29,N30,N31,N32,N33,N34,N35,N36,N37,N38,N39,N40,N41,N42,N43,N44,N45,N46,N47,N48,N49,N50,N51,N52,N53,N54,N55,N56",
        "ALLT": "T1,T2,T3,T4,T5"
    },
    "B10": {
        "ALL": "&NV1&NV2&NV3&NV4&NV5&NV6&NV7&NV8&NT1&NT2&NT3&NT4&NT5&NT6&NT7&NT8&SR1&SR2&SR3&SR4&SR5&SR6&SR7&SR8",
        "ALLV": "&NV1&NV2&NV3&NV4&NV5&NV6&NV7&NV8",
        "ALLVT": "&NV1&NV2&NV3&NV4&NV5&NV6&NV7&NV8&NT1&NT2&NT3&NT4&NT5&NT6&NT7&NT8"
    },
    "B12": {
        "ALL": "&NV1&NV2&NV3&NV4&NV5&NV6&NV7&NV8&NT1&NT2&NT3&NT4&NT5&NT6&NT7&NT8&SR1&SR2&SR3&SR4&SR5&SR6&SR7&SR8",
        "ALLV": "&NV1&NV2&NV3&NV4&NV5&NV6&NV7&NV8",
        "ALLVT": "&NV1&NV2&NV3&NV4&NV5&NV6&NV7&NV8&NT1&NT2&NT3&NT4&NT5&NT6&NT7&NT8"
    }
}

def xprint(*args, **kwargs):
    '''Print Wrapper to add timestamp and hostname to print or xprint() function.'''
    timestamp = str("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "]")
    hostname = str("[" + str(os.uname()[1]) + "]:")
    prefix = timestamp + hostname
    try:
        print(prefix, *args, **kwargs)
    except Exception:
        print(prefix, *args, **kwargs)


def default_config():
    settings = {
    "baud": None,
    "experimentname": None,
    "interval": None,
    "number": None,
    "offline": False,
    "port": None,
    "query": None,
    "timezone": None,
    "type": None
    }
    return settings


def read_config(filename):
    completeName = filename
    try:
        with open(completeName) as data:
            experimentDict = json.load(data)
            data.close()
            return experimentDict
    except FileNotFoundError:
        pass


def dict_to_csv(my_dict, filename):
    completeName = os.path.join(os.path.expanduser('~'), 'mp_data/', filename)
    file_lock.acquire()
    with open(completeName, 'a') as f:
        w = csv.DictWriter(f, my_dict.keys())
        if f.tell() == 0:
            w.writeheader()
            w.writerow(my_dict)
        else:
            w.writerow(my_dict)
    file_lock.release()


def csv_to_json(filename):
    data = []
    file_lock.acquire()
    with open(os.path.join(os.path.expanduser('~'), 'mp_data/', filename), 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for item in csvreader:
            data.append(item)
    return data
    file_lock.release()


def dict_to_jsonfile(my_dict, filename):
    file_lock.acquire()
    completeName = os.path.join(os.path.expanduser('~'), 'mp_data/', filename)
    with io.open(completeName, 'w', encoding='utf-8') as f:
        f.write(json.dumps(my_dict, ensure_ascii=False))
    file_lock.release()


def log_error(experimentName, errorfilename, error):
    ts = datetime.datetime.now()
    errorDict = {
        "Timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "Experiment": experimentName,
        "Error": str(error)
    }
    dict_to_csv(errorDict, errorfilename)


def upload_data(data_dict, api_key, api_url):
    timeout = urllib3.Timeout(connect=10.0, read=10.0)
    http = urllib3.PoolManager(timeout=timeout)
    payload = json.dumps(data_dict, indent=4, sort_keys=True)
    http.request('POST', api_url, headers={'Content-Type': 'application/json', 'x-api-key': api_key}, body=payload)


def timestamp(tz):
    tz = pytz.timezone(tz)
    utcnow = datetime.datetime.utcnow()
    ts = utcnow.replace(tzinfo=pytz.utc)
    lt = ts.astimezone(tz)

    time_dict = {
        "Timestamp": ts.strftime("%Y-%m-%d %H:%M:%S%z"),
        "LocalTime": lt.strftime("%Y-%m-%d %H:%M:%S%z"),
        "Datetime": int(ts.strftime("%s")) * 1000
    }
    return time_dict


# Function for converting system timezones to TZDB compatible ones.
def get_timezone():
    tz = str(time.tzname[time.daylight])
    if tz == ('PDT' or 'PST'):
        tz = "America/Los_Angeles"
    if tz == 'MDT':
        tz = "America/Denver"
    return tz


def querySleep():
    return .5


def miprober_init():
    global settings
    settings = default_config()
    parser = argparse.ArgumentParser(prog='miprober.py', description='MiProbe Python SDK "miprober" tool and associated mp_lib.py python module provide an easy to use data-logging tool and python library functions for automating real-time experiments. You must supply a board type (temporary), interval, and experiment name at minimum to use this tool.')
    parser.add_argument('-c', '--configfile', help='JSON configuration file of experiment settings.  Using this requires no additional parameters.', required=False)
    parser.add_argument('-e', '--experimentname', help='Experiment Name (e.g. "B56_Testing"). Require Option.', required=False)
    parser.add_argument('-t', '--type', help='Type of MiProbe Board (e.g. B10, B12, B56, B56D, B176).  Required option.', required=False)
    parser.add_argument('-i', '--interval', help='Measurement interval between readings in Seconds. Required option.', required=False)
    parser.add_argument('-p', '--port', help='Serial Port (e.g. COM1, /dev/ttyACM0, /dev/cu.usbmodem1 under Windows, Linux, and Mac respectively.)', required=False)
    parser.add_argument('-n', '--number', help='Number of readings (e.g. 42). Use 0 for continuous measurements (e.g. infinite).', required=False, default=0)
    parser.add_argument('-b', '--baud', help='Baud Rate.  Only use when working with prototype hardware or troubleshooting.  Miprober defaults to 38400 baud.', required=False, default=38400)
    parser.add_argument('-q', '--query', help='Query String.  (e.g. "&NV1&SR5" for B10 or B12 boards or "N01,N02,T1" for B56 boards and "N001,N002,T1" for B176 boards.). Will query all board inputs by default.', required=False)
    parser.add_argument('-z', '--timezone', help='Timezone. (e.g. "MST", "America/Los_Angeles").  Consult the list tzdb timezones on wikipedia for additional options.', required=False)
    parser.add_argument('-o', '--offline', help='Offline mode disables cloud logging. (e.g. "False", "True", 0, 1).  Default is 0 or False', required=False, default=0)
    args = vars(parser.parse_args())
    if args['configfile'] is not None:
        xprint("Loading special config file.")
        settings = read_config(args['configfile'])
        dict_to_jsonfile(settings, 'latest_config.json')
    else:
        xprint("No config file passed.  Loading configuration or arguments.")
        try:
            settings = dict(read_config(os.path.join(os.path.expanduser('~'), 'mp_data/', 'latest_config.json')))
            xprint("Loaded latest_config.json successfully.")
        except Exception:
            xprint("Could not load latest_config.json.  Processing Arguments.")
            if args is not None:
                if args['experimentname'] is None:
                    xprint("No Experiment Name specified. When passing arguments you must supply an Experiment Name, Board Type, and Measurement Interval.")
                    exit()
                if args['type'] is None:
                    xprint("No Board Type specified. When passing arguments you must supply an Experiment Name, Board Type, and Measurement Interval.")
                    exit()
                if args['interval'] is None:
                    xprint("No Measurement Interval specified. When passing arguments you must supply an Experiment Name, Board Type, and Measurement Interval.")
                    exit()
            if args is None:
                xprint("No arguments passed.  See miprober --help for more information.")
                exit()
            for i in args:
                if i != 'configfile':
                    if args[i] is not None:
                        settings[i] = str(args[i])
            if args['timezone'] is None:
                xprint("No Timezone argument.  Defaulting to system timezone: " + str(get_timezone()))
                settings['timezone'] = str(get_timezone())
            if args['offline'] == "True":
                settings['offline'] = bool(1)
            if args['offline'] == 1:
                settings['offline'] = bool(1)
            if args['offline'] == "False":
                settings['offline'] = bool(0)
            if args['offline'] == 0:
                settings['offline'] = bool(0)
            if args['query'] is None:
                xprint("No Query Command specified.  Defaulting to all sensor inputs.")
                settings['query'] = "ALLVT"
            dict_to_jsonfile(settings, 'latest_config.json')
        dict_to_jsonfile(settings, 'latest_config.json')
    return settings


def api_init():
    api_dict = {}
    try:
        with open(os.path.join(os.path.expanduser('~'), 'mp_data/', 'API.key')) as data:
            api_dict['api_key'] = data.read()
    except FileNotFoundError:
        xprint("No API key file found.")
        apikey = input("Enter API Key: ")
        api_dict['api_key'] = apikey
        with open(os.path.join(os.path.expanduser('~'), 'mp_data/', 'API.key'), 'w') as f:
            f.write(apikey)
        pass

    try:
        with open(os.path.join(os.path.expanduser('~'), 'mp_data/', 'API.url')) as data:
            api_dict['api_url'] = data.read()
    except FileNotFoundError:
        xprint("No API URL file found.")
        apiurl = input("Enter JSON POST API URL in quotes: ")
        api_dict['api_url'] = apiurl
        with open(os.path.join(os.path.expanduser('~'), 'mp_data/', 'API.url'), 'w') as f:
            f.write(apiurl)
        pass

    return api_dict


def serial_init(*args):
    global ser
    global serial_port
    serial_ports = serial.tools.list_ports.comports()
    board_ports = []

    for i, p in enumerate(serial_ports):
        if "ttyacm" in str(p).lower():  # Linux
            board_ports.append(str(p).split(" ")[0])
        if "cu.usbmodem" in str(p).lower():  # Mac OS X
            board_ports.append(str(p).split(" ")[0])
        if "U" in str(p):  # FreeBSD
            if "cuau" in str(p).lower():
                board_ports.append(str(p).split(" ")[0])
        if os.name == 'nt':  # Windows
            if "com" in str(p).lower():
                board_ports.append(str(p).split(" ")[0])

    if len(board_ports) == 0:
        xprint("No Serial Devices Found.  Check USB & Power Connections")
    elif len(board_ports) >= 2:
        xprint("Multiple devices found.  Please select MiProbe Serial Port.")
        xprint("Port Number\t" + "Port")
        for index, port in enumerate(board_ports):
            xprint(str(index) + " \t\t" + str(port))
        selected_port = int(input("Enter Port Number: "))
        serial_port = str(board_ports[selected_port])
    else:
        xprint("MiProbe Device found on port: " + str(board_ports[0]))
        serial_port = str(board_ports[0])
    if settings.get('baud') is None:
        baud_rate = 38400
    else:
        baud_rate = int(settings['baud'])

    ser = serial.Serial(serial_port, baud_rate)
    if ser.isOpen():
        ser.flushInput()
        ser.flushOutput()
        xprint("Serial connection established with MiProbe system board.")
    else:
        xprint("Cannot establish connection with " + str(serial_port) + ".")
        xprint("Check if another application is useding the serial port.")


def get_reading(experiment_name, command, tz):
    board = str(settings['type'])
    query_sleep = querySleep()
    if settings['type'] == "B10":
        command_unlock = "&LF1=1"
        ser.write(command_unlock.encode('ascii'))
        time.sleep(2)
        command_lab_mode = "&PI4=2"
        ser.write(command_lab_mode.encode('ascii'))
        time.sleep(2)
        ser.flushOutput()
        ser.flushInput()
        time.sleep(1)
    if settings['type'] == "B176":
        query_sleep = 3
    if command == "ALL":
        command = commands[board]['ALL']
    if command == "ALLVT":
        command = commands[board]['ALLVT']
    query = str("REQ[" + command + "]\r\n")
    measurement_lock.acquire()
    ser.write(query.encode('ascii'))
    time.sleep(query_sleep)
    response = str(ser.read(ser.inWaiting()).decode()).strip('\r\n')
    measurement_lock.release()
    if response.endswith(',') is True:
        response = response[:-1]
    time_info = timestamp(tz)
    if settings['type'] == "B10":
        response = response.strip("  Unlock_1 =1")
        readingsDict = ast.literal_eval(response)  # Test this on FreeBSD
    else:
        readingsList = list(map(Decimal, response.split(",")))
        readingsFieldsList = list(command.split(","))
        readingsDict = dict(zip(readingsFieldsList, readingsList))
    experimentDict = {"ExperimentName": experiment_name, "Timestamp": str(time_info['Timestamp']), "LocalTime": str(time_info['LocalTime']), "Datetime": time_info['Datetime']}
    item = dict(experimentDict, **readingsDict)

    ser.flushOutput()
    ser.flushInput()

    data = json.loads(json.dumps(item, indent=4, sort_keys=True, use_decimal=True), parse_float=Decimal)
    return data


def experiment_loop(board, experimentName, queryCommand, localTZ, experimentDict, api_dict, errorFilename, rawFilename, offlineMode, relay_status):
    global cloud_data
    cloud_data = {}
    key = str(api_dict['api_key'])
    status = relay_status
    try:
        getReading = get_reading(str(experimentName), queryCommand, localTZ)
        xprint("Reading Data from " + str(board))
        try:
            if status == "":
                try:
                    del getReading['Relay']
                except Exception as e:
                    pass
            else:
                getReading['Relay'] = str(status)
        except Exception as e:
            xprint("Error Logging Data: " + str(e))
            xprint("Could not parse relay status.")
            pass
        try:
            xprint("Writing Data to Disk...")
            dict_to_csv(getReading, rawFilename)
            xprint("Successfully wrote Data to Disk.")
        except Exception as e:
            xprint("Error Logging Data: " + str(e))
            log_error(experimentName, str(errorFilename), str(e))
            if search("Input/output error", str(e)):
                xprint("Reinitializing Serial Connection.  Possible loose cable.")
                serial_init()
            pass
        xprint(json.dumps(getReading, indent=4, sort_keys=True, use_decimal=True))
        # Preparing Cloud/Network Data
        data_lock.acquire()
        cloud_data['Data'] = getReading
        cloud_data['Settings'] = experimentDict
        cloud_data['Settings']['Hostname'] = str(platform.node())
        cloud_data['Settings']['LastReadingTime'] = str(getReading['LocalTime'])
        cloud_data['Settings']['LastReading'] = 0
        if int(offlineMode) == 0:
            try:
                xprint("Pushing Data to Cloud...")
                upload_data(cloud_data, key, api_dict['api_url'])
                xprint("Successfully Pushed Data to Cloud.")
            except Exception as e:
                xprint("Error Logging Data: " + str(e))
                log_error(experimentName, str(errorFilename), str(e))
                pass
        data_lock.release()
    except Exception as e:
        xprint("Error Logging Data: " + str(e))
        log_error(experimentName, str(errorFilename), str(e))
        if search("Input/output error", str(e)):
            xprint("Reinitializing Serial Connection.  Possible loose cable.")
            serial_init()
        pass


def run_experiment():
    # setup TQDM prefix
    timestamp = str("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "]")
    hostname = str("[" + str(os.uname()[1]) + "]: ")
    prefix = timestamp + hostname
    # Initialize Cloud Payload
    experimentDict = settings
    board = str(settings['type'])
    sensorReadings = int(settings['number'])
    experimentName = settings['experimentname']
    queryCommand = settings['query']
    readingInterval = int(settings['interval'])
    localTZ = settings['timezone']
    errorFilename = str("Error-" + str(experimentName) + str(".csv"))
    rawFilename = str(experimentName).replace(' ', '_') + str("-Data") + str(".csv")
    offlineMode = settings['offline']
    # use different function if using relays
    relay_status = ""

    if int(offlineMode) == 1:
        xprint("Miprober started in Offline Mode.  Data will only be logged to disk.")

    # Setup Loop for starting all logging at beginning of minute (XX:&&:00 seconds).
    now = time.localtime().tm_sec
    seconds = int(60 - now - querySleep())
    xprint(str("Waiting {} seconds until end of minute to start logging.").format(seconds))
    for i in tqdm(range(seconds), desc=str(str(prefix) + "Time Remaining"), total=seconds):
        time.sleep(1)
    if int(settings['number']) != 0:
        xprint("Running in fixed measurement mode.")
        # Initialize Main Loop Counter & Timer
        numberOfReadings = 0
        starttime = time.time()
        for i in tqdm(range(sensorReadings), desc=str(str(prefix) + "Fixed Mode: " + str(experimentName)), total=sensorReadings, initial=1, leave=False):
            experiment_loop(board, experimentName, queryCommand, localTZ, experimentDict, api_dict, errorFilename, rawFilename, offlineMode, relay_status)
            numberOfReadings = numberOfReadings + 1
            time.sleep(readingInterval - ((time.time() - starttime) % readingInterval))
            if (numberOfReadings >= sensorReadings):
                xprint("Readings Complete.  Stopping.")
                exit()
    if int(settings['number']) == 0:
        xprint("Running in continuous measurement mode.")
        while True:
            starttime = time.time()
            with tqdm(total=readingInterval, desc=str(str(prefix) + "∞ Mode: " + str(experimentName)), bar_format='{l_bar}{bar} | {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as t:
                experiment_loop(board, experimentName, queryCommand, localTZ, experimentDict, api_dict, errorFilename, rawFilename, offlineMode, relay_status)
                for i in range((int(math.floor(readingInterval - ((time.time() - starttime))))) - 1):
                    time.sleep(1)
                    t.update()
                time.sleep(readingInterval - ((time.time() - starttime) % readingInterval))


def setup_folders():
    if os.name != 'nt':
        if not os.path.exists(os.path.join(os.path.expanduser('~'), 'mp_data')):
            xprint("Creating mp_data folder to store local logs.")
            os.makedirs(os.path.join(os.path.expanduser('~'), 'mp_data'))
        else:
            xprint("Found mp_data folder in home folder.")


def start():
    setup_folders()
    global api_dict
    api_dict = api_init()


def server_init():
    app = flask.Flask(__name__)

    logging.getLogger('werkzeug').disabled = True
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'

    @app.route('/miprobe/latest/json', methods=['TRACE', 'GET'])
    def check_last_reading():
        xprint("Received latest reading request.  Sending last known readings.")
        data_lock.acquire()
        data = cloud_data  # Global from mp.experiment_loop()
        data_lock.release()
        response = flask.Response(response=json.dumps(data, indent=4, sort_keys=True), status=200, mimetype='application/json')
        return response

    @app.route('/miprobe/query/json', methods=['TRACE', 'GET'])
    def query_board():
        xprint("Received Query Request.  Querying Sensors and sending new measurements.")
        # Initialize Cloud Payload
        experimentDict = settings
        board = str(settings['type'])
        experimentName = settings['experimentname']
        queryCommand = settings['query']
        localTZ = settings['timezone']
        errorFilename = str("Error-" + str(experimentName) + str(".csv"))
        rawFilename = str(experimentName).replace(' ', '_') + str("-Data") + str(".csv")
        offlineMode = settings['offline']
        # use different function if using relays
        relay_status = ""
        experiment_loop(board, experimentName, queryCommand, localTZ, experimentDict, api_dict, errorFilename, rawFilename, offlineMode, relay_status)
        data = cloud_data  # Global from mp.experiment_loop()
        response = flask.Response(response=json.dumps(data, indent=4, sort_keys=True), status=200, mimetype='application/json')
        return response

    @app.route('/miprobe/dump/json', methods=['TRACE', 'GET'])
    def dump_json():
        xprint("Received JSON Dump request. Sending all known readings.")
        rawFilename = str(settings['experimentname']).replace(' ', '_') + str("-Data") + str(".csv")
        data = csv_to_json(rawFilename)
        response = flask.Response(response=json.dumps(data, indent=4, sort_keys=True), status=200, mimetype='application/json')
        return response

    @app.route('/miprobe/config', methods=['TRACE', 'GET'])
    def config():
        xprint("Received Configuration Request.  Sending current experiment configuration.")
        file_lock.acquire()
        data = read_config(os.path.join(os.path.expanduser('~'), 'mp_data/', 'latest_config.json'))
        file_lock.release()
        response = flask.Response(response=json.dumps(data, indent=4, sort_keys=True), status=200, mimetype='application/json')
        return response
    
    app.run(host='0.0.0.0')
