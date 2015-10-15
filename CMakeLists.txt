cmake_minimum_required(VERSION 3.3)
project(aiprog)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    src/c_implementations/expectimax.c)

add_executable(aiprog ${SOURCE_FILES})