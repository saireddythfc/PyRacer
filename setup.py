import cx_Freeze

executables = [cx_Freeze.Executable("pygame-racer.py")]

cx_Freeze.setup(
    name = "pygame-racer",
    options = {"build_exe": {"packages":["pygame"],
                             "include_files":["racecar.png", "racecar1.png", "crash.wav", "jazz.wav"]}},
    executables = executables
)
