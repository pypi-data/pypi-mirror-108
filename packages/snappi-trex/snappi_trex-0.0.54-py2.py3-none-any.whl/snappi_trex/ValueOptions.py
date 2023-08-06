"""
This file includes utility functions to calculate the
ending value of an incrementing variable. Each function
takes in a start value, step, and count. The function 
returns the minimum value, maximum value, add value, and
initial value
"""

import stl_path
from trex.stl.api import *


def getValueCmds(layerType, layerCnt, headerField, FieldLength, fieldStr, fixup):
    varname = "{0}{1}_{2}".format(layerType, layerCnt-1, fieldStr)
    vmCmds = []
    mask = getMask(FieldLength)

    if FieldLength > 32:
        numBytes = 8
    elif FieldLength > 16:
        numBytes = 4
    elif FieldLength > 8:
        numBytes = 2
    else:
        numBytes = 1

    # Handle every source port value option: Value, values, inc, dec
    if headerField['choice'] == 'value':
        add_val = convertToLong(headerField['value'], layerType)
        vmCmds.append(STLVmFlowVar(name=varname, size=numBytes,
            max_value=0, step=1, op='inc'
        ))

    elif headerField['choice'] == 'values':
        add_val = 0
        value_list = []
        for v in headerField['values']:
            value_list.append(convertToLong(v, layerType))
        vmCmds.append(STLVmFlowVar(name=varname, size=numBytes,
            value_list=value_list
        ))

    elif headerField['choice'] == 'increment':
        start = convertToLong(headerField['increment']['start'], layerType)
        step = headerField['increment']['step']
        cnt = headerField['increment']['count']
        minV, maxV, init, add_val = incValues(start,step,cnt,mask)
        vmCmds.append(STLVmFlowVar(name=varname, size=numBytes, init_value = init,
            min_value=minV, max_value=maxV, step=step, op='inc'
        ))

    elif headerField['choice'] == 'decrement':
        start = convertToLong(headerField['decrement']['start'], layerType)
        step = headerField['decrement']['step']
        cnt = headerField['decrement']['count']
        minV, maxV, init, add_val = incValues(start,-step,cnt,mask)
        vmCmds.append(STLVmFlowVar(name=varname, size=numBytes, init_value = init,
            min_value=minV, max_value=maxV, step=step, op='dec'
        ))

    else: 
        raise STLError('Invalid {0} operation'.format(varname))
    
    pkt_offset = "{0}:{1}.{2}".format(layerType, layerCnt-1, fieldStr)
    vmCmds.append(STLVmWrMaskFlowVar(fv_name=varname, 
                            pkt_cast_size=numBytes,
                            mask=mask,
                            pkt_offset=pkt_offset, 
                            offset_fixup=fixup,
                            add_value=add_val))

    # vmCmds.append(STLVmWrFlowVar(fv_name=varname, 
    #                         pkt_offset=pkt_offset, 
    #                         offset_fixup=fixup,
    #                         add_val=add_val))

    return vmCmds


def incValues(start, step, count, mask):

    if abs(step) * count > mask:
        raise STLError('incrementing/decrementing port count is too high. step*count must be less than 0xffff')

    if step < 0: # Decrementing
        step = -((-step) % mask)
        max = init = mask
        min = max + count * step
        add_val = (start + 1) % mask

    else: # Incrementing
        step = step % mask
        min = init = 0
        max = min + count * step
        add_val = start
    
    return (min, max, init, add_val)


def getMask(bits):
    mask = 0
    for x in range(bits):
        mask = mask << 1
        mask += 1
    return mask


def convertToLong(value, layerType):
    if layerType == 'IP':
        elements = value.split('.')
        result = 0
        for e in elements:
            result = result << 8
            if len(e) == 0:
                continue
            result += int(e)
        return result
    
    else: 
        return value