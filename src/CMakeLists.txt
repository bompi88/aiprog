include_directories(.)
add_executable(aiprog clibs/expectimax.c)
add_library(source_lib clibs/expectimax.c)
