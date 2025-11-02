cmake_minimum_required(VERSION 3.22)

if(NOT "${METAMODULE_SDK_DIR}" STREQUAL "")
    message("METAMODULE_SDK_DIR set by CMake variable ${METAMODULE_SDK_DIR}")
elseif(DEFINED ENV{METAMODULE_SDK_DIR})
    set(METAMODULE_SDK_DIR "$ENV{METAMODULE_SDK_DIR}")
    message("METAMODULE_SDK_DIR set by environment variable ${METAMODULE_SDK_DIR}")
else()
    set(METAMODULE_SDK_DIR "${CMAKE_CURRENT_LIST_DIR}/metamodule-plugin-sdk")
    message("METAMODULE_SDK_DIR set to default: ${METAMODULE_SDK_DIR}")
endif()

include(${METAMODULE_SDK_DIR}/plugin.cmake)

project(VcvMetaModulePlugins
    VERSION 0.1
    DESCRIPTION "VCV Plugin for MetaModule"
    LANGUAGES C CXX ASM
)

add_library(VcvMetaModules STATIC)

set(SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/VcvModules)
set(EXTERN_DIR ${CMAKE_CURRENT_LIST_DIR}/VcvModules/extern)


target_include_directories(VcvMetaModules PRIVATE
    ${SOURCE_DIR}/src
    ${SOURCE_DIR}/inc/rnbo-export/common
)

target_sources(VcvMetaModules
    PRIVATE
    ${SOURCE_DIR}/src/plugin.cpp
    
)


set_property(TARGET VcvMetaModules PROPERTY CXX_STANDARD 20)

if("${INSTALL_DIR}" STREQUAL "")
    set(INSTALL_DIR ${CMAKE_CURRENT_LIST_DIR}/metamodule-plugins)
endif()

create_plugin(
    SOURCE_LIB VcvMetaModules # This is the cmake target name (defined in add_target)
    PLUGIN_NAME TestPlug # This must match the brand "slug" used in VCV Rack
    PLUGIN_JSON ${SOURCE_DIR}/plugin.json # Path to the plugin.json file used by VCV Rack
    SOURCE_ASSETS ${CMAKE_CURRENT_LIST_DIR}/assets # Path to the assets/ dir containing the PNGs
    DESTINATION ${INSTALL_DIR}/ # Dir where plugin .mmplugin file should be put
)

set_property(DIRECTORY APPEND PROPERTY ADDITIONAL_CLEAN_FILES "${CMAKE_CURRENT_SOURCE_DIR}/build" "${CMAKE_CURRENT_SOURCE_DIR}/dep" "${CMAKE_CURRENT_SOURCE_DIR}/dist")
set_property(TARGET VcvMetaModules APPEND PROPERTY ADDITIONAL_CLEAN_FILES "${CMAKE_CURRENT_SOURCE_DIR}/plugin.dylib")
