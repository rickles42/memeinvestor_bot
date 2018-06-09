from datetime import datetime, timedelta
from pprint import pprint

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

# INPUT_FILENAME = 'logs_overday.txt' # output of the logging job, cleaned up
INPUT_FILENAME = 'logs_overnight.txt' # output of the logging job, cleaned up

class Message:
    def __init__(self, id, time, author, payload):
        self.id = id
        self.time = time
        self.author = author
        self.payload = payload
        self.is_reply_to = None
    
    def __repr__(self):
        return f"{self.id} @ {self.time} from {self.author}: {self.payload}"

def main():
    messages = {}
    message_list = []

    with open(INPUT_FILENAME, 'r') as f:
        for line in f:
            parts = [x for x in line.strip().split(" -- ")]
            assert(len(parts) == 4)

            parts[0] = parts[0].split(":")[2]
            parts[1] = datetime.strptime(parts[1], '%Y-%m-%d %H:%M:%S')

            new_message = Message(parts[0], parts[1], parts[2], parts[3])
            messages[new_message.id] = new_message
            message_list.append(new_message)

            if new_message.author == "MemeInvestor_bot":
                new_message.is_reply_to = new_message.payload

            # if len(messages) > 50:
            #     break
    
    # pprint(messages)
    print(f"len(message_list) = {len(message_list)}")

    unserviced = []
    delays = []
    x = []

    for m in message_list:
        if m.is_reply_to:
            assert(m.author == "MemeInvestor_bot")
            parent_id = m.is_reply_to
            if parent_id in messages:
                parent = messages[m.is_reply_to]

                if parent not in unserviced:
                    print(f"Duplicate or misordered response to request {parent}")
                else:
                    unserviced.remove(parent)

                delay = (m.time - parent.time).total_seconds()
                delays.append(delay)
                x.append(m.time.timestamp())
            else:
                # Bot reply to an earlier request
                # print(f"Skipping {m.id}")
                pass
        else:
            assert(m.author != "MemeInvestor_bot")
            unserviced.append(m)

    # pprint(delays)
    print(f"len(delays) = {len(delays)}")
    print(f"max(delays) = {max(delays)}")
    print(f"len(unserviced) = {len(unserviced)}")

    # for m in message_list:
    #     if m not in unserviced:
    #         print(m.time)
    #     else:
    #         print(str(m.time) + " -- UNSERVICED")

    # Plot unserviced
    # t0 = message_list[0].time
    # unserviced_times = [int((m.time - t0).total_seconds()) for m in unserviced]
    # bar_heights = [1 for m in unserviced]
    # plot_delays_in_order(unserviced_times, bar_heights)

    # Plot delays
    # plot_delays_in_order(x, delays)

    # Plot histogram of delays
    plot_delays_histogram(delays)

    # Plot timing of requests
    # message_list = [m for m in message_list if m.author != "MemeInvestor_bot"]
    # plot_requests_or_replies_over_time(message_list)

    # Plot timing of responses
    # message_list = [m for m in message_list if m.author == "MemeInvestor_bot"]
    # plot_requests_or_replies_over_time(message_list)

def plot_delays_in_order(x, delays):
    assert(len(x) == len(delays))

    fig, ax = plt.subplots()

    # n_groups = len(delays)
    # index = np.arange(n_groups)

    bar_width = 50.0

    # rects1 = ax.bar(index, delays, bar_width)
    rects1 = ax.bar(x, delays, bar_width)

    # ax.set_xlabel('Group')
    # ax.set_ylabel('Scores')
    ax.set_xlim([0, 23000])
    ax.set_title('Unserviced requests')
    # ax.set_xticks(index + bar_width / 2)
    # ax.set_xticklabels(('A', 'B', 'C', 'D', 'E'))
    # ax.legend()

    fig.tight_layout()
    plt.show()

def plot_delays_histogram(delays):
    x = delays

    bins = range(0, int(max(x)), 10)

    fig, ax = plt.subplots()

    # the histogram of the data
    n, bins, patches = ax.hist(x, bins=bins, rwidth=1.0, cumulative=False, density=True)

    # ax.set_xlabel('Time')
    # ax.set_ylabel('#messages')
    # ax.set_title('Requests per minute over six hours')
    # ax.set_title('Responses per minute over six hours')

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.show()    

def plot_requests_or_replies_over_time(messages):
    print(len(messages))

    t0 = messages[0].time
    x = [int((m.time - t0).total_seconds()) for m in messages]

    num_bins = 50
    bins = range(0, x[len(x)-1], 60)

    # bins = [t0 + n*60 for n in range()]

    fig, ax = plt.subplots()

    # the histogram of the data
    n, bins, patches = ax.hist(x, bins=bins, rwidth=1)

    # ax.set_xlabel('Time')
    # ax.set_ylabel('#messages')
    ax.set_title('Messages per minute')

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()