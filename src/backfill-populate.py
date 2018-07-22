import re
import time
import logging
import traceback

import praw

import config
import message
from kill_handler import KillHandler
from models import Base, Investment, Investor
from stopwatch import Stopwatch

InputFilename = "final_upvotes.test.txt"

def main():
    with open(InputFilename, 'r') as f:
        for line in f:
            parts = [x for x in line.strip().split("\t")]

            if len(parts) != 6:
                assert(parts[1] == "xFAILx")
                print(f"-- Skipping {parts[0]}: was xFAILx")
                continue

            investment_id = parts[0]
            response_id = parts[1]
            initial_upvotes = parts[2]
            if parts[3] != initial_upvotes:
                raise Exception("Mismatched initial upvotes: " + line)
            if parts[4] != "NULL":
                raise Exception("Not NULL: " + line)
            final_upvotes = parts[5]

            if final_upvotes == "NOPE":
                print(f"-- Skipping {investment_id}: was NOPE")
                continue

            print(f"UPDATE TABLE Investments SET final_upvotes={final_upvotes} WHERE id={investment_id};")

if __name__ == "__main__":
    main()
