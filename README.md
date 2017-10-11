`hbldh` Authenticator
=====================

A small wrapper around `pyotp` to provide tailored
storage of Authenticator tokens.

The tokens are intended to be stored on an encrypted partition or similar,
enabling this authenticator to be used as a backup for the mobile-based one.

Installation
------------

```bash
$ pip install git+https://github.com/hbldh/hbldhauth.git@master
```

or use [pipsi](https://github.com/mitsuhiko/pipsi):
```bash
$ pipsi install git+https://github.com/hbldh/hbldhauth.git@master#egg=hbldhauth
```

Usage
-----

By default, `hbldhauth` looks for a config file at `~/.hbldhauth`, 
containing the path to the actual file containing the tokens to be
used for Authenticator code generation.

Sample config file:
```text
/keybase/private/hbldh/tokens
```

Sample tokens file:
```text
Github: abcdefghijklmnop
Discord: abcd efgh ijkl mnop
Sentry: ABCD EFGH IJKL MNOP QRST UVWX YZ23 4567
```

Then run `hbldhauth`:
```bash
$ hbldhauth
--- hbldh Authenticator ---
Valid for 17 seconds...

Github: 998 725
Discord: 998 725
Sentry: 362 213

```


