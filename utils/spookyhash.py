try:
    # https://burtleburtle.net/bob/hash/spooky.html
    import cppimport.import_hook
    from .spookyhash_cpp import hash128
except:
    raise NotImplementedError

if __name__ == "__main__":
    import sys
    print(hash128(bytes.fromhex(sys.argv[1])))