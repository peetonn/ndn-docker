""" ndnd YML writer """

import yaml, os

class YmlWriter(object):
    def __init__(self, nodes, consumerEnv, producerEnv):
        self.nodes = nodes
        self.cenv = consumerEnv
        self.penv = producerEnv

    def makeYml(self):
        yml = { 'version': '3', 'services': {} }
        producerNodes = [x for x in self.nodes.values() if x['type'] == 'producer']
        consumerNodes = [x for x in self.nodes.values() if x['type'] == 'consumer']
        hubNodes = [x for x in self.nodes.values() if x['type'] == 'hub']

        for node in consumerNodes:
            consumerYml = self.baseYmlForNode(node)
            # add dependencies
            # by default consumers depend on all hubs and all producers
            consumerYml['depends_on'] = [n['name'] for n in producerNodes + hubNodes]
            # add environment
            consumerYml['environment'] = self.makeEnvironment(node['network_shape'], node['routes'], self.cenv)
            yml['services'][node['name']] = consumerYml
        
        for node in hubNodes:
            hubYml = self.baseYmlForNode(node)
            # hubs depend on producers
            hubYml['depends_on'] = [n['name'] for n in producerNodes]
            # add environment
            hubYml['environment'] = self.makeEnvironment(node['network_shape'], node['routes'], {"NFD_BACKGROUND":"no"})
            yml['services'][node['name']] = hubYml

        for node in producerNodes:
            producerYml = self.baseYmlForNode(node)
            # add environment
            producerYml['environment'] = self.makeEnvironment(node['network_shape'], {}, self.penv)
            yml['services'][node['name']] = producerYml

        self.yml = yml

        return True

    def baseYmlForNode(self, node):
        return {
                'build': node['type'][0], 
                'container_name': node['name'], 
                'volumes': [os.path.join('./generated', node['name'])+':/generated'],
                'cap_add': ['NET_ADMIN']
               }

    def writeYml(self, outFile):
        if os.path.exists(outFile):
            os.remove(outFile)
        with open(outFile, 'w') as f:
            f.write(yaml.dump({'version':self.yml['version']}, default_flow_style=False))
            f.write(yaml.dump({'services':self.yml['services']},default_flow_style=False))
            

    def makeEnvironment(self, networkShapes, routes, otherEnv):
        env = []
        networkShapeVar = self.makeNetworkShapeVar(networkShapes)
        if networkShapeVar:
            env.append('NETWORK_SHAPE='+networkShapeVar)
        registerVar = self.makeRegisterVar(routes)
        if registerVar:
            env.append('REGISTER='+registerVar)
        for var,val in otherEnv.items():
            env.append(var+'='+val)
        return env

    def makeNetworkShapeVar(self, networkShapes):
        shapeVar = None
        for targetNode, linkShape in networkShapes.items():
            if shapeVar and len(shapeVar) > 0:
                shapeVar += " "
            else:
                shapeVar = ""
            lat = linkShape['lat'] if 'lat' in linkShape else 0
            loss = linkShape['loss'] if 'loss' in linkShape else 0
            bw = linkShape['bw'] if 'bw' in linkShape else 0
            shapeVar += "{0}:{1}-{2}-{3}".format(targetNode, lat, loss, bw)
        return shapeVar
    
    def makeRegisterVar(self, routes):
        registerVar = None
        for prefix, nodes in routes.items():
            for n in nodes:
                if registerVar:
                    registerVar += " "
                else:
                    registerVar = ""
                registerVar += "{0}:{1}".format(n, prefix)
        return registerVar
