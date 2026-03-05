cmake_minimum_required(VERSION 3.5)
project(booster_description)

# Find dependencies
find_package(ament_cmake REQUIRED)

# Install directories
# Qui diciamo a ROS di copiare le tue cartelle 'launch', 'meshes', 'urdf' e 'config'
# nella cartella di installazione, così RViz le può trovare.
install(
  DIRECTORY 
    config 
    launch 
    meshes 
    urdf 
  DESTINATION 
    share/${PROJECT_NAME}
)

# Setup the project
ament_package()