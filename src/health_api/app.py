import health_api

if __name__ == "__main__":
    env = health_api.HostEnvironment()
    health_api.serving.Server.start()