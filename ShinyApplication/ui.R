library(leaflet)
library(shinyWidgets)

ui <- navbarPage("The TopoTable Project", id="nav", position="fixed-top",
                 tabPanel("Home",
                          div(class="home",
                              mainPanel(width=12,
                                        fluidRow(div(style="height:75px")),
                                        fluidRow(align="center", div(imageOutput("logo"), style="height: 325px")),
                                        fluidRow(align="center", h1("The TopoTable Project"), h4("James Kitchens"), HTML("<br><br>")),
                                        fluidRow(column(width=2), column(width=8, p("The goal of the TopoTable Project is to create a dynamic 3D topographic relief table that is built with moveable pillars.
                                                                                    Historically, topographic relief maps have been made using plaster that has been shaped to accurately depict a
                                                                                    region of the world. This style of map is common at the visitor centers of National Parks or within museums. They are
                                                                                    more approachable than 2D topographic maps, as users can both see and physically feel the terrain. I began thinking
                                                                                    about ways that I could incorporate a 3D topographic relief table in a personal setting, such as a home. Unfortunately,
                                                                                    these maps are immutable, being constrained to a single region, which limits their novelness to an individual over time.
                                                                                    They are also rather heavy and large, forcing them to take up a lot of space within the house or in storage. By rethinking
                                                                                    the construction of the table, replacing the plaster with moveable pillars, the TopoTable would be able to approximate any
                                                                                    number of maps, similar to a pin art display.")), column(width=2)),
                                        fluidRow(column(width=2), column(width=8, h4("Table Design"), column(width=2))),
                                        fluidRow(column(width=2), column(width=8, p('The TopoTable will consist of 400, 900, or 1600 pillars arranged in a square. There will be three pillar sizes:
                                                                                    1"x1"x10", 2"x2"x20", or 3"x3"x30". Each pillar will be controlled by its own motor, allowing all of the motors to move simultaneously. An
                                                                                    Arduino will be used to control the motors, designating the heights for the each pillar. Maps will be loaded through a removable SD card, similar
                                                                                    to the functionality of a 3D printer.'), column(width=2))),
                                        fluidRow(column(width=2), column(width=8, h4("Application"), column(width=2))),
                                        fluidRow(column(width=2), column(width=8, p("The TopoTable application allows users to select and download terrain data and save it in a format (.csv) that 
                                                                                    will be used by the TopoTable. Terrain data comes from Mapzen Terrain Tiles. These are the pixelated to either 20x20, 30x30, or 40x40 pixels,
                                                                                    corresponding to the size of the user's table. The user selects the dimensions of a pillar within their table, and the table scales the pillar 
                                                                                    heights appropriately. A preview of what the user's TopoTable will look like is displayed. The user can download their map and save it onto a
                                                                                    removable SD card that will then be inserted into the TopoTable."), column(width=2))),
                                        fluidRow(column(width=2), column(width=8, h4("About The Creator"), column(width=2))),
                                        fluidRow(column(width=2), column(width=8, p("Hi, my name is James Kitchens. I am a recent graduate of Warren Wilson College in Asheville, North Carolina, 
                                                                                    where I earned a BS in Biology and a BS in Chemistry. I enjoy creative programming and data visualizations, 
                                                                                    especially those focused around GIS applications. Click", 
                                                                                    tags$a(href="http://www.james-kitchens.com","here"), "for my personal website, which describes other projects and research that I have worked 
                                                                                    on.")), column(width=2)),
                                        fluidRow(div(style="height:50px"))
                                        )
                                        )
                                        ),
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