import asyncio

from astaria import main


if __name__ == "__main__":
    with open(input("Filename with emails: ")) as file:
        emails = file.read().splitlines()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main(emails))
    except KeyboardInterrupt:
        pass
    