# Overview

A few dummy experiments that demonstrate how you can use Reliably and SLO to 
play nicely with your Chaos Toolkit experiments.

To make it simple, make sure you have [installed][reliablyinstall] the
`reliably` CLI and [logged in][reliablylogin] against Reliably.

[reliablyinstall]: https://reliably.com/docs/getting-started/install/
[reliablylogin]: https://reliably.com/docs/getting-started/login/

Once logged in you should see a a file at:

```
~/.config/reliably/config.yaml
```

This file is important as the extension will use it to authenticate.

These experiments do not focus on what they actually experiment on but are
templates on integrating against Reliably's service to benefit from SLO in
Chaos Engineering experiments.

Make sure to install the Chaos Toolkit requirements for these experiments:

```console
$ pip install -r requirements.txt
```

# Use SLO as a Steady-State

File: use-slo-as-steady-state.json

This experiment describes how you can use your SLO as a natural steady-state
hypothesis in order to indicate if the experiment deviated or not.

SLO are fantastic for this because they are grounded into the reality of your
system. They also have been discussed and agreed by the team already, so a
deviation from them can be immediatly understood by everyone.

# Use SLO as a safeguard

File: use-slo-as-experiment-safeguard.json

This experiment describes how you can use your SLO as a natural safeguard
to protect your system from experiments that may indeed harm it too extensively.

Your SLO are being checked regularly during the experiment and as soon as one
of them breaks its target, the safeguard mechanism interrupts the experiment.