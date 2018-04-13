import pathlib
import datetime
import pyotp

__version__ = '0.2.0'

_PAGE_PARTS = [
    "<!DOCTYPE html>\n<html>\n  <body>\n    <h1>hbldhauth QR code page</h1>",
    "    <script src=\"https://cdnjs.cloudflare.com/ajax/libs" +
    "/qrious/4.0.2/qrious.min.js\"></script>\n<script>",
    "    </script>\n  </body>\n</html>"
]

_FUNCTION_TEMPLATE = """
      (function() {
        var qr = new QRious({
          element: document.getElementById('%s'),
          value: '%s'
        });
      })();
"""


def _get_token_path_from_config(path):
    with open(path, 'r') as f:
        return str(pathlib.Path(f.read().strip()))


def read_tokens(path):
    with open(path, 'r') as f:
        out = []
        for line in f.read().strip().splitlines(keepends=False):
            issuer_and_account, token = tuple(map(str.strip, line.split(':')))
            issuer, account = map(str.strip, issuer_and_account.split('|'))
            out.append((issuer, account, token.replace(' ', '')))
    return tuple(out)


def now(s):
    otp = pyotp.TOTP(s.replace(' ', '')).now()
    return " ".join([str(otp)[:3], str(otp)[3:]])


def qr_uri(issuer, account, token):
    return pyotp.totp.TOTP(token).provisioning_uri(account, issuer_name=issuer)


def generate_qr_page(tokens):
    canvases = []
    functions = []
    for token_tuple in tokens:
        canvases.append("    <h2>{0}</h2><canvas id=\"{0}\" style=\"padding-bottom:200px\"></canvas>".format(token_tuple[0]))
        functions.append(_FUNCTION_TEMPLATE % (token_tuple[0], qr_uri(*token_tuple)))
    return _PAGE_PARTS[0] + "\n".join(canvases) + _PAGE_PARTS[1] + "\n".join(functions) + _PAGE_PARTS[2]


def main():
    import argparse

    parser = argparse.ArgumentParser(prog='hbldhauth')
    parser.add_argument('-c', '--config',
                        default=str(pathlib.Path.home().joinpath('.hbldhauth')))
    parser.add_argument('--qr', action='store_true', help="Open a webpage with QR codes for provisioning.")

    args = parser.parse_args()
    token_path = _get_token_path_from_config(args.config)
    tokens = read_tokens(token_path)

    if args.qr:
        import os
        import time
        import tempfile
        import webbrowser
        print('--- hbldh Authenticator ---')

        html = generate_qr_page(tokens)
        with tempfile.NamedTemporaryFile('w', suffix='.html', encoding='utf-8', delete=False) as f:
            print('Generating QR code page at {0}...'.format(f.name))
            f.write(html)
            webbrowser.open(f.name)
        time.sleep(3.0)
        try:
            os.remove(f.name)
            print("Deleted QR code web page.")
        except:
            print("WARNING! Could not remove web page!")
    else:
        print('--- hbldh Authenticator ---')
        print('Valid for {0} seconds...\n'.format(
            30 - datetime.datetime.now().second % 30))
        for issuer, account, token in tokens:
            print("{0} ({1}): {2}".format(issuer, account, now(token)))


if __name__ == "__main__":
    main()


