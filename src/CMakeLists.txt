include_directories(.)
add_executable(aiprog c_implementations/expectimax.c)
add_library(source_lib c_implementations/expectimax.c)