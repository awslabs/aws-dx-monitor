# aws-dx-monitor - monitor DirectConnect and publish to CloudWatch
#
#   Copyright 2015-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# Author: Richard Elberger (elberger@amazon.com)

import logging
import botocore
import boto3
import json
from enum import Enum

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dxclient = boto3.client('directconnect')
cwclient = boto3.client('cloudwatch')

# The 'live' handler - from scheduler
def lambda_handler ( event, context ):
    ver_vistate  ( dxclient.describe_virtual_interfaces() )
    ver_cstate   ( dxclient.describe_connections() )
    ver_vpgstate ( dxclient.describe_virtual_gateways() )
    # Only DX Service Providers can make this call without an
    # exception
    #
    # ver_cistate( dxclient.describe_interconnects() )

# virtualInterfaces payload evaluation
def ver_vistate ( data ):
    if not 'virtualInterfaces' in data:
        logger.error("unexpected: virtualInterfaces key not found in data")
        return
    for iface in data['virtualInterfaces']:
        put_vistate( iface['virtualInterfaceId'],
                     VirtualInterfaceState[iface['virtualInterfaceState']].value )

# connections payload evaluation
def ver_cstate ( data ):
    if not 'connections' in data:
        logger.error("unexpected: connections key not found in data")
        return
    for conn in data['connections']:
        put_cstate( conn['connectionId'],
                    # Lookup int value in Connection enum
                    ConnectionState[conn['connectionState']].value )

# interconnect payload evaluation
def ver_cistate ( data ):
    if not 'interconnects' in data:
        logger.error("unexpected: interconnects key not found in data")
        return
    for intconn in data['interconnects']:
        put_icstate( intconn['interconnectId'],
                     # Lookup int value in IntConn enum
                     InterconnectState[intconn['interconnectState']].value )

# virtualgateway payload evaluation
def ver_vpgstate( data ):
    if not 'virtualGateways' in data:
        logger.error("unexpected: virtualGateways key not found in data")
        return
    for vpg in data['virtualGateways']:
        put_vpgstate( vpg['virtualGatewayId'],
                      # Lookup int value in VGW enum
                      VirtualGatewayState[vpg['virtualGatewayState']].value )

# Writes VirtualInterfaceState dimension data to DX custom metric
def put_vistate ( iid, state ):
    response = cwclient.put_metric_data(
        Namespace='AWSx/DirectConnect',
        MetricData=[
            {
                'MetricName': 'VirtualInterfaceState',
                'Dimensions': [
                    {
                        'Name': 'VirtualInterfaceId',
                        'Value': iid
                    },
                ],
                'Value': state,
                'Unit': 'None'
            },
        ],
    )

# Writes ConnectionState dimension data to DX custom metric
def put_cstate ( iid, state ):
    response = cwclient.put_metric_data(
        Namespace='AWSx/DirectConnect',
        MetricData=[
            {
                'MetricName': 'ConnectionState',
                'Dimensions': [
                    {
                        'Name': 'ConnectionId',
                        'Value': iid
                    },
                ],
                'Value': state,
                'Unit': 'None'
            },
        ],
    )

# Writes InterconnectState dimension data to DX custom metric
def put_icstate ( iid, state ):
    response = cwclient.put_metric_data(
        Namespace='AWSx/DirectConnect',
        MetricData=[
            {
                'MetricName': 'InterconnectState',
                'Dimensions': [
                    {
                        'Name': 'InterconnectId',
                        'Value': iid
                    },
                ],
                'Value': state,
                'Unit': 'None'
            },
        ],
    )

# Writes VGW dimension data to DX custom metric
def put_vpgstate ( iid, state ):
    response = cwclient.put_metric_data(
        Namespace='AWSx/DirectConnect',
        MetricData=[
            {
                'MetricName': 'VirtualGatewayState',
                'Dimensions': [
                    {
                        'Name': 'VirtualGatewayId',
                        'Value': iid
                    },
                ],
                'Value': state,
                'Unit': 'None'
            },
        ],
    )


class VirtualInterfaceState(Enum):
    confirming = 1
    verifying  = 2
    pending    = 3
    available  = 4
    down       = 5
    deleting   = 6
    deleted    = 7
    rejected   = 8

class ConnectionState(Enum):
    ordering   = 1
    requested  = 2
    pending    = 3
    available  = 4
    down       = 5
    deleting   = 6
    deleted    = 7
    rejected   = 8

class InterconnectState(Enum):
    requested  = 1
    pending    = 2
    available  = 3
    down       = 4
    deleting   = 5
    deleted    = 6

class VirtualGatewayState(Enum):
    pending    = 1
    available  = 2
    deleting   = 3
    deleted    = 4
