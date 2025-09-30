model {
    properties {
        "structurizr.groupSeparator" ":"
    }

    # each group should have it's own file defining the entities (e.g. softwareSystems, containers) and
    # relations between entities of the same group.
    !include software_systems.dsl
    !include external_systems.dsl

    # list relev
    !include users.dsl

    # the relations file contains the inter-group relations
    !include relations.dsl

    # special file for deployment
    !include "deployment.dsl"

}
