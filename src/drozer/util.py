import argparse

class StoreZeroOrTwo(argparse.Action):
    
    def __call__(self, parser, args, values, option_string=None):
        if not (len(values) == 0 or len(values) == 2):
            msg='argument "--{f}" requires either 0 or 2 arguments'.format(f=self.dest)
            raise argparse.ArgumentTypeError(msg)
        setattr(args, self.dest, values)
