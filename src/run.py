import argparse
from server import app

parser = argparse.ArgumentParser(description='Main appliction controller.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')


if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000, debug=True)