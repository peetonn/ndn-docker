""" Parses .env files """

class EnvReader(object):
    def parse(self, envFile):
        env = {}
        with open(envFile, 'r') as f:
            for line in f:
                stripped = line.strip()
                if not stripped.startswith('#'):
                    split = stripped.split('=', 1)
                    if len(split) == 2:
                        env[split[0]] = split[1]
                    else:
                        print "Can't parse line " + line + " in file " + envFile
        return env