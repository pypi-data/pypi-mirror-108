# ==============================================================================
#  Copyright (c) 2021. Sergey2006 (Sergey Selivanov)
#  This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see https://www.gnu.org/licenses/.
# ==============================================================================

"""
Quick docs:
DecoFiler is a profiler that use power of decorations for all your needs

The main class is Profiler, it has:
    TimeProfile()
      prints time after the function finishes
    ManyTime(count=5)
      profiles time of a function several times and print time for each test
    Soon there will be memory profiling, function memory capping and
    function timeout

"""

import time
from functools import wraps
import tracemalloc


# I don't know who you are if you don't have Python Standard Library.
# Try to install latest Python from here: https://www.python.org/downloads


def time_profiler(func):
    """
    Quick doc:
    This decorator profiles time with VERY easy way(seems to be slow)
    after function done, it will say the time it takes and returns
    result of a function\n
    How to use:\n
        @time_profiler\n
        def main():
            pass
    It will give you something like that:
        Function Done! Time elapsed: 0 sec
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        old_time = time.time()
        try:
            result = func(*args, **kwargs)
            delta = time.time() - old_time
        except Exception as e:
            result = None
            print("Exception!", e)
            delta = time.time() - old_time
        print("Function Done! Time elapsed:", delta, "sec")
        return result
    
    return wrapper


def many_time_profiler(count=5, average=True):
    """
    Quick doc:
    This decorator profiles time several times with VERY easy
    way(seems to be slow)after function done, it will say the time
    it takes and returns result of a function
    How to use:
        @many_time_profiler(count=5)\n
        def main():
            pass
    It will give you something like that:
        Test done! Average time is: 0 sec
    But if you will use average=false:
        Test done!\n
        Test 1: time elapsed: 0 sec\n
        Test 2: time elapsed: 0 sec\n
        Test 3: time elapsed: 0 sec\n
        Test 4: time elapsed: 0 sec\n
        Test 5: time elapsed: 0 sec
    """
    
    def timer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            deltas = []
            for i in range(count):
                old_time = time.time()
                _ = func(*args, **kwargs)
                delta = time.time() - old_time
                deltas.append(delta)
            if average:
                print("Test done! Average time:", sum(deltas) / count,
                      "sec")
            else:
                print("Test done!")
                for i in range(len(deltas)):
                    print("Test", str(i + 1) + ": Time elapsed:", deltas[
                        i], "sec")
            return func(*args, **kwargs)
        
        return wrapper
    
    return timer


def memory_profiler(func):
    """
    Quick doc:
    memory_profiler uses tracemalloc to see how much memory you use and
    the peak memory usage. For very optimised ways peak memory usage
    is less than 500 KiB bigger than overall memory usage... But will you
    reach the
    same? This thing will help you!\n
    How to use:
        @memory_profiler\n
        def main():
            pass
    It will give you something like that:
    Function done! Memory used: 3 KiB. Peak is: 5 KiB
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        size_before, _ = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        result = func(*args, **kwargs)
        size, peak = tracemalloc.get_traced_memory()
        print("Function done! Memory used:", (size - size_before),
              "KiB. Peak is:", peak, "KiB")
        tracemalloc.stop()
        return result
    
    return wrapper


def many_memory_profiler(count=5, average=True):
    """
    Quick doc:
    many_memory_profiler uses tracemalloc to see how much memory you use and
    the peak memory usage. For very optimised ways peak memory usage
    is less than 500 KiB bigger than overall memory usage... But will you
    reach the
    same? This thing will help you!\n
    How to use:
        @many_memory_profiler(count=5, average=True)\n
        def main():
            pass
    It will give you something like that:
    Test done! Average Memory usage: 3 KiB. Average Peak is: 5 KiB
    But if you will use Average=False:\n
    Test done!\n
    Test 1: Memory used: 3 KiB. Peak is: 5 KiB\n
    Test 2: Memory used: 3 KiB. Peak is: 5 KiB\n
    Test 3: Memory used: 3 KiB. Peak is: 5 KiB\n
    Test 4: Memory used: 3 KiB. Peak is: 5 KiB\n
    Test 5: Memory used: 3 KiB. Peak is: 5 KiB
    
    """
    
    def memory_profile(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            memories = []
            for i in range(count):
                tracemalloc.start()
                size_before, _ = tracemalloc.get_traced_memory()
                tracemalloc.reset_peak()
                _ = func(*args, **kwargs)
                size, peak = tracemalloc.get_traced_memory()
                memories.append((size - size_before, peak))
                tracemalloc.stop()
            memory = list(map(lambda x: x[0], memories))
            peaks = list(map(lambda x: x[1], memories))
            if average:
                print("Test Done! Average memory usage:", sum(memory) /
                      count, "KiB. Average peak is:", sum(peaks) /
                      count, "KiB")
            else:
                print("Test done!")
                for i in range(len(memories)):
                    print("Test", str(i + 1) + ": Memory used:",
                          memory[i], "KiB. Peak is:", peaks[i],
                          "KiB")
            return func(*args, **kwargs)
        
        return wrapper
    
    return memory_profile
