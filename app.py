#!/usr/bin/env python3

import aws_cdk as cdk

from inec.inec_stack import InecStack


app = cdk.App()
InecStack(app, "inec",env=cdk.Environment(account='109661032234', region='us-east-1'),)

app.synth()
