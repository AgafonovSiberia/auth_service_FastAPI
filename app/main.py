from fastapi import FastAPI
from config_reader import config


def main():
    api = FastAPI(title="AuthService",
                  description="authorization service",
                  openapi_url=f"{config.API_V1_URL}/openapi.json")




if __name__ == '__main__':
    main()


