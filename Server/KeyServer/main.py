import multiprocessing
from Server.KeyServer.KeyServer import KeyServer

if __name__ == '__main__':
    try:
        KeyServer('localhost', 8081).run()
    except Exception as ex:
        print(f"\nUnexpected error occurred: {str(ex)}")
    finally:
        print("Shutting down server")
        for process in multiprocessing.active_children():
            print(f"Shutting down process {process.pid}")
            process.terminate()
            process.join()
