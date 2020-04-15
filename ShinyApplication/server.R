library(shiny)
library(leaflet)
library(leaflet.extras)
library(raster)
library(sp)
library(rgdal)
library(elevatr)
library(plot3D)
library(magick)


server <- function(input, output, session) {
  mapRaster <- reactiveValues(mapRaster=NULL, mapRasterLow=NULL)
  mapCenter <- reactiveValues(lng=86.9250, lat=27.9881)
  
  output$download <- downloadHandler(
    filename = function(){"topoTable.csv"},
    content = function(fname){
      everest.df <- as.data.frame(mapRaster$mapRasterLow, xy=TRUE)
      everest.df$x <- round((everest.df$x - min(everest.df$x)) / ((mapRaster$mapRasterLow@extent@xmax - mapRaster$mapRasterLow@extent@xmin)/as.numeric(input$tableSize)),0)
      everest.df$y <- round((everest.df$y - min(everest.df$y)) / ((mapRaster$mapRasterLow@extent@ymax - mapRaster$mapRasterLow@extent@ymin)/as.numeric(input$tableSize)),0)
      everest.df$z <- ((everest.df$layer - min(everest.df$layer)) / ((mapRaster$mapRasterLow@extent@xmax - mapRaster$mapRasterLow@extent@xmin)/as.numeric(input$tableSize))) * as.numeric(input$pillarSize)
      everest.df <- everest.df[,c("x","y","z")]
      write.csv(everest.df, fname, row.names=FALSE)
    }
  )

  output$plot <- renderPlot({
    if (!is.null(mapRaster$mapRaster)){
      bottomLimit <- mean(values(mapRaster$mapRaster)) - 4*(sd(values(mapRaster$mapRaster)))
      values(mapRaster$mapRaster)[which(values(mapRaster$mapRaster)<bottomLimit)] <- NA
      everest_low <- aggregate(mapRaster$mapRaster, fact=mapRaster$mapRaster@nrows/as.numeric(input$tableSize))
      everest.matrix <- as.matrix(everest_low)
      yRange <- everest_low@extent@ymax-everest_low@extent@ymin
      xRange <- everest_low@extent@xmax-everest_low@extent@xmin
      mapRaster$mapRasterLow <- everest_low
      
      hist3D(x=(1:nrow(everest.matrix))*(xRange/as.numeric(input$tableSize)), y=(1:ncol(everest.matrix))*(yRange/as.numeric(input$tableSize)), z=everest.matrix, scale=FALSE, axes = FALSE, colkey=FALSE, theta=input$plotViewAngle+45) # xlim=c(1*xRange, nrow(everest.matrix)*xRange), ylim=c(mapRaster$mapRaster@extent@ymin, mapRaster$mapRaster@extent@ymax), zlim=c(minValue(mapRaster$mapRaster), maxValue(mapRaster$mapRaster))      zlim=c(minValue(mapRaster$mapRaster),minValue(mapRaster$mapRaster)+2*(mapRaster$mapRaster@extent@ymax-mapRaster$mapRaster@extent@ymin))) 
    }
  }, height=350)
  
  output$terrainPreview <- renderImage({
    list(
      src="www/terrainPreview_recolored.png",
      contentType="image/png",
      width=200,
      height=200,
      alt="Terrain"
    )
  }, deleteFile=FALSE)
  
  observeEvent(input$generateTerrainPreview, {
    proxy <- leafletProxy("mymap")
    proxy %>%
      addRectangles(layerId="preview", lng1=input$mymap_center$lng-input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lng2=input$mymap_center$lng+input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lat1=input$mymap_center$lat-input$regionSize*1000*(1/111111), lat2=input$mymap_center$lat+input$regionSize*1000*(1/111111), color="green") #%>%
      #addRectangles(layerId="preview1", lng1=input$mymap_center$lng-0.1, lng2=input$mymap_center$lng, lat1=input$mymap_center$lat-0.1, lat2=input$mymap_center$lat, color="green", opacity=0.1, fillOpacity=0) %>%
      #addRectangles(layerId="preview2", lng1=input$mymap_center$lng, lng2=input$mymap_center$lng+0.1, lat1=input$mymap_center$lat-0.1, lat2=input$mymap_center$lat, color="green", opacity=0.1, fillOpacity=0) %>%
      #addRectangles(layerId="preview3", lng1=input$mymap_center$lng-0.1, lng2=input$mymap_center$lng, lat1=input$mymap_center$lat, lat2=input$mymap_center$lat+0.1, color="green", opacity=0.1, fillOpacity=0) %>%
      #addRectangles(layerId="preview4", lng1=input$mymap_center$lng, lng2=input$mymap_center$lng+0.1, lat1=input$mymap_center$lat, lat2=input$mymap_center$lat+0.1, color="green", opacity=0.1, fillOpacity=0)
    withProgress(message = 'Retrieving Elevation File', value = 0, {
      #retrieveElevationPreview(north=input$mymap_center$lat+0.1, south=input$mymap_center$lat-0.1, east=input$mymap_center$lng+0.1, west=input$mymap_center$lng-0.1)
      crds <- cbind(x=c(input$mymap_center$lng+input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))),input$mymap_center$lng+input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))),input$mymap_center$lng-input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))),input$mymap_center$lng-input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925)))), y=c(input$mymap_center$lat+input$regionSize*1000*(1/111111),input$mymap_center$lat-input$regionSize*1000*(1/111111),input$mymap_center$lat+input$regionSize*1000*(1/111111),input$mymap_center$lat-input$regionSize*1000*(1/111111)))
      Pl <- Polygon(crds)
      ID <- "everest"
      Pls <- Polygons(list(Pl), ID=ID)
      SPls <- SpatialPolygons(list(Pls))
      df <- data.frame(value=1, row.names=ID)
      SPDF <- SpatialPolygonsDataFrame(SPls, df)
      proj4string(SPDF) <- CRS("+proj=longlat")
      utm_zone <- ceiling((input$mymap_center$lng+180)/6)
      SPDF_utm <- spTransform(SPDF, CRS(paste("+proj=utm +zone=", as.character(utm_zone)," +datum=WGS84", sep="")))
      incProgress(0.1)
      if (input$regionSize < 2) {
        everest <- get_elev_raster(locations=SPDF_utm, z=14, clip="bbox") 
      } else if (input$regionSize < 5) {
        everest <- get_elev_raster(locations=SPDF_utm, z=12, clip="bbox")
      } else {
        everest <- get_elev_raster(locations=SPDF_utm, z=10, clip="bbox")
      }
      incProgress(0.4)
      everest_trim <- trim(everest)
      pass <- FALSE
      while (pass==FALSE) {
        counts <- data.frame(r1=2, r2=everest_trim@nrows, c1=1, c2=everest_trim@ncols, countNA=c(sum(is.na(everest_trim[1,]))))
        counts <- rbind(counts, data.frame(r1=1, r2=everest_trim@nrows-1, c1=1, c2=everest_trim@ncols, countNA=c(sum(is.na(everest_trim[everest_trim@nrows,])))))
        counts <- rbind(counts, data.frame(r1=1, r2=everest_trim@nrows, c1=2, c2=everest_trim@ncols, countNA=c(sum(is.na(everest_trim[,1])))))
        counts <- rbind(counts, data.frame(r1=1, r2=everest_trim@nrows, c1=1, c2=everest_trim@ncols-1, countNA=c(sum(is.na(everest_trim[,everest_trim@ncols])))))
        if (any(counts$countNA > 0)) {
          sideToTrim <- counts[which(counts$countNA==max(counts$countNA)),][1,]
          everest_trim <- everest_trim[sideToTrim$r1:sideToTrim$r2, sideToTrim$c1:sideToTrim$c2, drop=FALSE] #crop(everest_trim, extent(everest_trim, sideToTrim$r1, sideToTrim$r2, sideToTrim$r3, sideToTrim$r4))
        }else{
          pass <- TRUE
        } 
      }
      incProgress(0.4)
      if (nrow(everest_trim) > ncol(everest_trim)) {
        everest_trim <- everest_trim[1:nrow(everest_trim)-(nrow(everest_trim) - ncol(everest_trim)), 1:ncol(everest_trim), drop=FALSE]
      } else if (ncol(everest_trim) > nrow(everest_trim)) {
        everest_trim <- everest_trim[1:nrow(everest_trim), 1:ncol(everest_trim)-(ncol(everest_trim) - nrow(everest_trim)), drop=FALSE]
      }
      writeRaster((everest_trim - everest_trim@data@min)/(everest_trim@data@max - everest_trim@data@min), filename="www/terrainPreview_recolored.tif", overwrite=TRUE)
      terrainPreview <- image_read("www/terrainPreview_recolored.tif")
      image_write(terrainPreview, path = "www/terrainPreview_recolored.png", format = "png")
      mapRaster$mapRaster <- everest_trim
      incProgress(0.1)
    })
    output$terrainPreview <- renderImage({
      list(
        src="www/terrainPreview_recolored.png",
        contentType="image/png",
        width=200,
        height=200,
        alt="Terrain"
      )
    }, deleteFile=FALSE)
  })
  
  output$mymap <- renderLeaflet({
    leaflet(options=leafletOptions(minZoom=2, maxZoom=15, worldCopyJump=TRUE, inertia=FALSE)) %>%
      addProviderTiles(providers$OpenStreetMap.Mapnik, options=providerTileOptions(noWrap=FALSE)) %>%
      addRectangles(layerId="preview", lng1=86.92483-1*1000*(1/(111111*cos(27.98787*0.0174532925))), lng2=86.92483+1*1000*(1/(111111*cos(27.98787*0.0174532925))), lat1=27.98787-1*1000*(1/111111), lat2=27.98787+1*1000*(1/111111), color="green") %>%
      addRectangles(layerId="center", lng1=86.92483-1*1000*(1/(111111*cos(27.98787*0.0174532925))), lng2=86.92483+1*1000*(1/(111111*cos(27.98787*0.0174532925))), lat1=27.98787-1*1000*(1/111111), lat2=27.98787+1*1000*(1/111111)) %>%
      addRectangles(layerId="center1", lng1=86.92483-1*1000*(1/(111111*cos(27.98787*0.0174532925))), lng2=86.92483, lat1=27.98787-1*1000*(1/111111), lat2=27.98787, opacity=0.1, fillOpacity=0) %>%
      addRectangles(layerId="center2", lng1=86.92483, lng2=86.92483+1*1000*(1/(111111*cos(27.98787*0.0174532925))), lat1=27.98787-1*1000*(1/111111), lat2=27.98787, opacity=0.1, fillOpacity=0) %>%
      addRectangles(layerId="center3", lng1=86.92483-1*1000*(1/(111111*cos(27.98787*0.0174532925))), lng2=86.92483, lat1=27.98787, lat2=27.98787+1*1000*(1/111111), opacity=0.1, fillOpacity=0) %>%
      addRectangles(layerId="center4", lng1=86.92483, lng2=86.92483+1*1000*(1/(111111*cos(27.98787*0.0174532925))), lat1=27.98787, lat2=27.98787+1*1000*(1/111111), opacity=0.1, fillOpacity=0) %>%
      #addRectangles(layerId="preview", lng1=86.9250-0.1, lng2=86.9250+0.1, lat1=27.9881-0.1, lat2=27.9881+0.1, options=markerOptions(draggable=TRUE)) %>%
      #setView(lng=86.9250, lat=27.9881, zoom=11) %>%
      #addDrawToolbar(position="bottomleft", circleMarkerOptions=NA, circleOptions=NA, markerOptions=NA, polygonOptions=NA, rectangleOptions=NA, polylineOptions=NA) %>%
      addSearchOSM(options = searchOptions(autoCollapse = TRUE, minLength = 2, hideMarkerOnCollapse=TRUE, zoom=12)) %>%
      addScaleBar(position="bottomright")
  })
  
  observe({
    if (!is.null(input$mymap_center$lat)){
      proxy <- leafletProxy("mymap")
      if (input$mymap_zoom < 10){
        proxy %>%
          removeShape(layerId="center") %>%
          removeShape(layerId="center1") %>%
          removeShape(layerId="center2") %>%
          removeShape(layerId="center3") %>%
          removeShape(layerId="center4")
      }else if (input$mymap_center$lat != mapCenter$lat){
        proxy %>% 
          setView(lng=input$mymap_center$lng, lat=input$mymap_center$lat, zoom=input$mymap_zoom) %>%
          addRectangles(layerId="center", lng1=input$mymap_center$lng-input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lng2=input$mymap_center$lng+input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lat1=input$mymap_center$lat-input$regionSize*1000*(1/111111), lat2=input$mymap_center$lat+input$regionSize*1000*(1/111111)) %>%
          addRectangles(layerId="center1", lng1=input$mymap_center$lng-input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lng2=input$mymap_center$lng, lat1=input$mymap_center$lat-input$regionSize*1000*(1/111111), lat2=input$mymap_center$lat, opacity=0.1, fillOpacity=0) %>%
          addRectangles(layerId="center2", lng1=input$mymap_center$lng, lng2=input$mymap_center$lng+input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lat1=input$mymap_center$lat-input$regionSize*1000*(1/111111), lat2=input$mymap_center$lat, opacity=0.1, fillOpacity=0) %>%
          addRectangles(layerId="center3", lng1=input$mymap_center$lng-input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lng2=input$mymap_center$lng, lat1=input$mymap_center$lat, lat2=input$mymap_center$lat+input$regionSize*1000*(1/111111), opacity=0.1, fillOpacity=0) %>%
          addRectangles(layerId="center4", lng1=input$mymap_center$lng, lng2=input$mymap_center$lng+input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lat1=input$mymap_center$lat, lat2=input$mymap_center$lat+input$regionSize*1000*(1/111111), opacity=0.1, fillOpacity=0)
      }else if (input$mymap_center$lng != mapCenter$lng){
        proxy %>%
          setView(lng=input$mymap_center$lng, lat=input$mymap_center$lat, zoom=input$mymap_zoom) %>%
          addRectangles(layerId="center", lng1=input$mymap_center$lng-input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lng2=input$mymap_center$lng+input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lat1=input$mymap_center$lat-input$regionSize*1000*(1/111111), lat2=input$mymap_center$lat+input$regionSize*1000*(1/111111)) %>%
          addRectangles(layerId="center1", lng1=input$mymap_center$lng-input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lng2=input$mymap_center$lng, lat1=input$mymap_center$lat-input$regionSize*1000*(1/111111), lat2=input$mymap_center$lat, opacity=0.1, fillOpacity=0) %>%
          addRectangles(layerId="center2", lng1=input$mymap_center$lng, lng2=input$mymap_center$lng+input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lat1=input$mymap_center$lat-input$regionSize*1000*(1/111111), lat2=input$mymap_center$lat, opacity=0.1, fillOpacity=0) %>%
          addRectangles(layerId="center3", lng1=input$mymap_center$lng-input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lng2=input$mymap_center$lng, lat1=input$mymap_center$lat, lat2=input$mymap_center$lat+input$regionSize*1000*(1/111111), opacity=0.1, fillOpacity=0) %>%
          addRectangles(layerId="center4", lng1=input$mymap_center$lng, lng2=input$mymap_center$lng+input$regionSize*1000*(1/(111111*cos(input$mymap_center$lat*0.0174532925))), lat1=input$mymap_center$lat, lat2=input$mymap_center$lat+input$regionSize*1000*(1/111111), opacity=0.1, fillOpacity=0)
      }
    }
  })
  
}