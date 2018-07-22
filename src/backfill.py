import re
import time
import logging
import traceback

import praw

import config
import message
from stopwatch import Stopwatch

InputFilename = "investments_dump.txt"

entry_regex = re.compile(r"You bought in at (\d+) upvotes.", re.MULTILINE | re.IGNORECASE)
exit_regex  = re.compile(r"Your investment has matured at (\d+) upvotes.", re.MULTILINE | re.IGNORECASE)

def main():
    reddit = praw.Reddit(client_id=config.client_id,
                         client_secret=config.client_secret,
                         username=config.username,
                         password=config.password,
                         user_agent=config.user_agent)

    with open(InputFilename, 'r') as f:
        for line in f:
            parts = [x for x in line.strip().split("\t")]
            if len(parts) != 12:
                raise Exception(f"Unexpected data here: {line}")

            investment_id = parts[0]
            response_id = parts[8]
            initial_upvotes = parts[2]
            final_upvotes = parts[10]

            if response_id == "0":
                print(f"xFAILx\t{investment_id}")
                continue

            if final_upvotes == "NULL":
                comment = reddit.comment(response_id)

                parsed_initial_upvotes = "NOPE"
                parsed_final_upvotes = "NOPE"

                entry_match = entry_regex.search(comment.body)
                if entry_match:
                    parsed_initial_upvotes = entry_match.group(1)
                exit_match = exit_regex.search(comment.body)
                if exit_match:
                    parsed_final_upvotes = exit_match.group(1)
                
                print(f"{investment_id}\t{response_id}\t{initial_upvotes}\t{parsed_initial_upvotes}\t{final_upvotes}\t{parsed_final_upvotes}")

                # rem = int(reddit.auth.limits['remaining'])
                # res = int(reddit.auth.limits['reset_timestamp'] - time.time())
                # print(f"API calls remaining: {rem:3d}, resetting in {res:3d}s")

    # for comment in reddit.redditor("memeinvestor_bot").comments(limit=None):
    #     response_id = comment.id
    #     entry_match = entry_regex.search(comment.body.lower())
    #     if entry_match:
    #         parsed_initial_upvotes = entry_match.group(1)
    #         exit_match = exit_regex.search(comment.body.lower())
    #         if exit_match:
    #             parsed_final_upvotes = exit_match.group(1)
    #             print(f"{response_id}\t{parsed_initial_upvotes}\t{parsed_final_upvotes}")

    #     print("-----------------")
    #     rem = int(reddit.auth.limits['remaining'])
    #     res = int(reddit.auth.limits['reset_timestamp'] - time.time())
    #     print(f"API calls remaining: {rem:3d}, resetting in {res:3d}s")
    #     print("-----------------")

if __name__ == "__main__":
    main()
