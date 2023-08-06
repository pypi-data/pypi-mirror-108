"""
This file includes utility functions to calculate the
ending value of an incrementing variable. Each function
takes in a start value, step, and count. The function 
returns the minimum value, maximum value, add value, and
initial value
"""

from snappi_trex import stl_path
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
        add_val = 0
        val = convertToLong(headerField['value'], layerType)
        vmCmds.append(STLVmFlowVar(name=varname, size=numBytes,
            min_value=val, max_value=val, step=1, op='inc'
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
        step = convertToLong(headerField['increment']['step'], layerType)
        cnt = headerField['increment']['count']
        minV, maxV, init, add_val = incValues(start,step,cnt,mask)
        vmCmds.append(STLVmFlowVar(name=varname, size=numBytes, init_value = init,
            min_value=minV, max_value=maxV, step=step, op='inc'
        ))

    elif headerField['choice'] == 'decrement':
        start = convertToLong(headerField['decrement']['start'], layerType)
        step = convertToLong(headerField['decrement']['step'], layerType)
        cnt = headerField['decrement']['count']
        minV, maxV, init, add_val = incValues(start,-step,cnt,mask)
        vmCmds.append(STLVmFlowVar(name=varname, size=numBytes, init_value = init,
            min_value=minV, max_value=maxV, step=step, op='dec'
        ))

    else: 
        raise STLError('Invalid {0} operation'.format(varname))
    
    pkt_offset = "{0}:{1}.{2}".format(layerType, layerCnt-1, fieldStr)
    if FieldLength <= 32:
        vmCmds.append(STLVmWrMaskFlowVar(fv_name=varname, 
                                pkt_cast_size=numBytes,
                                mask=mask,
                                pkt_offset=pkt_offset, 
                                offset_fixup=fixup,
                                add_value=add_val))
    else:
        ''''''

    return vmCmds

# Need specific function for Ethernet MAC addresses b/c STLVmWrFlowVar only supports 4 byte fields
def getMACValueCmds(layerType, layerCnt, headerField, fieldStr, fixup):
    varname1 = "{0}{1}_{2}".format(layerType, layerCnt-1, fieldStr)
    varname2 = varname1+'2'
    vmCmds = []

    # Handle every source port value option: Value, values, inc, dec
    if headerField['choice'] == 'value':
        add_val = 0
        val = convertToLong(headerField['value'], layerType)
        vmCmds.append(STLVmFlowVar(name=varname1, size=2,
            min_value=val>>32, max_value=val>>32, step=1, op='inc'
        ))
        vmCmds.append(STLVmFlowVar(name=varname2, size=4,
            min_value=val&0xffffffff, max_value=val&0xffffffff, step=1, op='inc'
        ))

    elif headerField['choice'] == 'values':
        add_val = 0
        value_list1 = []
        value_list2 = []
        for v in headerField['values']:
            value_list1.append(convertToLong(v, layerType) >> 32)
            value_list2.append(convertToLong(v, layerType) & 0xffffffff)
        vmCmds.append(STLVmFlowVar(name=varname1, size=2,
            value_list=value_list1
        ))
        vmCmds.append(STLVmFlowVar(name=varname2, size=4,
            value_list=value_list2
        ))

    elif headerField['choice'] == 'increment':
        start = convertToLong(headerField['increment']['start'], layerType)
        step = convertToLong(headerField['increment']['step'], layerType)
        cnt = headerField['increment']['count']
        minV, maxV, init, add_val = incValues(start,step,cnt,0xffffffffffff)
        vmCmds.append(STLVmFlowVar(name=varname1, size=2,
            min_value=start>>32, max_value=start>>32, step=1, op='inc'
        ))
        vmCmds.append(STLVmFlowVar(name=varname2, size=4, init_value = init&0xffffffff,
            min_value=minV&0xffffffff, max_value=maxV&0xffffffff, step=step&0xffffffff, op='inc'
        ))

    elif headerField['choice'] == 'decrement':
        start = convertToLong(headerField['decrement']['start'], layerType)
        step = convertToLong(headerField['decrement']['step'], layerType)
        cnt = headerField['decrement']['count']
        minV, maxV, init, add_val = incValues(start,-step,cnt,0xffffffffffff)
        vmCmds.append(STLVmFlowVar(name=varname1, size=2,
            min_value=start>>32, max_value=start>>32, step=1, op='dec'
        ))
        vmCmds.append(STLVmFlowVar(name=varname2, size=4, init_value = init&0xffffffff,
            min_value=minV&0xffffffff, max_value=maxV&0xffffffff, step=step&0xffffffff, op='dec'
        ))

    else: 
        raise STLError('Invalid {0} operation'.format(varname))
    
    pkt_offset = "{0}:{1}.{2}".format(layerType, layerCnt-1, fieldStr)
    vmCmds.append(STLVmWrMaskFlowVar(fv_name=varname1, 
                            pkt_cast_size=2,
                            mask=0xffff,
                            pkt_offset=pkt_offset, 
                            offset_fixup=fixup,
                            add_value=add_val>>32))
    vmCmds.append(STLVmWrMaskFlowVar(fv_name=varname2, 
                            pkt_cast_size=4,
                            mask=0xffffffff,
                            pkt_offset=pkt_offset, 
                            offset_fixup=fixup+2,
                            add_value=add_val&0xffffffff))
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
    if isinstance(value, int): 
        return value

    if layerType == 'IP':
        elements = value.split('.')
        result = 0
        for e in elements:
            result = result << 8
            if len(e) == 0:
                continue
            result += int(e)
        return result

    if layerType == 'Ethernet':
        elements = value.split(':')
        result = 0
        for e in elements:
            result = result << 8
            if len(e) == 0:
                continue
            result += int(e, 16)
        return result
    
    return value