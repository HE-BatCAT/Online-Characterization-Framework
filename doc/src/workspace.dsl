workspace "Online Characterization Framework" "Architecture of the Online Characterization Framework" {
    !identifiers hierarchical
    !impliedRelationships true
    !adrs "decisions"
    !docs "architecture.md"
    !docs "docs"

    configuration {
        //scope landscape
    }

    !include model/model.dsl
    !include views/views.dsl

}
