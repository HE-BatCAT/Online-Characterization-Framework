# Put your deployment views here


## Note: 'testbed' is a deployment environment definded in ../model/deployment.dsl
deployment * testbed testbed_deployment {
    include *
    properties {
        "generatr.view.deployment.belongsTo" oc_framework
    }
}

