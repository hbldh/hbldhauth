import pathlib
import datetime
import pyotp

__version__ = '0.1.0'


def _get_token_path_from_config(path):
    with open(path, 'r') as f:
        return str(pathlib.Path(f.read().strip()))


def read_tokens(path):
    with open(path, 'r') as f:
        data = f.read().strip().splitlines(keepends=False)
    return (tuple(map(str.strip, d.split(':'))) for d in data)


def now(s):
    otp = pyotp.TOTP(s.replace(' ', '')).now()
    return " ".join([str(otp)[:3], str(otp)[3:]])


def main():
    import argparse
    parser = argparse.ArgumentParser(prog='hbldhauth')
    parser.add_argument('-c', '--config',
                        default=str(pathlib.Path.home().joinpath('.hbldhauth')))

    args = parser.parse_args()
    token_path = _get_token_path_from_config(args.config)
    tokens = read_tokens(token_path)
    print('--- hbldh Authenticator ---')
    print('Valid for {0} seconds...\n'.format(
        30 - datetime.datetime.now().second % 30))
    for app, token in tokens:
        print("{0}: {1}".format(app, now(token)))


if __name__ == "__main__":
    main()


