""" ndndn DOT Graph parser """

import networkx as nx
import networkx.drawing.nx_agraph as nx_dot
import pygraphviz as pgv
import re, copy
import template

class GraphParser(object):
    def __init__(self):
        pass

    def parseGraph(self, dotFile):
        topologyGraph = nx_dot.read_dot(dotFile)
        return self.parseTopologyGraph(topologyGraph)

    def renderGraph(self, dotFile, renderFile):
        g = pgv.AGraph(dotFile)
        # try: 
        g.draw(renderFile, prog='dot')
        # except:
            # print "Failed rendering dot file ", dotFile, " into ", renderFile

    def parseTopologyGraph(self, graph):
        nodes = {}
        for graphNode in graph.nodes():
            node = self.parseGraphNode(graphNode, graph)
            if node:
                nodes[graphNode] = node
        producerNodes = [x for x in nodes.values() if x['type'] == 'producer']
        consumerNodes = [x for x in nodes.values() if x['type'] == 'consumer']
        
        # replace 'fetch_from' from a simple list of names to list of producer nodes objects
        for node in consumerNodes:
            fetchFromNodes = []
            for nodeName in node['fetch_from']:
                fetchFromNodes.append(next(x for x in producerNodes if x['name'] == nodeName))
            node['fetch_from'] = fetchFromNodes

        # figure out automatic routes registering by finding 
        # minimal shortest paths between consumers and producers they fetch from
        self.addRouting(graph, nodes)

        # add network shaping parameters
        self.addNetworkShaping(graph, nodes)

        return nodes

    def addNetworkShaping(self, graph, nodes):
        linkShapes = nx.get_edge_attributes(graph, 'label')
        for (node1,node2,_),shape in linkShapes.iteritems():
            linkShape = self.parseShapeLabel(shape)
            if linkShape:
                n1name = nodes[node1]['name']
                n2name = nodes[node2]['name']
                nodes[node1]['network_shape'][n2name] = linkShape
                nodes[node2]['network_shape'][n1name] = linkShape
    
    def parseShapeLabel(self, label):
        p = re.compile('((?P<lat>\d+)ms\s*)?((?P<loss>\d+)%\s*)?((?P<bw>\d+)kbit\s*)?')
        m = p.match(label)
        networkShape = {}
        if m:
            if m.group('lat'):
                networkShape['lat'] = m.group('lat')
            if m.group('loss'):
                networkShape['loss'] = m.group('loss')
            if m.group('bw'):
                networkShape['bw'] = m.group('bw')
        if len(networkShape):
            return networkShape
        return None

    def addRouting(self, graph, nodes):
        consumerNodes = [x for x in nodes.values() if x['type'] == 'consumer']
        undirectedGraph = nx.Graph(graph)
        for consumerNode in consumerNodes:
            for producerNode in consumerNode['fetch_from']:
                try:
                    prefix = producerNode['prefix']
                    path = nx.shortest_path(undirectedGraph, consumerNode['graph_node'], producerNode['graph_node'])
                    self.addRoutes(prefix, path, nodes)
                except (nx.exception.NetworkXNoPath):
                    print("No path between " + consumerNode['graph_node'] + " and " + producerNode['graph_node'])

    def addRoutes(self, prefix, path, nodes):
        idx = 1
        for source in path:
            if idx < len(path):
                sourceNode = nodes[source]
                target = nodes[path[idx]]['name']
                idx += 1
                if not prefix in sourceNode['routes']:
                    sourceNode['routes'][prefix] = []
                if not target in sourceNode['routes'][prefix]:
                    sourceNode['routes'][prefix].append(target)

    def parseGraphNode(self, graphNode, graph):
        nodeMark, nodeIdx = self.parseGraphNodeName(graphNode)
        allLabels = nx.get_node_attributes(graph, 'label')
        nodeLabel = allLabels[graphNode] if graphNode in allLabels else 'none'
        try:
            node = copy.deepcopy(template.NODE_TEMPLATES[nodeMark])
            node['name'] = nodeMark+str(nodeIdx)
            node['index'] = nodeIdx
            node['label'] = nodeLabel
            node['graph_node'] = graphNode
            if nodeMark == 'c':
                node = self.parseConsumerNode(node)
            if nodeMark == 'p':
                node = self.parseProducerNode(node)
            return node
        except (KeyError):
            print "Unknown node type: " + nodeMark + " for node " + graphNode
            return None

    def parseGraphNodeName(self, name):
        nodeMark = name.lower()[0]
        nodeIdx = int(name[1:])
        return nodeMark, nodeIdx

    def parseConsumerNode(self, node):
        label = node['label']
        fetchFrom = self.parseConsumerLabel(label)
        if fetchFrom:
            node['fetch_from'] = fetchFrom
            return node
        return None

    def parseConsumerLabel(self, label):
        p = re.compile('C\d+\s*<-\s*(?P<fetch_from>(P\d+\s*)+)')
        m = p.match(label)
        if m:
            fetchFrom = m.group('fetch_from')
            producers = []
            for mm in re.finditer(r'P\d+', fetchFrom):
                m,i = self.parseGraphNodeName(mm.group(0))
                producers.append(m+str(i))
            return producers

        print "Consumer label " + label + " was not recognized"
        return None


    def parseProducerNode(self, node):
        label = node['label']
        prefix = self.parseProducerLabel(label)
        if prefix:
            node['prefix'] = prefix
            return node
        return None

    def parseProducerLabel(self, label):
        p = re.compile('P\d+\s*:\s*(?P<prefix>.+)')
        m = p.match(label)  
        if m:
            prefix = m.group('prefix')
            return prefix
        print "Producer label " + label + " was not recognized"
        return None