from trex.stl.api import *

class SetConfig:

    def set_rate(rate):
        pps = bps = percent = None
        if rate['choice'] == 'pps':
            pps = rate['pps']

        elif rate['choice'] == 'bps':
            bps = rate['bps']

        elif rate['choice'] == 'kbps':
            bps = rate['kbps'] * 1000

        elif rate['choice'] == 'mbps':
            bps = rate['mbps'] * 1000000

        elif rate['choice'] == 'gbps':
            bps = rate['gbps'] * 1000000000

        elif rate['choice'] == 'percentage':
            percent = rate['percentage']

        else:
            raise STLError('Invalid rate option')
        return pps, bps, percent

    
    def set_duration(duration, pps, bps, percent):
        if duration['choice'] == 'fixed_packets':
            mode = STLTXSingleBurst(
                total_pkts=duration['fixed_packets']['packets'], 
                pps=pps, bps_L2=bps, percentage=percent
            )

        elif duration['choice'] == 'fixed_seconds':
            raise STLError('T-Rex does not support fixed_seconds duration option')

        elif duration['choice'] == 'continuous':
            mode = STLTXCont(pps=pps, bps_L2=bps, percentage=percent)

        elif duration['choice'] == 'burst':
            mode = STLTXMultiBurst(
                pkts_per_burst=duration['burst']['packets'],
                ibg=duration['burst']['gap'],
                count=duration['burst']['bursts'],
                pps=pps, bps_L2=bps, percentage=percent)

        else:
            raise STLError('Invalid duration option')

        return mode

    
    def set_packet_headers(packet_headers):
        vmCmds = []
        layerCnt = {} # Counts the occurrences of each layer
        layers = [] # Keeps track of all of the layers in order
        pkt_headers = []
        for i, header in enumerate(packet_headers):

            # ETHERNET HEADER FIELDS CONFIGURATION
            if header['choice'] == 'ethernet':
                pkt_headers.append(Ether())
                layers.append('Ether')
                layerCnt['Ether'] = layerCnt['Ether']+1 if 'Ether' in layerCnt else 1

                if 'src' in header['ethernet']:
                    vmCmds += valueoptions.getMACValueCmds(
                        'Ethernet', layerCnt['Ether'], header['ethernet']['src'], 'src', 0
                    )

                if 'dst' in header['ethernet']:
                    vmCmds += valueoptions.getMACValueCmds(
                        'Ethernet', layerCnt['Ether'], header['ethernet']['dst'], 'dst', 0
                    )
                
                
            # IPv4 HEADER FIELDS CONFIGURATION
            elif header['choice'] == 'ipv4':
                vmCmds = []
                pkt_headers.append(IP())
                layers.append('IP')
                layerCnt['IP'] = layerCnt['IP']+1 if 'IP' in layerCnt else 1

                if 'src' in header['ipv4']:
                    vmCmds += valueoptions.getValueCmds(
                        'IP', layerCnt['IP'], header['ipv4']['src'], 32, 'src', 0
                    )

                if 'dst' in header['ipv4']:
                    vmCmds += valueoptions.getValueCmds(
                        'IP', layerCnt['IP'], header['ipv4']['dst'], 32, 'dst', 0
                    )

            
            # UDP HEADER FIELDS CONFIGURATION
            elif header['choice'] == 'udp':
                pkt_headers.append(UDP())
                layers.append('UDP')
                layerCnt['UDP'] = layerCnt['UDP']+1 if 'UDP' in layerCnt else 1

                if 'src_port' in header['udp']:
                    vmCmds += valueoptions.getValueCmds(
                        'UDP', layerCnt['UDP'], header['udp']['src_port'], 16, 'sport', 0
                    )

                if 'dst_port' in header['udp']:
                    vmCmds += valueoptions.getValueCmds(
                        'UDP', layerCnt['UDP'], header['udp']['dst_port'], 16, 'dport', 0
                    )

            # TCP HEADER FIELDS CONFIGURATION
            elif header['choice'] == 'tcp':
                pkt_headers.append(TCP())
                layers.append('TCP')
                layerCnt['TCP'] = layerCnt['TCP']+1 if 'TCP' in layerCnt else 1

                if 'src_port' in header['tcp']:
                    vmCmds += valueoptions.getValueCmds(
                        'TCP', layerCnt['TCP'], header['tcp']['src_port'], 16, 'sport'
                    )

                if 'dst_port' in header['tcp']:
                    vmCmds += valueoptions.getValueCmds(
                        'TCP', layerCnt['TCP'], header['tcp']['dst_port'], 16, 'dport'
                    )

            else:
                raise STLError('Invalid packet header option')

        return pkt_headers, vmCmds


    def set_packet_size(fSize):
        vmCmds = []
        if fSize['choice'] == 'increment':
            needsTrim = True
            start = fSize['increment']['start']
            maxPktSize = end = fSize['increment']['end']
            step = fSize['increment']['step']
            vmCmds.append(STLVmFlowVar(name = 'pkt_len', size = 2, op = 'inc', step = step,
                                            min_value = start,
                                            max_value = end))

        elif fSize['choice'] == 'random':
            needsTrim = True
            start = fSize['random']['min']
            maxPktSize = end = fSize['random']['max']
            vmCmds.append(STLVmFlowVar(name = 'pkt_len', size = 2, op = 'random',
                                            min_value = start,
                                            max_value = end))

        elif fSize['choice'] == 'fixed':
            needsTrim = False
            maxPktSize = fSize['fixed']

        else:
            raise STLError('Invalid packet size option')
        
        # Trim packets if needed
        if needsTrim:
            vmCmds.append(STLVmTrimPktSize('pkt_len'))
            layersWithLen = {'IP': 0, 'UDP': 0, 'TCP': 0}
            for i, layer in enumerate(layers):
                if layer in layersWithLen:
                    pkt_offset = "{0}:{1}.len".format(layer, layersWithLen[layer])
                    vmCmds.append(STLVmWrFlowVar(fv_name='pkt_len',
                                                pkt_offset=pkt_offset,
                                                add_val=len(pkt_base[i])-len(pkt_base)
                    ))
                    layersWithLen[layer] += 1