from dotenv import dotenv_values

from src.api.FetchGithub import fetchGraphQL, fetchREST

config = dotenv_values(".env")
ACCESS_TOKEN = config["ACCESS_TOKEN"]

def main():
    fetchGraphQL(ACCESS_TOKEN, 1)
    fetchREST(ACCESS_TOKEN, 1)
    fetchGraphQL(ACCESS_TOKEN, 50)
    fetchREST(ACCESS_TOKEN, 50)

main()