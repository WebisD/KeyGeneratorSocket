import multiprocessing
from ComplexityServer import ComplexityServer

if __name__ == '__main__':
    try:
        ComplexityServer('localhost', 8080).run()
    except Exception as ex:
        print(f"\nUnexpected error occurred: {str(ex)}")
    finally:
        print("Shutting down server")
        for process in multiprocessing.active_children():
            print(f"Shutting down process {process.pid}")
            process.terminate()
            process.join()
