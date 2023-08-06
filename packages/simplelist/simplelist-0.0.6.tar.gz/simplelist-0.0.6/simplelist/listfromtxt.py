def listfromtxt(file):
    with open(file, 'r') as f:
        name = [line.strip() for line in f]
        return name
