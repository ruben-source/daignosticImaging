
err = ("some error msg", "error", 404)
err2 = ("some error msg", "blank", 200)
err3 = ("", "", 0)

def error_handle(err):
    msg = err[0]
    match err:
        case (msg, "error", 404):
            print(f"error with error message: \n   {msg} \n and exit code 404")
        case (msg, "blank", 404):
            print(f"error with error message: \n   {msg} \n and exit code 404")
        case (msg, "blank", x) if x == 200:
            print(f"error with error message: \n   {msg} \n and exit code 200")
        case _:
            print("default")

error_handle(err)
print("\n")
error_handle(err2)
print("\n")
error_handle(err3)