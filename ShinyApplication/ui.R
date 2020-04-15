library(leaflet)
library(shinyWidgets)

ui <- navbarPage("The TopoTable Project", id="nav", position="fixed-top",
                 tabPanel("Application",
                          div(class="outer",
                              tags$head(
                                includeCSS("styles.css")
                              
                              ),
                              sidebarLayout(
                                            mainPanel(width=8,
                                                      leafletOutput("mymap", height="90vh")),
                                            sidebarPanel(id="sidebar",
                                                         width=4,
                                                         tags$head(tags$style(type="text/css",
                                                                              "#terrainPreview img {max-width: 100%; width: 100%; height: auto}")),
                                                         fluidRow(align="center",
                                                                  #shinyWidgets::sliderTextInput(inputId = "regionSize", 
                                                                  #                              label = "Region Size", 
                                                                  #                              choices = c(0.5, seq(1,10)))
                                                                  sliderInput("regionSize", "Region Size",
                                                                              min = 1, max = 10,
                                                                              value = 1, step = 1)
                                                          ),
                                                         fluidRow(align="center",
                                                           actionButton("generateTerrainPreview", "Generate Terrain Preview")
                                                         ),
                                                         fluidRow(
                                                           column(width=5, align="center", h3("Terrain Preview"),
                                                                  div(imageOutput("terrainPreview"), style="max-height: 200px;")),
                                                           column(width=7, align="center", h3("Select the sizes of table and pillars:"),
                                                                  column(width=6, align="center", radioButtons(inputId="tableSize", label="Table", choices=c("20", "30", "40"))),
                                                                  column(width=6, align="center", radioButtons(inputId="pillarSize", label="Pillars", choices=c("1", "2", "3")))
                                                                  )
                                                         ),
                                                         fluidRow(div(plotOutput("plot"), style="height:275px;")),
                                                         fluidRow(align="center",
                                                                  sliderInput("plotViewAngle", "",
                                                                              min = 0, max = 270,
                                                                              value = 0, step = 90)
                                                         ),
                                                         fluidRow(align="center",
                                                                  downloadButton('download',"Download the data"))
                                                         )
                              ))))