import pyotp


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