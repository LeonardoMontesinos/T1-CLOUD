#!/usr/bin/env python3
import aws_cdk as cdk
from crud_stack import CrudStack

app = cdk.App()
CrudStack(app, "CrudStack",
    env=cdk.Environment(
        account="153265898954",  # tu cuenta AWS
        region="us-east-1"
    )
)
app.synth()
