# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.20

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /Applications/CLion.app/Contents/bin/cmake/mac/bin/cmake

# The command to remove a file.
RM = /Applications/CLion.app/Contents/bin/cmake/mac/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/mac_batch_runner.dir/depend.make
# Include the progress variables for this target.
include CMakeFiles/mac_batch_runner.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/mac_batch_runner.dir/flags.make

CMakeFiles/mac_batch_runner.dir/main.cpp.o: CMakeFiles/mac_batch_runner.dir/flags.make
CMakeFiles/mac_batch_runner.dir/main.cpp.o: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/mac_batch_runner.dir/main.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/mac_batch_runner.dir/main.cpp.o -c /Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner/main.cpp

CMakeFiles/mac_batch_runner.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/mac_batch_runner.dir/main.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner/main.cpp > CMakeFiles/mac_batch_runner.dir/main.cpp.i

CMakeFiles/mac_batch_runner.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/mac_batch_runner.dir/main.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner/main.cpp -o CMakeFiles/mac_batch_runner.dir/main.cpp.s

# Object files for target mac_batch_runner
mac_batch_runner_OBJECTS = \
"CMakeFiles/mac_batch_runner.dir/main.cpp.o"

# External object files for target mac_batch_runner
mac_batch_runner_EXTERNAL_OBJECTS =

mac_batch_runner: CMakeFiles/mac_batch_runner.dir/main.cpp.o
mac_batch_runner: CMakeFiles/mac_batch_runner.dir/build.make
mac_batch_runner: CMakeFiles/mac_batch_runner.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable mac_batch_runner"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/mac_batch_runner.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/mac_batch_runner.dir/build: mac_batch_runner
.PHONY : CMakeFiles/mac_batch_runner.dir/build

CMakeFiles/mac_batch_runner.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/mac_batch_runner.dir/cmake_clean.cmake
.PHONY : CMakeFiles/mac_batch_runner.dir/clean

CMakeFiles/mac_batch_runner.dir/depend:
	cd /Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner /Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner /Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner/cmake-build-debug /Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner/cmake-build-debug /Users/codythompson/Documents/GitHub/git-shortcut/mac_batch_runner/cmake-build-debug/CMakeFiles/mac_batch_runner.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/mac_batch_runner.dir/depend

