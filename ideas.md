# Ideas for Procedural Map Generation

should be generated in this order, first height, then water then humidity

## Mountains depending on Plate Tectonics

- first spawn fault lines which form separate plates
- each plate has a speed and direction
- each plate has a height (oceanic plates and land plates)
- Oceanic Plates spawn with water on top
- at the border of each plate two kinds of mountains can exist (or none):
  - converging and diverging plates (down converging and up converging)
- At the border the highest mountain exists and it
- somehow there should be multiple mountains and not just one large mountain
- height gets added with a noise map to create more interesting structures

## Rivers

- There are two heights, water Height and Terrain height
- Water flows downhill
- each adjacent cell(+water height), which is below the current cell (+water height) gets water
- randomly spawn height of water in one pixel
- height of water of a cell never reduces (only increases if different water arrives)
- water of current cell gets spread over all adjacent cells steepest cell change gets most water
- all water gets distributed to adjacent cells as long as all adjacent cells have less water than current cell

## Humidity

- One wind direction for simplicity
- Humidity Map
- Base Humidity at the start of the Map
- Humidity around Rivers and Lakes (Oceans if they exist not sure) depending on the depth and wind speed
- wind gets stopped at mountains a bit ()
- Landscape drawing:
  - humidity below 20% desert --> sand colour
    - turns to brown and then grey with height
  - humidity between 20% and 60% grass land (lime green) and below some height $h_1$
    - also on a scale the higher the humidity the darker the green, never as dark as forest
  - humidity between 60% and 90% forest (dark green)
    - below some height $h_2 < h_1$
    - when above then grass land
    - from some height $h_3 >> h_1$ snow, maybe that is gradual for height always some value which determines the colour by height and once above certain height its just white
  - humidity above 90% swamp dark green
- if humidity high and cell steep spawn height water (depending on incline and humidity (lets say at least 70%))
