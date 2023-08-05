import argparse
import logging
logger = logging.getLogger(__name__)


def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Oanda v20 API integration')

    parser.add_argument('--bot', default='rsi_bot',
                        required=True, action='store',
                        help='System bot to trade')

    parser.add_argument('--pair', default='EUR_USD',
                        required=True, action='store',
                        help='instrument to trade')

    if pargs is not None:
        return parser.parse_args(pargs)

    return parser.parse_args(pargs)

