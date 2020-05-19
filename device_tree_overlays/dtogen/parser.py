
import xml.etree.ElementTree as ET

from .node import *

def parser(sopc_file, existing_node, axi_master):
    """[summary]

    Parameters
    ----------
    sopc_file : str
        sopcinfo file name, ex. 'soc_system.sopcinfo'
    existing_node : str
        Name of existing device tree node to attach nodes to, ex. 'hps_bridges'
    axi_master : str
        AXI_master to parse memory blocks from, ex. 'h2f_lw'
    """
    tree = ET.parse(sopc_file)
    root = tree.getroot()

    
    bridges_root = root.find('./module/assignment[value="bridge"]/..')

    #print("test: " )
    #print(test.attrib)
    #root_axi = test.findtext('./parameter[@name="address_map"]/sysinfo_arg')
    #print( root_axi)
    #print("children:" )
    bridges_xml = bridges_root.findall('./interface[@kind="altera_axi_slave"]')
    bridges = {}
    bridge_counter = 0
    bridge_nodes = []
    for bridge in bridges_xml:
        #print(bridge.attrib)
        span = bridge.findtext("./assignment[name='addressSpan']/value")
        if(span != None):         
            memoryblock = root.find(f".//memoryBlock[moduleName='{bridges_root.attrib['name']}'][slaveName='{bridge.attrib['name']}']")
            base = memoryblock.findtext('baseAddress')
            #print(hex(int(base)))
            bridge_link = bridge.attrib["name"].split("_", 1)[1]
            bridges[bridge_link] = bridge.attrib["name"]
            bridges[bridge.attrib["name"]] = [bridge_counter, base]
            
            bridge_nodes.append(MemoryBridgeNode(bridge.attrib["name"], base_addr=int(base), span=int(span), index=bridge_counter, label=bridge.attrib["name"]))
            bridge_counter += 1
    nodes = []
    fe_nodes = get_fe_nodes(root, bridges)
    for node in fe_nodes:
        bridge_nodes[node.index].add_children(node)
    nodes = bridge_nodes
    
    return [BridgeRootNode(bridges_root.attrib["name"], bridges_root.attrib["name"], children=nodes)]

def get_fe_nodes(root, bridges):
    
    fe_nodes = root.findall('./module/assignment[name="embeddedsw.dts.vendor"][value="fe"]/..')

    #print(fe_nodes)
    nodes = []
    for node in fe_nodes:
        primary_compatible = f"fe,{node.attrib['kind']}-{node.attrib['version']}"
        secondary_compatible = node.findtext('./assignment[name="embeddedsw.dts.compatible"]/value')
        compatible = f"\"{primary_compatible}\", \"{secondary_compatible}\""
        #print(compatible)
        address_span_bits = node.findtext('./interface[@name="avalon_slave"]/parameter[@name="addressSpan"]/value')
        #print(address_span_bits)
        avalon_connection = root.find('./connection[@kind="avalon"][endModule="' + node.attrib["name"] + '"]')
        baseAddress = avalon_connection.findtext('./parameter[@name="baseAddress"]/value')
        #print(baseAddress)
        bridge = avalon_connection.findtext('./startConnectionPoint')
        #print(bridge)
        #print(bridges)
        link = bridges[bridge]
        bridge_info = bridges[link]
        nodes.append(MemoryMappedSlaveNode(label = node.attrib["name"], name= node.attrib["kind"], base_addr=int(baseAddress, 0), \
            span=int(address_span_bits), index=bridge_info[0], compatible=compatible\
            ))
    return nodes