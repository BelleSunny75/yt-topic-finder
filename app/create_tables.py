from .db import Base, engine
from . import models

def main():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    main()
