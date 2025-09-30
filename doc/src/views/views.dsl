views {

    properties {
        "c4plantuml.tags" true
        "c4plantuml.legend" false
        "plantuml.animation" true
        "generatr.site.exporter" "structurizr"
        "generatr.site.nestGroups" true
        "generatr.site.externalTag" "Extern"
        "generatr.markdown.flexmark.extensions" "TableOfContents,Tables,Admonition,Footnotes,Definition,GitLab"
        "generatr.style.faviconPath" "site/favicon.png"
        #"generatr.style.colors.primary" "#0b7983"
        #"generatr.style.colors.secondary" "#FFFFFF"
    }

    #branding {
    #    logo <file|url>
    #    font <name> [url]
    #}

    !include "styles.dsl"
    !include "deployment.dsl"
    !include "system_landscape.dsl"
    !include "runtime.dsl"

    # put your system/container/component views in one file per software system group
    !include example.dsl

}
